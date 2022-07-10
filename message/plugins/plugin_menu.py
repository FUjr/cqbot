import json
import __main__
import time
import sys
import os
from importlib import reload
from . import base_utility
alia = ['help','帮助','menu','菜单','test']
help = {
    'brief_help' : '显示帮助信息',
    'more' : '发送 /菜单 /帮助 /help 可获得所有命令的简介，如果这后面跟着命令名，则会获得其详细信息 \n 如：发送 /help help 会获得帮助的详细信息',
    'alia' : alia
}
permission = {
    'group' : [True,[]],
    'private' : [True,[]],
    'member_id' : {13:14},
    'role' : 'member'
}

class plugin_menu(base_utility.base_utility):

    def run(self,data) -> False:
        message = data['message']
        split_msg = message.split(' ')
        if len(split_msg) == 2:
            command = split_msg[1]
            message = self.get_cmd_help(command,'more')
        else:
            message = self.get_cmd_help('all_cmd','brief_help')
        self.send_back_msg(message)
        return False

    def get_cmd_help(self,cmd,index):
        if __main__.message.load_plugin.load_plugin.help_dict == {}:
            dir = os.path.dirname(__file__)
            with open(dir + '/help.json') as help_file:
                __main__.message.load_plugin.load_plugin.help_dict = json.load(help_file)
        if cmd == 'all_cmd':
            print(__main__.message.load_plugin.load_plugin.help_dict)
            msg = """
欢迎使用本垃圾机器人
    1、本机器人不支持回复临时会话，加好友验证消息为 “机器人” 即可自动通过
    2、触发命令需要在关键词前增加‘/’
    3、机器人开源地址 https://www.github.com/fujr/cqbot,欢迎来提交插件
            """
            
            for key in __main__.message.load_plugin.load_plugin.help_dict :
                if (self.permission_deny(key)):
                    pass
                alia_list = ' '.join(__main__.message.load_plugin.load_plugin.help_dict[key]['alia'])
                help_info = __main__.message.load_plugin.load_plugin.help_dict[key][index]
                cmd_help = '命令：' + alia_list + '\n帮助：' + help_info
                msg += cmd_help
                msg += '\n'
        else:
            if cmd in __main__.message.plugins.command_dict:
                cmd = __main__.message.plugins.command_dict[cmd]
            if cmd in __main__.message.load_plugin.load_plugin.help_dict:
                alia_list = ' '.join(__main__.message.load_plugin.load_plugin.help_dict[cmd]['alia'])
                help_info = __main__.message.load_plugin.load_plugin.help_dict[cmd][index]
                cmd_help = '命令：' + alia_list + '\n帮助：' + help_info
                msg = cmd_help
            else:
                msg = 'command not found'
        return msg
    
    def permission_deny(self,key):
        if self.check_permission(key):
            print('%s permission deny' % key)
            return False
        return True
        
        
    def check_permission(self,command):
        if command in __main__.message.load_plugin.load_plugin.permission_dict:
            permission = __main__.message.load_plugin.load_plugin.permission_dict[command]
        else:
            permission_file_path = os.path.dirname(__file__) + os.sep + 'permission' + os.sep + command +'_permission.json'
            if not os.path.exists(permission_file_path):
                if self.init_permission(command) == False:
                    return False
            with open(permission_file_path,'r') as permission_file:
                try:
                    permission = json.load(permission_file)
                    __main__.message.load_plugin.load_plugin.permission_dict[command] =  permission
                except json.decoder.JSONDecodeError:
                    self.init_permission(command)
                    return False


        user_id = self.first_message['user_id']
        if self.first_message['message_type'] == 'private':
            sendable = permission['private'][0]
            if str(user_id) in permission['private'][1]:
                sendable =not sendable
        
        if self.first_message['message_type'] == 'group':
            group_id = self.first_message['group_id']
            privillege_map = {
                'owner' : 1,
                'admin' : 2,
                'member' : 3 
            }
            sendable = permission['group'][0]
            
            special_member_dict = permission['member_id'].get(str(user_id) + '-' + str(group_id))
            allow_in_all = permission['member_id'].get('all' + '-' + str(user_id))
            command_role_requirement = privillege_map.get(permission.get('role'))
            

            if str(group_id)  in permission['group'][1]:
                #若第一个元素为true，则其他列表为黑名单。第一个元素为false时，则其他列表为白名单。因此当存在性与第一元素相反时，可以判断为true
                sendable = not sendable
            
            #对于群内特殊名单用户，若其在名单且有未过期时间，则获取相反权限
            if isinstance(special_member_dict,dict):
                if isinstance(special_member_dict[user_id],float):
                    if time.time() > special_member_dict[user_id]:
                        sendable = not sendable
                else:
                    sendable = not sendable
                    
            #对all-user的特殊名单，若其在名单且有未过期时间，则直接获得权限

            if isinstance(allow_in_all,float):
                if time.time() > allow_in_all:
                    sendable = True
            elif isinstance(allow_in_all,str):
                sendable = True
                
            if isinstance(command_role_requirement,str):
            #若命令有成员权限需求，则直接判断成员权限即可
                if privillege_map[self.first_message['sender']['role']] < command_role_requirement:
                    return False
        return sendable
            
    def init_permission(self,command):
        permission_file_path = os.path.dirname(__file__)   + os.sep + 'permission' + os.sep + command +'_permission.json'
        if not os.path.isdir(os.path.dirname(__file__)  + os.sep + 'permission'):
            os.mkdir(os.path.dirname(__file__) + os.sep + 'permission')
        with open(permission_file_path,'w') as permission_file:
                modulel_name = __name__.replace(__class__.__name__,'plugins.') + command
                if modulel_name in sys.modules:
                    reload(sys.modules[modulel_name])
                else:
                    __import__(modulel_name)
                try:
                    permission =  getattr(sys.modules[__name__.replace(__class__.__name__,'plugins.') + command], 'permission')
                    json.dump(permission,permission_file)
                except Exception as e:
                    self.log_queue.put([1,e.__context__])
                    self.log_queue.put([1,e.args[0]])
                    return False
        return True