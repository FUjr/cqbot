from math import perm
from . import modules
from . import cqcode
import __main__
import sys
import time
import json
import os
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
        self.data = data
        if data['message_type'] != 'private' and data['message_type'] != 'group':
            return False
        #查看对话类型，若非群聊和私聊，直接退出
        if self.check_blacklist():
            return False
        dialog_content = self.handle_first_message(data)
        return dialog_content #dialog_content 就是self或者false

    def handle_first_message(self,data):
        raw_message = data['raw_message']
        if raw_message.startswith('/'):
            message = raw_message.split(' ')
            command = message[0].split('/')[1]
            if self.check_permission(command): 
                pass
            else:
                self.log_queue.put((5,'permission denied'))
                return False
            if command in list(modules.command_dict.keys()):
                #若在字典内，尝试导入模块
                #__import__(__name__.replace(__class__.__name__,'modules.') + modules.command_dict[command])
                try:
                    handler = getattr(sys.modules[__name__.replace(__class__.__name__,'modules.') + modules.command_dict[command]], modules.command_dict[command])(self.api_queue,self.api_res_queue,self.log_queue)
                    self.log_queue.put([1,'loaded: ' + modules.command_dict[command]])
                    self.content = handler.run(data) #需要保存状态的模块，请在第一次run时返回self，不需要content的请返回False
                    self.log_queue.put([1,'runed: ' + modules.command_dict[command]])
                    if self.content != False:
                        return self
                    else:
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
        
    def check_blacklist(self):
        if not os.path.exists('blacklist.json'):
            default = {
                'user_id' : [],
                'group_id' : []
            }
            with open('blacklist.json','w') as blacklist_file:
                json.dump(default,blacklist_file)
        with open ('blacklist.json','r') as blacklist_file:
            blacklist = json.load(blacklist_file)
        if self.data['message_type'] == 'private':
            if self.data['user_id'] in blacklist['user_id']:
                return True
        elif self.data['message_type'] == 'group':
            if self.data['group_id'] in blacklist['group_id']:
                return True
            if self.data['user_id'] in blacklist['user_id']:
                return True
        return False

    def check_permission(self,command):
        if not os.path.exists('permission/'+ command +'_permission.json'):
            if self.init_permission(command) == False:
                return False
        with open('permission/'+ command +'_permission.json','r') as permission_file:
            try:
                permission = json.load(permission_file)
            except json.decoder.JSONDecodeError:
                self.init_permission(command)
                return False
            if permission['permission'] == 'all':
                return True
            elif permission['permission'] == 'robotowner':
                if self.data['user_id'] in permission['robotowner']:
                    return True
            elif permission['permission'] == 'group_owner':
                pass
            elif permission['permission'] == 'group_admin':
                pass
            elif permission['permission'] == 'group_member':
                pass
            elif permission['permission'] == 'private_only':
                pass
            elif permission['permission'] == 'group_only':
                pass
            else:
                return False
            return False

    def init_permission(self,command):
        if not os.path.isdir('permission'):
            os.mkdir('permission')
        with open('permission/'+ command +'_permission.json','w') as permission_file:
                try:
                    __import__(__name__.replace(__class__.__name__,'modules.') + modules.command_dict[command])
                    permission =  getattr(sys.modules[__name__.replace(__class__.__name__,'modules.') + modules.command_dict[command]], 'permission')
                    json.dump(permission,permission_file)
                except Exception as e:
                    self.log_queue.put([1,e.__context__])
                    self.log_queue.put([1,e.args[0]])
                    return False
        return True