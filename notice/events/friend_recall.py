import json # for json.loads
from . import urlparse
class friend_recall:
    def __init__(self,api_queue,api_res,log_queue):
        self.api_queue = api_queue
        self.api_res = api_res
        self.log_queue =log_queue

    def do(self,data):
        user_id = data['user_id']
        message_id = data['message_id']
        self.api_queue.put('get_msg?message_id=' + str(message_id))
        message = self.api_res.get()
        recalled_message_info = json.loads(message)
        try:
            sender_nick_name = recalled_message_info['data']['sender']['nickname']
        except:
            self.log_queue.put([1,recalled_message_info])
            sender_nick_name = ''
        try:
            recalled_message = urlparse.urlparse(recalled_message_info['data']['message'])  
        except:
            recalled_message = '消息获取失败'

        recall_info = urlparse.urlparse("您的好友 %s [%s]撤回了一条消息\n内容如下" %(str(user_id) ,sender_nick_name))
        self.api_queue.put('send_msg?user_id=' + str(1194436766) + '&message=' + recall_info)
        self.log_queue.put([1,self.api_res.get()])
        self.api_queue.put('send_msg?user_id=' + str(1194436766) + '&message=' + recalled_message)
        self.log_queue.put([1,self.api_res.get()])
