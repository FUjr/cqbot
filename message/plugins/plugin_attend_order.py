import json

from requests import post
from . import base_utility
alia = ['进群顺序']
help = {
    'brief_help' : '来看看你是怎么进群的吧～',
    'more' : '直接输入 /进群顺序 ，就可以知道你是第几个近群的了',
    'alia': alia
}
permission = {
    'group' : [True,[]],
    'private' : [True,[]],
    'member_id' : {},
    'role' : ''
}
class attend_order(base_utility.base_utility):
    def run(self,data) -> False:
        if data['message_type'] != 'group':
            return False
        self.data = data
        msg = self.get_attend_order()
        self.send_back_msg(data,msg)
        return False

        
    def get_attend_order(self):
        group_id = self.data['group_id']
        user_id = self.data['user_id']

        get_group_member_list = "get_group_member_list"
        post_data = {
            'group_id': group_id
        }
        res = self.query_api(get_group_member_list,post_data)
        if res['status'] == 'failed':
            return False
        member_list = res['data']
        join_time_list = []
        group_member_count = 0
        for member in member_list:
            join_time = member['join_time']
            join_time_list.append(join_time)
            group_member_count += 1

        get_group_member_info = "get_group_member_info"
        post_data = {
            'group_id':group_id,
            'user_id' :user_id
        }
        res = self.query_api(get_group_member_info,post_data)
        if res['status'] == 'failed':
            return False
        your_join_time = res['data']['join_time']
        count = 1
        for time in join_time_list:
            if time < your_join_time:
                count += 1
        return "你是本群" + str(group_member_count) + "人里第" +str(count)  + "个加入的dalao"