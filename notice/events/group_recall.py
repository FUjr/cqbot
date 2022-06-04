import json # for json.loads
from  . import  urlparse
class group_recall:
    def __init__(self,api_queue,api_res,log_queue):
        self.api_queue = api_queue
        self.api_res = api_res
        self.log_queue =log_queue

    def do(self,data):
        user_id = data['user_id']
        group_id = data['group_id']
        message_id = data['message_id']
        operator_id = data['operator_id']
        self.api_queue.put('get_msg?message_id=' + str(message_id))
        message = self.api_res.get()
        recalled_message_info = json.loads(message)
        
        try:
            self.api_queue.put('get_group_info?group_id=' + str(group_id))
            group_info  = self.api_res.get()
            group_name = json.loads(group_info)['data']['group_name']
        except:
            self.log_queue.put([1,group_info])
        if operator_id == user_id:
            is_admin_recall = ''
        else:
            is_admin_recall = "被管理员%s" %operator_id
        try:
            sender_nick_name = recalled_message_info['data']['sender']['nickname']
        except Exception as e:
            self.log_queue.put([1,e.args])
            sender_nick_name = ''
        try:
            recalled_message = urlparse.urlparse(recalled_message_info['data']['message'])
            
        except:
            recalled_message = '消息获取失败'

        recall_info = urlparse.urlparse("在群(%s) 群号[%s] 的 %s [%s]%s撤回了一条消息\n内容如下" %(group_name ,str(group_id),str(user_id) ,sender_nick_name,is_admin_recall) )
        self.api_queue.put('send_msg?user_id=' + str(1194436766) + '&message=' + recall_info)
        self.log_queue.put([1,self.api_res.get()])
        self.api_queue.put('send_msg?user_id=' + str(1194436766) + '&message=' + recalled_message)
        self.log_queue.put([1,self.api_res.get()])
