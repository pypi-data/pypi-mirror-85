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
from typing import List

import pydantic

from sizzlews.server.common import ClassBasedSizzleWSHandler
from sizzlews.server.tornado import bootstrap_torando_rpc_application


class MyDTO(pydantic.BaseModel):
    field1: int
    field2: str


class MyApi(ClassBasedSizzleWSHandler):
    METHOD_PREFXIX = "api."

    async def some_method(self, a: int, b):
        await asyncio.sleep(0.1)
        return a + b

    async def divide_by_zero(self, a: int):
        await asyncio.sleep(0.1)
        return 1 / 0

    async def my_dto_method(self):
        return MyDTO(field1=1, field2='str')

    async def returns_list_of_dtos(self) -> List[MyDTO]:
        return [MyDTO(field1=1, field2='str'), MyDTO(field1=2, field2='str2')]


if __name__ == "__main__":
    bootstrap_torando_rpc_application(MyApi(), url_path='/rpc')
