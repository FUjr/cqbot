import json
class kengvip:
    permission = {"permission": "group_only"}
    def __init__(self,api_queue,api_res_queue,log_queue) -> None:
        self.api_queue  = api_queue
        self.api_res_queue = api_res_queue
        self.log_queue = log_queue

    def get_group_info(self):
        count = 0
        group_member_api = 'get_group_member_list'
        self.api_queue.put(group_member_api + '?group_id=' + str(942566374))
        res = json.loads(self.api_res_queue.get())
        vip_group_member_list = res["data"]
        if res["status"] == "failed":
            return '[群聊不存在]'
        self.api_queue.put(group_member_api + '?group_id=' + str(self.group_id))
        group_member_list = json.loads(self.api_res_queue.get())['data']
        vip_id_set = set()
        for vip_id in vip_group_member_list:
            vip_id_set.add(vip_id['user_id'])
        for group_member_id in group_member_list:
            if group_member_id['user_id'] in vip_id_set:
                count += 1
        return str(count)
                
                

    
    def run(self,data) -> object:
        message = '来看看大雕在这个群坑了多少人去付费群吧～'
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
            count = self.get_group_info()
            count = str(count)
            self.log_queue.put([1,count])
            api = "send_group_msg?group_id=" + str(group_id) +"&message=大雕在本群一共割了"  + count + "颗韭菜"
            self.log_queue.put([1,api])
            self.api_queue.put(api)
            self.api_res_queue.get()
        return False

    