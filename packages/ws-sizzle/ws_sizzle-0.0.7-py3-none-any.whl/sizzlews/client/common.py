#    sizzlews
#    Copyright (C) 2020 Dmitry Berezovsky
#    The MIT License (MIT)
#    
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files
#    (the "Software"), to deal in the Software without restriction,
#    including without limitation the rights to use, copy, modify, merge,
#    publish, distribute, sublicense, and/or sell copies of the Software,
#    and to permit persons to whom the Software is furnished to do so,
#    subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import logging
from abc import ABCMeta, abstractmethod
from typing import Union, Any, Dict, List, Type, Optional

import pydantic

RESPONSE_FIELD_RESULT = 'result'

RESPONSE_FIELD_EROR = 'error'

RESPONSE_FIELD_JSONRPC = 'jsonrpc'

InvocationParams = Union[Dict[str, Any], List[Any]]
InvocationResultType = Type[Union[pydantic.BaseModel, List[pydantic.BaseModel]]]
InvocationResult = Union[pydantic.BaseModel, List[pydantic.BaseModel]]


class JsonRpcRequest(object):
    def __init__(self, method, params: InvocationParams = None) -> None:
        super().__init__()
        self.method = method
        self.paams = params
        self.id = 0

    def to_dict(self) -> dict:
        return {
            "method": self.method,
            "params": self.paams,
            "jsonrpc": "2.0",
            "id": self.id
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class RPCSourceError(Exception):

    def __init__(self, msg: str, type: str, args: List[Any]) -> None:
        super().__init__(msg)
        self.type: str = type
        self.msg: str = msg
        self.args: List[Any] = args


class RPCInvocationError(Exception):

    def __init__(self, msg: str, code: int, data: Dict) -> None:
        super().__init__(msg)
        self.msg: str = msg
        self.code: int = code
        self.data: Dict = data
        self.error: Optional[RPCSourceError] = None

        # If there is data field - try to parse it
        if data is not None:
            self.error = RPCSourceError(
                msg=data.get('message', 'Unknown error'),
                type=data.get('type', 'UNKNOWN'),
                args=data.get('args', []),
            )

    @classmethod
    def from_rpc_dict(cls, rpc_dict: dict) -> 'RPCInvocationError':
        return cls(rpc_dict['message'], rpc_dict['code'], rpc_dict.get('data', None))

    def __repr__(self) -> str:
        if self.error is None:
            return self.msg
        return 'RPC Invocation error {}: {}. Cause: {}: {}'.format(str(self.code), self.msg, self.error.type,
                                                                   self.error.msg)

    def __str__(self):
        return self.__repr__()


class SizzleWsBaseClient(metaclass=ABCMeta):
    def _params_to_rq(self, method_name, args, kwargs) -> JsonRpcRequest:
        params = []
        if args and kwargs:
            raise ValueError("You can't mix named and list arguments")
        if args:
            params = args
        if kwargs:
            params = kwargs
        rq = JsonRpcRequest(method_name, params)
        return rq

    @staticmethod
    def _parse_rpc_response(response: Dict[str, Any],
                            expected_response_type: InvocationResultType = None) -> InvocationResult:
        if RESPONSE_FIELD_JSONRPC not in response or response[RESPONSE_FIELD_JSONRPC] != '2.0':
            raise ValueError('Unknown response format. Expected result should be in JSONRPC 2.0 format')
        if RESPONSE_FIELD_EROR in response:
            raise RPCInvocationError.from_rpc_dict(response[RESPONSE_FIELD_EROR])
        elif RESPONSE_FIELD_RESULT in response:
            if expected_response_type is None:
                return response[RESPONSE_FIELD_RESULT]
            else:
                if isinstance(response[RESPONSE_FIELD_RESULT], list):
                    return list(map(lambda x: expected_response_type.parse_obj(x), response[RESPONSE_FIELD_RESULT]))
                else:
                    return expected_response_type.parse_obj(response[RESPONSE_FIELD_RESULT])


class SizzleWsClient(SizzleWsBaseClient, metaclass=ABCMeta):

    def __init__(self) -> None:
        self._logger = logging.getLogger("SizzleWsClient")

    def init(self):
        pass

    def close(self):
        pass

    def invoke(self, method_name, *args, expected_response_type: InvocationResultType = None, **kwargs):
        rq = self._params_to_rq(method_name, args, kwargs)
        return self._invoke_request(rq, expected_response_type)

    @abstractmethod
    def _invoke_request(self, rq: JsonRpcRequest, expected_response_type: InvocationResultType = None):
        pass

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.close()
            return True
        except Exception as e:
            self._logger.exception("Error while closing SizzleWsClient", e)


class SizzleWsAsyncClient(SizzleWsBaseClient, metaclass=ABCMeta):

    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger("SizzleWsAsyncClient")

    async def init(self):
        pass

    async def close(self):
        pass

    @abstractmethod
    async def _invoke_request(self, rq: JsonRpcRequest, expected_response_type: InvocationResultType = None):
        pass

    async def async_invoke(self, method_name, *args, expected_response_type: InvocationResultType = None, **kwargs):
        rq = self._params_to_rq(method_name, args, kwargs)
        return await self._invoke_request(rq, expected_response_type)

    def __enter__(self):
        raise TypeError("Use async with instead")

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.close()
            return True
        except Exception as e:
            self._logger.exception("Error while closing SizzleWsClient", e)
