import re
class cq_reply:
    def __init__(self, data, api_queue, api_res,log_queue):
        self.api_queue = api_queue
        self.api_res = api_res
        self.log_queue = log_queue
        self.content_livetime = 300
        
    def run(self,data):
        #命令前置功能
        rex = r'(\/.*) '
        command_list = re.findall(rex,data['message'])
        if len(command_list) > 0:
            command = command_list[0]
            data['message'] = data['message'].replace(command, '')
            data['message'] = command + ' ' + data['message']
        return data