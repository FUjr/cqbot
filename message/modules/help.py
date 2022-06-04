from . import urlparse

class help:
    def __init__(self,api_queue,api_res_queue,log_queue) -> None:
        self.api_queue  = api_queue
        self.api_res_queue = api_res_queue
        self.log_queue = log_queue

    def run(self,data):
        msg = "目前该帮助信息是写死了的，有空再写自动获取描述。 \n目前支持的功能有 \n 1、查看和你在其他共同群的人数 命令 /内鬼，用法：输入/内鬼 后在下一条消息输入群号，多个群号用飞换行符隔开，正则自动提取。\n  2、大雕的韭菜：用来看看有多少人被坑进付费群。 命令/大雕的韭菜 \n 3、进群顺序 命令 /进群顺序"
        msg = urlparse.urlparse(msg)
        if data['message_type'] == 'private':
            user_id = data['user_id']
            api = "send_group_msg?user_id=" + str(user_id) +"&message="  + msg
            self.api_queue.put(api)
            self.log_queue.put([1,self.api_res_queue.get()])
        elif data['message_type'] == 'group':
            count = 0
            group_id = data['group_id']
            api = "send_group_msg?group_id=" + str(group_id) +"&message="  + msg
            self.log_queue.put([1,api])
            self.api_queue.put(api)
            self.api_res_queue.get()
        return False

