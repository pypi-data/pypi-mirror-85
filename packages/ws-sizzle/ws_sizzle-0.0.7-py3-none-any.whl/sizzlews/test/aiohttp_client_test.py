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

from sizzlews.client.aiohttp import SizzleWsAIOClient
from sizzlews.client.common import RPCInvocationError


class MyDTO(pydantic.BaseModel):
    field1: int
    field2: str


class MyTestApiClient(SizzleWsAIOClient):

    async def some_method(self, a: int, b: int):
        return await self.async_invoke('api.some_method', a, b)

    async def divide_by_zero(self, a: int):
        return await self.async_invoke('api.divide_by_zero', a)

    async def my_dto_method(self):
        return await self.async_invoke('api.my_dto_method', expected_response_type=MyDTO)

    async def returns_list_of_dtos(self) -> List[MyDTO]:
        return await self.async_invoke('api.returns_list_of_dtos', expected_response_type=MyDTO)


client = MyTestApiClient('http://localhost:8888/rpc')


async def main():
    async with client:
        print(await client.some_method(1, 2))
        try:
            print(await client.divide_by_zero(1))
        except RPCInvocationError as e:
            print("Error: " + e.msg)
        try:
            print(await client.my_dto_method())
        except Exception as e:
            print(e)
        try:
            print("List of DTOs")
            print(await client.returns_list_of_dtos())
        except Exception as e:
            print(e)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
