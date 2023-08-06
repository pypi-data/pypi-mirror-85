#!/usr/bin/env python3
# -*- coding: utf-8 -*-



# from pytgbot.async_test import TestYo
# testyo = TestYo()
# await testyo.async_foo()


from luckydonaldUtils.logger import logging

__author__ = 'luckydonald'

logger = logging.getLogger(__name__)
if __name__ == '__main__':
    logging.add_colored_handler(level=logging.DEBUG)
# end if


import httpx


# noinspection PyCompatibility
class TestYo(object):
    async def make_request(self, foo):
        async with httpx.AsyncClient() as client:
            r: httpx.Response = await client.get('https://www.example.com/')
        # end with
        return r.text + "\n" + foo
    # end if

    def foo(self):
        return self.make_request('foo')
    # end def

    async def async_foo(self):
        return await self.foo()
    # end if
# end class

