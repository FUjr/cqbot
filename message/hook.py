from . import load_plugin
from . import plugins
import time
import sys
class hook:
    def __init__(self,api_queue,api_res_queue,log_queue) -> None:
        self.api_queue =api_queue
        self.api_res_queue = api_res_queue
        self.log_queue = log_queue
        self.hook_list = {}
    
    def handle_first_message(self,command,construct_msg):
        if command in list(plugins.command_dict.keys()):
                module_name = __name__.replace(__class__.__name__,'plugins.') + plugins.command_dict[command]
                __import__(module_name)
                try:
                    handler = getattr(sys.modules[__name__.replace(__class__.__name__,'plugins.') + plugins.command_dict[command]], plugins.command_dict[command])(data,                                                                                                                                              self.api_queue,self.api_res_queue,self.log_queue)
                    self.log_queue.put([1,'hook_loaded: ' + plugins.command_dict[command]])
                    content = handler.run(construct_msg) #需要保存状态的模块，请在第一次run时返回self，不需要content的请返回False
                    self.log_queue.put([1,'hook_runed: ' + plugins.command_dict[command]])
                    if content != False:
                        return content
                    else:
                        return False
                except Exception as e:
                    self.log_queue.put([1,e.args])
                    return False
        else:
            return False

    def handle_content(self,data,content):
        raw_message = data['raw_message']
        if raw_message.startswith('退出'):
            content = False
            return False
        stillneed = content.add(data)
        if stillneed == True:
            return content
        else:
            return False

    def add_share_one_dialog_hook(self,class_name,dialog_id,data) -> None:
        pass
        
    def add_each_dialog_hook(self,hook_name,hook_plugin,construct_data) -> None:
        pass
        
    def run(self,data):
        if data['message_type'] == 'group':
            user_id = data['user_id']
            group_id = data['group_id']
            dialog_id = 'group_' + str(group_id) + '_' + str(user_id)
            dialog_id_2 = 'group_' + str(group_id)
        #如果返回False则继续往下执行，返回True则结束
        self.log_queue.put([0,data])
        return False