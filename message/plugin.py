from . import modules
from . import cqcode
import __main__
import sys
import time
import yaml
class plugin():
    def __init__(self, api_queue, api_res_queue, log_queue,content_livetime: int = 360):
        self.content_livetime = content_livetime
        self.api_queue = api_queue
        self.api_res_queue  = api_res_queue
        self.log_queue = log_queue
        self.last_time = time.time()
        self.content = False

    def new_dialog(self, data):
        #distribute的入口函数，如果该聊天无需保存则返回false，否则返回self
        if data['message_type'] == 'group':#调用黑名单函数
            group_id = data['group_id']
            user_id = data['user_id']
            if not self.check_blacklist_and_permission(user_id,group_id):#调用黑名单函数
                return False
        elif data['message_type'] == 'private':
            user_id = data['user_id']
            if not self.check_blacklist_and_permission(user_id,0):#调用黑名单函数,非群聊传参0
                return False
        else:
            return False
        #查看对话类型，若非群聊和私聊，直接退出

        dialog_content = self.handle_first_message(data)
        return dialog_content #dialog_content 就是self或者false

    def handle_first_message(self,data):
        raw_message = data['raw_message']
        if raw_message.startswith('/'):
            message = raw_message.split(' ')
            command = message[0].split('/')[1]
            if command in list(modules.command_dict.keys()):
                #若在字典内，尝试导入模块
                __import__(__name__.replace(__class__.__name__,'modules.') + modules.command_dict[command])
                try:
                    handler = getattr(sys.modules[__name__.replace(__class__.__name__,'modules.') + modules.command_dict[command]], modules.command_dict[command])(self.api_queue,self.api_res_queue,self.log_queue)
                    self.log_queue.put([1,'loaded: ' + modules.command_dict[command]])
                    self.content = handler.run(data) #需要保存状态的模块，请在第一次run时返回self，不需要content的请返回False
                    self.log_queue.put([1,'runed: ' + modules.command_dict[command]])
                    if self.content != False:
                        return self
                    else :
                        return False
                except Exception as e:
                    self.log_queue.put([1,e.args])
                    return False
            else:
                return False
        return False

    def handle_content(self,data):
        raw_message = data['raw_message']
        if raw_message.startswith('退出'):
            self.content = False
            return False
        stillneed = self.content.add(data)
        if stillneed == True:
            return True
        else:
            self.content = False
            return False
        
    def check_blacklist_and_permission(self,user_id: int,group_id : int):
        
        return True
