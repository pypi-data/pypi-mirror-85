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

import asyncio
from typing import Any

import tornado.ioloop
import tornado.web
from tornado import httputil

from sizzlews.server.common import SizzleWSHandler


class TornadoHttpSizzleWSHandler(tornado.web.RequestHandler):

    def __init__(self, application: "tornado.web.Application", request: httputil.HTTPServerRequest,
                 **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
        # self._api_handler = None  # type: SizzleWSApiHandler

    def initialize(self, api_handler: SizzleWSHandler):
        self._api_handler = api_handler

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    async def post(self):
        self.write(await self._api_handler.handle(self.request.body, str(self.request.body)))


def bootstrap_torando_rpc_application(api_handler: SizzleWSHandler, port=8888, url_path='/'):
    app = tornado.web.Application([
        (url_path, TornadoHttpSizzleWSHandler, dict(api_handler=api_handler))
    ])
    app.listen(port)
    if not asyncio.get_event_loop().is_running():
        tornado.ioloop.IOLoop.current().start()
    return app
