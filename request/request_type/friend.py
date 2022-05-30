import json
import time
class friend:
    allow_starts = ['test','内鬼']
    def __init__(self,api_queue,api_res,log_queue):
        self.api_queue = api_queue
        self.api_res = api_res
        self.log_queue =log_queue

    def do(self,data):
        approve = False
        api = 'set_friend_add_request'
        for starts in self.allow_starts:
            if data['comment'].startswith(starts):
                approve = True
                remark = starts + time.strftime("%Y%m%d",time.localtime())
                flag = data['flag']
            if approve == True:
                self.api_queue.put(api + '?approve=true&flag=' + flag + '&remark=' + remark )
                self.log_queue.put([1,self.api_res.get()])
                self.log_queue.put([1,'?approve=true&flag=' + flag + '&remark=' + remark ])
            else:
                self.log_queue.put([1,'ignored friend request' + time.strftime("%Y%m%d",time.localtime()) ])
                