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

import inspect
import json
import logging

import pydantic
from jsonrpc.exceptions import (
    JSONRPCInvalidParams,
    JSONRPCInvalidRequest,
    JSONRPCInvalidRequestException,
    JSONRPCMethodNotFound,
    JSONRPCParseError,
    JSONRPCServerError,
    JSONRPCDispatchException,
)
from jsonrpc.jsonrpc import JSONRPCRequest
from jsonrpc.jsonrpc1 import JSONRPC10Response
from jsonrpc.jsonrpc2 import (
    JSONRPC20BatchRequest,
    JSONRPC20BatchResponse,
    JSONRPC20Response,
)
from jsonrpc.utils import is_invalid_params

logger = logging.getLogger(__name__)


class JSONRPCResponseAsyncManager(object):
    """
    JSON-RPC response manager.

    Method brings syntactic sugar into library. Given dispatcher it handles
    request (both single and batch) and handles errors.
    Request could be handled in parallel, it is server responsibility.

    :param str request_str: json string. Will be converted into
        JSONRPC20Request, JSONRPC20BatchRequest or JSONRPC10Request

    :param dict dispather: dict<function_name:function>.

    """

    RESPONSE_CLASS_MAP = {
        "1.0": JSONRPC10Response,
        "2.0": JSONRPC20Response,
    }

    @classmethod
    async def handle(cls, request_str, dispatcher):
        if isinstance(request_str, bytes):
            request_str = request_str.decode("utf-8")

        try:
            data = json.loads(request_str)
        except (TypeError, ValueError):
            return JSONRPC20Response(error=JSONRPCParseError()._data)

        try:
            request = JSONRPCRequest.from_data(data)
        except JSONRPCInvalidRequestException:
            return JSONRPC20Response(error=JSONRPCInvalidRequest()._data)

        return await cls.handle_request(request, dispatcher)

    @classmethod
    async def handle_request(cls, request, dispatcher):
        """
        Handle request data.

        At this moment request has correct jsonrpc format.

        :param dict request: data parsed from request_str.
        :param jsonrpc.dispatcher.Dispatcher dispatcher:

        .. versionadded: 1.8.0

        """
        rs = request if isinstance(request, JSONRPC20BatchRequest) \
            else [request]
        responses = [r async for r in cls._get_responses(rs, dispatcher)
                     if r is not None]

        # notifications
        if not responses:
            return

        if isinstance(request, JSONRPC20BatchRequest):
            response = JSONRPC20BatchResponse(*responses)
            response.request = request
            return response
        else:
            return responses[0]

    @classmethod  # noqa: C901
    async def _get_responses(cls, requests, dispatcher):  # noqa: C901
        """ Response to each single JSON-RPC Request.

        :return iterator(JSONRPC20Response):

        .. versionadded: 1.9.0
          TypeError inside the function is distinguished from Invalid Params.

        """
        for request in requests:
            def make_response(**kwargs):
                response = cls.RESPONSE_CLASS_MAP[request.JSONRPC_VERSION](
                    _id=request._id, **kwargs)
                response.request = request
                return response

            output = None
            try:
                method = dispatcher[request.method]
            except KeyError:
                output = make_response(error=JSONRPCMethodNotFound()._data)
            else:
                try:
                    result = method(*request.args, **request.kwargs)
                    if inspect.isawaitable(result):
                        result = await result
                    # Find pydantic models and convert them to dict
                    if isinstance(result, pydantic.BaseModel):
                        result = result.dict()
                    elif isinstance(result, list):
                        result = [x.dict() if isinstance(x, pydantic.BaseModel) else x for x in result]
                except JSONRPCDispatchException as e:
                    output = make_response(error=e.error._data)
                except Exception as e:
                    err_args = e.args
                    if e.__class__.__name__ == 'ValidationError':
                        err_args = None
                    data = {
                        "type": e.__class__.__name__,
                        "args": err_args,
                        "message": str(e),
                    }

                    logger.exception("API Exception: {0}".format(data))

                    if isinstance(e, TypeError) and is_invalid_params(
                            method, *request.args, **request.kwargs):
                        output = make_response(
                            error=JSONRPCInvalidParams(data=data)._data)
                    else:
                        output = make_response(
                            error=JSONRPCServerError(data=data)._data)
                else:
                    output = make_response(result=result)
            finally:
                if not request.is_notification:
                    yield output
