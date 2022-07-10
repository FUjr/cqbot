import sys
from . import base_utility
import asyncio
alia = ['demo']

permission = {
    'group' : [True,[]],
    'private' : [True,[]],
    'member_id' : {},
    'role' : 'member'
}
help = {
    'brief_help' : '这是我用来测试的，无意义',
    'more' : '这是我用来测试的，无意义',
    'alia' : alia
}

class plugin_demo(base_utility.base_utility):

    def main(self) -> None:
        asyncio.create_task(self.send_test())
        res = yield 1
        self.send_back_msg(res['message'])
        self.add_log(self.first_message)
        res = yield 2
        self.send_back_msg(res['message'])
        res = yield 3
        self.send_back_msg(res['message'])

    async def send_test(self):
        await asyncio.sleep(10)
        self.send_back_msg('test')
