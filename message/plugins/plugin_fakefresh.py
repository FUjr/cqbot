import json
import re
from . import base_utility
alia = ['真假新生']
help = {
    'brief_help' : '发送 /真假新生 @要查的人 就可以知道有几个人是真的新生',
    'more' : '发送 /真假新生 @要查的人 机器人会告诉你，xxx还进了哪些群（和机器人的共同群）、进群时间',
    'alia' : alia
}
permission = {
    'group' : [True,[]],
    'private' : [False,[]],
    'member_id' : {},
    'role' : 'member'
}
class plugin_fakefresh(base_utility.base_utility):
    def run(self,data):
        at_info = self.first_message['message']
        rex = r'qq=(\d{1,})'
        check_qq = re.findall(rex,at_info)
        if len(check_qq) == 0:
            self.send_back_msg('请发送 /真假新生 @要查的人')
            return False
        else :
            for i in check_qq:
                self.get_fakefresh_info(i)
            return False
        
    def get_fakefresh_info(self,qq) -> False:
        same_people_buffer = ''
        group_list = self.get_group_list()
        for i in group_list:
            res = self.get_same_people(i,qq)
            if res != '':
                same_people_buffer += res
                same_people_buffer += '\n'
        if same_people_buffer == '':
            self.send_back_msg(self.attend_group_time(qq))
            return False
        else:
            self.at_info = self.get_at_info(qq)
            self.send_back_msg(self.at_info + '\n' + self.attend_group_time(qq) + '\n' + same_people_buffer)
            return False
    
    def get_at_info(self,qq) -> str:
        at_info = '[CQ:at,qq=%s]' % qq
        return at_info       
    
    def get_group_list(self) -> list:
        group_list = []
        group_list_res = self.query_api('get_group_list',{})
        for i in group_list_res['data']:
            group_list.append(i['group_id'])
        return group_list
    
    def get_same_people(self,group_id,qq) -> str:
        same_people_buffer = ''
        res = self.query_api('get_group_member_list',{'group_id':group_id})
        for i in res['data']:
            print(i['user_id'])
            if i['user_id'] == str(qq):
                same_people_buffer += '还在%s群里\n' % i['group_name']
        return same_people_buffer
    
    def attend_group_time(self,qq) -> str:
        res = self.query_api('get_group_member_info',{'group_id':self.first_message['group_id'],'user_id':qq})
        return '进本群时间是%s' % res['data']['join_time']