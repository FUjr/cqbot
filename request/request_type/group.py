import json
import time
class group:
    def __init__(self,api_queue,api_res,log_queue):
        self.api_queue = api_queue
        self.api_res = api_res
        self.log_queue =log_queue

    def do(self,data):
        approve = False
        api = 'set_group_add_request'
        if data['sub_type'] == 'add':
            pass
        elif data['sub_type'] == 'invite':
            invite_id = data['user_id']
            approve = True
            flag = data['flag']
            if approve == True:
                self.api_queue.put(api + '?approve=true&flag=' + flag)
                self.log_queue.put([1,self.api_res.get()])
            else:
                self.log_queue.put([1,'ignored friend request' + time.strftime("%Y%m%d",time.localtime())])
                