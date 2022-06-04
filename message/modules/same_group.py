from distutils.command.build_scripts import first_line_re
import json
import re

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
class same_group:
    permission = {"permission": "group_only"}
    def __init__(self,api_queue,api_res_queue,log_queue) -> None:
        self.api_queue  = api_queue
        self.api_res_queue = api_res_queue
        self.log_queue = log_queue

    def get_same_people(self,group_list):
        count = 0
        group_member_api = 'get_group_member_list'
        group_info_api = 'get_group_info'
        group_name_list = []
        group_member_set,jointime = self.get_this_group_people()
        other_membe_set = set()
        other_group_jointime = {}
        first_in = 0
        for group_id in group_list:
            self.api_queue.put(group_member_api + '?group_id=' + str(group_id))
            other_group_info = json.loads(self.api_res_queue.get())
            if other_group_info['status'] == "failed" :
                return '[群聊不存在或者我没加群]'
            other_group_list = other_group_info['data']
            self.api_queue.put(group_info_api + '?group_id=' + str(group_id))
            group_name = json.loads(self.api_res_queue.get())['data']['group_name']
            group_name_list.append(group_name)
            
            for member_info  in other_group_list:
                member_id = member_info['user_id']
                other_group_jointime[member_info['user_id']] = member_info['join_time']
                if member_id not in other_membe_set:
                    other_membe_set.add(member_id) 
        for id in group_member_set:
            if id in other_membe_set:
                count +=1
                if other_group_jointime[id] < jointime[id]:
                    first_in += 1
        msg = "本群中出了" + str(count) + "个" + ' '.join(group_name_list) + "的内鬼，" + "其中" + str(first_in) + "个先进的隔壁群"
        return msg
                
                

    def get_this_group_people(self):
        group_member = set()
        jointime = {}
        group_member_api = 'get_group_member_list'
        self.api_queue.put(group_member_api + '?group_id=' + str(self.group_id))
        group_member_id_list = json.loads(self.api_res_queue.get())['data']
        for member_info in group_member_id_list:
            jointime[member_info['user_id']] = member_info['join_time']
            group_member.add(member_info['user_id'])
        return group_member,jointime

    def run(self,data) -> object:
        self.g = self.main()
        self.log_queue.put([2,data])
        next(self.g)
        message = '来看看有几个内鬼吧～ 在下一条消息输入待测群号，用换行以外的字符分隔'
        if data['message_type'] == 'private':
            user_id = data['user_id']
            api = "send_group_msg?user_id=" + str(user_id) +"&message="  + message
            self.api_queue.put(api)
            self.api_res_queue.get()
        elif data['message_type'] == 'group':
            count = 0
            group_id = data['group_id']
            self.group_id = group_id
            api = "send_group_msg?group_id=" + str(group_id) +"&message="  + message
            self.log_queue.put([1,api])
            self.api_queue.put(api)
            self.api_res_queue.get()
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
        self.log_queue.put([1,group_id_list])
        msg = 0
        msg = self.get_same_people(group_id_list)
        self.log_queue.put([1,msg])
        api = "send_group_msg?group_id=" + str(data['group_id']) +"&message=" + msg
        self.log_queue.put([1,api])
        self.api_queue.put(api)
        self.api_res_queue.get()
