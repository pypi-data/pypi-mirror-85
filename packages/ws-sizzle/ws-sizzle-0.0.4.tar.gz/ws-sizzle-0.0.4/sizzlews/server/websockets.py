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

import websockets
from websockets import WebSocketServerProtocol

from sizzlews.server.common import SizzleWSHandler, BiDirectionalSizzleWSHandler, BidirectionalSizzleWSSession


def WebsocketsSizzleWSHandler(api_handler: BiDirectionalSizzleWSHandler):
    async def ws_handler(ws: WebSocketServerProtocol, path: str):
        if path != '/rpc':
            await ws.close(404, "not found")
        session = BidirectionalSizzleWSSession(id(ws), connection=ws)
        api_handler.register_session(session)
        async for message in ws:
            await ws.send(api_handler.handle(message, session))

    return ws_handler


def bootstrap_websockets_rpc_application(api_handler: SizzleWSHandler, port=8888, url_path='/',
                                         host: str = '0.0.0.0', **kwargs):
    start_ws_server = websockets.serve(WebsocketsSizzleWSHandler(api_handler), host, port, **kwargs)
    asyncio.get_event_loop().run_until_complete(start_ws_server)
