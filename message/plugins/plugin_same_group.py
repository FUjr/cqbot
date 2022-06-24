from distutils.command.build_scripts import first_line_re
import json
import re
from . import base_utility

alia = ['内鬼']
help = {
    'brief_help' : '来看看别的群的内鬼吧～（内鬼是调侃啦）',
    'more' : '首先发送 /内鬼 激活bot，然后现在下一条消息中输入想测试的群号（多个群号可用任意换行以外的字符分割），然后bot就会告诉你本群和那个(些）群有几个共同成员啦～',
    'alia' : alia
}
permission = {
    'group' : [True,[]],
    'private' : [True,[]],
    'member_id' : {},
    'role' : 'member'
}
class plugin_same_group(base_utility.base_utility):
    def get_same_people(self,group_list):
        try:
            if 'detail' in self.first_message['message'] :
                detail_flag = 1
        except:
            pass
        count = 0
        group_member_api = 'get_group_member_list'
        group_info_api = 'get_group_info'
        group_name_list = []
        group_member_set,jointime = self.get_this_group_people()
        other_membe_set = set()
        other_group_jointime = {}
        first_in = 0
        for group_id in group_list:

            post_data = {
                'group_id' : group_id
            }
            other_group_info = self.query_api(group_member_api,post_data)
            if other_group_info['status'] == "failed" :
                return '[群聊不存在或者我没加群]'
            other_group_list = other_group_info['data']
            group_name = self.query_api(group_info_api,post_data)['data']['group_name']
            group_name_list.append(group_name)
            
            for member_info  in other_group_list:
                member_id = member_info['user_id']
                other_group_jointime[member_info['user_id']] = member_info['join_time']
                if member_id not in other_membe_set:
                    other_membe_set.add(member_id) 
        buffer = ''
        for id in group_member_set:
            if id in other_membe_set:
                count +=1
                first_in_flag = '先进的本群'
                if other_group_jointime[id] < jointime[id]:
                    first_in_flag = '先进的隔壁群'
                    first_in += 1
                buffer += str(id) + ' ' +first_in_flag + '\n'
                if len(buffer > 150 and detail_flag == 1):
                    self.send_back_msg(buffer)
                    buffer = ''
        if len(buffer > 0 and detail_flag == 1):
                    self.send_back_msg(buffer)
                    buffer = ''
        msg = "本群中出了" + str(count) + "个" + ' '.join(group_name_list) + "的内鬼，" + "其中" + str(first_in) + "个先进的隔壁群"
        
        return msg
                
                

    def get_this_group_people(self):
        group_member = set()
        jointime = {}

        group_member_api = 'get_group_member_list'
        post_data = {
                'group_id' : self.first_message['group_id']
            }
        group_member_id_list = self.query_api(group_member_api,post_data)['data']
        for member_info in group_member_id_list:
            jointime[member_info['user_id']] = member_info['join_time']
            group_member.add(member_info['user_id'])
        return group_member,jointime

    def run(self,data) -> object:
        self.g = self.main()
        self.add_log(0,data)
        next(self.g)
        message = '来看看有几个内鬼吧～ 在下一条消息输入待测群号，用换行以外的字符分隔'
        if data['message_type'] == 'private':
            return False
        elif data['message_type'] == 'group':
            self.send_back_msg(message)
        return self

    def add(self,data) -> None:
        try:
            self.g.send(data)
        except StopIteration:
            return False
        return True

    def main(self):
        group_id_list = []
        data = yield 1
        rex = r'(\d{1,})'
        message = data['message']
        group_id_list = re.findall(rex,message)
        msg = 0
        msg = self.get_same_people(group_id_list)
        self.add_log(1,msg)
        self.send_back_msg(msg)
