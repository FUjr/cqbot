import json
class attend_order:
    def __init__(self,api_queue,api_res_queue,log_queue) -> None:
        self.api_queue  = api_queue
        self.api_res_queue = api_res_queue
        self.log_queue = log_queue

    def run(self,data) -> False:
        if data['message_type'] != 'group':
            return False
        self.data = data
        msg = self.get_attend_order()
        api = "send_group_msg?group_id=" + str(data['group_id']) + "&message=" + msg
        self.log_queue.put([1,api])
        self.api_queue.put(api)
        self.api_res_queue.get()
        return False

        
    def get_attend_order(self):
        group_id = self.data['group_id']
        user_id = self.data['user_id']
        api = "get_group_member_list?group_id=" + str(group_id)
        self.api_queue.put(api)
        res = json.loads(self.api_res_queue.get())
        if res['status'] == 'failed':
            return False
        member_list = res['data']
        join_time_list = []
        group_member_count = 0
        for member in member_list:
            join_time = member['join_time']
            join_time_list.append(join_time)
            group_member_count += 1
        api = "get_group_member_info?group_id=" + str(group_id) + "&user_id=" + str(user_id)
        self.api_queue.put(api)
        res = json.loads(self.api_res_queue.get())
        if res['status'] == 'failed':
            return False
        your_join_time = res['data']['join_time']
        count = 1
        for time in join_time_list:
            if time < your_join_time:
                count += 1
        return "你是本群" + str(group_member_count) + "人里第" +str(count)  + "个加入的dalao"
                
