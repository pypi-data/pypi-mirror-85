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

import datetime
import json
from abc import ABCMeta, abstractmethod
from json import JSONEncoder
from typing import Callable

from jsonrpc import Dispatcher
from jsonrpc.exceptions import JSONRPCInvalidRequest, JSONRPCInvalidRequestException, JSONRPCParseError
from jsonrpc.jsonrpc import JSONRPCRequest
from jsonrpc.jsonrpc2 import JSONRPC20Response

from sizzlews.jsonrpc.manager import JSONRPCResponseAsyncManager

API_METHOD_VERSION = 'version'
API_METHOD_PING = 'ping'

ANNOTATIONS_RPC_METHOD_PROPERTY = '_rpc_method'
ANNOTATIONS_IGNORE_PREFIX_PROPERTY = '_rpc_ignore_prefix'


class SizzleWSSession(object):

    def __init__(self, session_id: object):
        self.__id = session_id

    def id(self):
        return self.__id


class SizzleWSJsonEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()


class SizzleWSHandler(object):

    def __init__(self, dispatcher: Dispatcher = None, expose_version_api=True, expose_ping_api=True) -> None:
        self.dispatcher = dispatcher or Dispatcher()
        self.__api_version = None  # type: str
        self.encoder = SizzleWSJsonEncoder()
        if expose_version_api:
            self.dispatcher[API_METHOD_VERSION] = self.m_get_version
        if expose_ping_api:
            self.dispatcher[API_METHOD_PING] = self.m_ping
        self.on_dispatcher_prepare(self.dispatcher)

    def on_dispatcher_prepare(self, dispatcher: Dispatcher):
        pass

    def m_get_version(self):
        return self.__api_version or "<unknown>"

    def m_ping(self):
        return "pong"

    def check_permissions(self):
        pass

    def _parse_request(self, request_str) -> JSONRPCRequest:
        if isinstance(request_str, bytes):
            request_str = request_str.decode("utf-8")
        data = json.loads(request_str)
        return JSONRPCRequest.from_data(data)

    def _build_response_str(self, response: JSONRPC20Response):
        return self.encoder.encode(response.data)

    async def handle(self, request_str, ctx: object) -> str:
        try:
            request = self._parse_request(request_str)
        except (TypeError, ValueError):
            return self._build_response_str(JSONRPC20Response(error=JSONRPCParseError()._data))
        except JSONRPCInvalidRequestException:
            return self._build_response_str(JSONRPC20Response(error=JSONRPCInvalidRequest()._data))

        # TODO: Middleware
        # TODO: Auth

        return self._build_response_str(await JSONRPCResponseAsyncManager.handle_request(request, self.dispatcher))


class BidirectionalSizzleWSSession(SizzleWSSession):

    def __init__(self, session_id: object, connection):
        super().__init__(session_id)
        self.connection = connection

    def id(self):
        return self.__id


class BiDirectionalSizzleWSHandler(SizzleWSHandler, metaclass=ABCMeta):

    def __init__(self, dispatcher: Dispatcher = None, expose_version_api=True, expose_ping_api=True) -> None:
        super().__init__(dispatcher, expose_version_api, expose_ping_api)
        self.sessions = dict()  # type: dict[int]

    @abstractmethod
    def post_message(self, message: JSONRPCRequest, session: BidirectionalSizzleWSSession):
        pass

    def register_session(self, session: SizzleWSSession):
        self.sessions[session.id] = session

    def broadcast(self, message: JSONRPCRequest, session_filter: Callable[[BidirectionalSizzleWSSession], bool]):
        for session_id, session in self.sessions.items():
            if session_filter is not None and session_filter(session):
                try:
                    self.post_message(message, session)
                except Exception:
                    # TODO: Log failure
                    pass


class MethodDiscoveryMixin(object):
    METHOD_PREFXIX = ""

    def on_dispatcher_prepare(self, dispatcher: Dispatcher):
        for name in dir(self):
            item = getattr(self, name)
            if callable(item) and hasattr(item, ANNOTATIONS_RPC_METHOD_PROPERTY):
                rpc_name = getattr(item, ANNOTATIONS_RPC_METHOD_PROPERTY)
                if not getattr(item, ANNOTATIONS_IGNORE_PREFIX_PROPERTY, False):
                    rpc_name = self.METHOD_PREFXIX + rpc_name
                dispatcher.add_method(item, rpc_name)


class ClassBasedSizzleWSHandler(SizzleWSHandler):
    METHOD_PREFXIX = ""

    def __init__(self, dispatcher: Dispatcher = None, expose_version_api=True, expose_ping_api=True) -> None:
        super().__init__(dispatcher, expose_version_api, expose_ping_api)

    def on_dispatcher_prepare(self, dispatcher: Dispatcher):
        dispatcher.build_method_map(self, self.METHOD_PREFXIX)
