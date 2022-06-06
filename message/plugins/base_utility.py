import abc
import json
class base_utility:
    def __init__(self,api_queue,api_res_queue,log_queue) -> None:
        self.api_queue  = api_queue
        self.api_res_queue = api_res_queue
        self.log_queue = log_queue

    def send_back_msg(self,data:dict,message):
        if data['message_type'] == 'private':
            send_api = 'send_msg'
            user_id = data['user_id']
            post_data = {
                'user_id' : user_id,
                'message' : message
            }
        elif data['message_type'] == 'group':
            send_api = 'send_group_msg'
            user_id = data['user_id']
            group_id = data['group_id']
            post_data = {
                'user_id' : user_id,
                'group_id' : group_id,
                'message' : message
            }
        self.api_queue.put([send_api,post_data])
        self.api_res_queue.get() 
    

    def add_log(self,log_level:int,log_msg):
        self.log_queue.put([log_level,log_msg])

    def run(self,data) -> object:
        self.g = self.main()
        next(self.g)
        return self

    def add(self,data) -> None:
        try:
            self.g.send(data)
        except StopIteration:
            return False
        return True

    def query_api(self,api,data):
        self.api_queue.put([api,data])
        return json.loads(self.api_res_queue.get())
