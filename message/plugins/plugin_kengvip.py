import json
from . import base_utility
alia = ['大雕的韭菜']
help = {
    'brief_help' : '看看大雕在这个群坑了多少个人去他的付费群吧～',
    'more' : '直接发送 /大雕的韭菜 就可以知道有几颗韭菜被割啦',
    'alia' : alia
}
permission = {
    'group' : [True,[]],
    'private' : [False,[]],
    'member_id' : {},
    'role' : 'member',
    'display' : False,
}
class kengvip(base_utility.base_utility):
    def get_group_info(self):
        count = 0
        group_member_api = 'get_group_member_list'
        post_data = {
            'group_id' : 942566374
        }
        res = self.query_api(group_member_api,post_data)
        vip_group_member_list = res["data"]
        if res["status"] == "failed":
            return '[群聊不存在]'
        
        post_data = {
            'group_id' : self.group_id
        }
        res1 = self.query_api(group_member_api,post_data)

        group_member_list = res1['data']
        vip_id_set = set()
        for vip_id in vip_group_member_list:
            vip_id_set.add(vip_id['user_id'])
        for group_member_id in group_member_list:
            if group_member_id['user_id'] in vip_id_set:
                count += 1
        return str(count)
                
                

    
    def plugin_kengvip(self,data) -> object:
        message = '来看看大雕在这个群坑了多少人去付费群吧～'
        if data['message_type'] == 'private':
            pass
        elif data['message_type'] == 'group':
            self.group_id = data['group_id']
            count = 0
            self.send_back_msg(message)
            count = self.get_group_info()
            count = str(count)
            self.add_log(1,count)
            self.send_back_msg("大雕在本群一共割了"  + count + "颗韭菜")
        return False

    