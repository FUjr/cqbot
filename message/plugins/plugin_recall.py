import time
import re
from . import base_utility
alia = ['撤回','recall']
help = {
    'brief_help' : '发送 /撤回 并引用相应消息，就可以撤回相应消息，如果是群管理员支持撤回成员的消息',
    'more' : '发送 /撤回 并引用相应消息，就可以撤回相应消息，如果是群管理员支持撤回成员的消息',
    'alia' : alia
}

permission = {
    'group' : [True,[]],
    'private' : [False,[]],
    'member_id' : {},
    'role' : 'member',
}

class plugin_recall(base_utility.base_utility):
    def run(self,data) -> False:
        rex = r'\[CQ:reply,id=(-?\d+)\]'
        delete_msg_id = re.findall(rex,data['raw_message'])
        if len(delete_msg_id) == 0:
            self.send_back_msg('请引用相应消息，如果是群管理员支持撤回成员的消息')
            return False
        else :
            delete_msg_id = delete_msg_id[0]
            delete_api = 'delete_msg'
            post_data = {
                'message_id' : delete_msg_id
            }
            res = self.query_api(delete_api,post_data)
            print(data,post_data,res)
            if res['status'] == 'ok':
                self.send_back_msg('消息已撤回')
                post_data =  {
                    'message_id' : self.first_message['message_id']
                }
                res1 = self.query_api(delete_api,post_data)
                if res1['status'] == 'failed':
                    self.send_back_msg('您的消息撤回失败，请自行撤回')
            
            elif res['status'] == 'failed':
                if res['wording'] == 'recall error: 1001 msg: No message meets the requirements':
                    self.send_back_msg('里在干婶莫？没有管理员权限撤回成员消息？')
                else:
                    self.send_back_msg(res['wording'])
            return False