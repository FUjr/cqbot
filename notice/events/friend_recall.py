import json # for json.loads
class friend_recall:
    def __init__(self,api_queue,api_res,log_queue):
        self.api_queue = api_queue
        self.api_res = api_res
        self.log_queue =log_queue

    def do(self,data):
        user_id = data['user_id']
        message_id = data['message_id']
        get_msg = 'get_msg'
        post_data = {
            'message_id' : message_id
        }
        self.api_queue.put([get_msg,post_data])
        message = self.api_res.get()
        recalled_message_info = json.loads(message)
        try:
            sender_nick_name = recalled_message_info['data']['sender']['nickname']
        except:
            self.log_queue.put([1,recalled_message_info])
            sender_nick_name = ''
        try:
            recalled_message = recalled_message_info['data']['message']
            
        except:
            recalled_message = '消息获取失败'

        recall_info = "您的好友 %s [%s]撤回了一条消息\n内容如下" %(str(user_id) ,sender_nick_name) 

        api = 'send_msg'
        post_data = {
            'user_id' : 1194436766,
            'message' : recall_info
        }
        self.api_queue.put([api,post_data])
        self.log_queue.put([1,self.api_res.get()])
        post_data = {
            'user_id' : 1194436766,
            'message' : recalled_message
        }
        self.api_queue.put([api,post_data])
        self.log_queue.put([1,self.api_res.get()])
