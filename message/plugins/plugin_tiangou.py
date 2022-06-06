from email.mime import base
import sys
from . import base_utility
alia = ['舔狗']

permission = {
    'group' : [True,[]],
    'private' : [True,[]],
    'member_id' : {},
    'role' : 'member'
}
help = {
    'brief_help' : '你想要舔狗吗？',
    'more' : '你想要舔狗吗！接下来三条消息都会被舔狗夸哦！',
    'alia' : alia
}

class plugin_tiangou(base_utility.base_utility):
    
    def main(self) -> None:
        self.send_back_msg('舔狗启动！！')
        nick_name = self.first_message['sender']['nickname']
        print(nick_name)
        res = yield 1
        self.send_back_msg("哇！%s说得太有道理啦！！！你们再给我听一遍" % nick_name)
        self.send_back_msg(res['message'])
        res = yield 2
        self.send_back_msg(" %s 你~是~我的神！！！！[CQ:at,qq=%s]" % (nick_name,self.first_message['sender']['user_id']))
        res = yield 3
        self.send_back_msg("呜呜，这是我最后一次当你的舔狗了，我不舍得你啊呜呜呜呜，快给我亲亲抱抱举高高呜呜") 