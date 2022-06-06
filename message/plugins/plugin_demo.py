import sys
from . import base_utility
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

class demo(base_utility.base_utility):

    def main(self) -> None:
        res = yield 1
        self.send_back_msg(res['message'])
        res = yield 2
        self.send_back_msg(res['message'])
        res = yield 3
        self.send_back_msg(res['message'])

