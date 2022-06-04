import json
import __main__
import sys
import os
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

class menu:
    def __init__(self,api_queue,api_res_queue,log_queue) -> None:
        self.api_queue  = api_queue
        self.api_res_queue = api_res_queue
        self.log_queue = log_queue

    def run(self,data) -> False:
        message = data['message']
        split_msg = message.split(' ')
        if len(split_msg) == 2:
            command = split_msg[1]
            message = self.get_cmd_help(command,'more')
        else:
            message = self.get_cmd_help('all_cmd','brief_help')
        if data['message_type'] == 'private':
            send_api = 'send_msg'
            user_id = data['user_id']
            post_data = {
                'user_id' : user_id,
                'message' : message
            }
        elif data['message_type'] == 'group':
            send_api = 'send_group_msg'
            user_id = data['user_id']
            group_id = data['group_id']
            post_data = {
                'user_id' : user_id,
                'group_id' : group_id,
                'message' : message
            }
        self.api_queue.put([send_api,post_data])
        self.api_res_queue.get()
        return False

    def get_cmd_help(self,cmd,index):
        
        if __main__.message.plugin.plugin.help_dict == {}:
            dir = os.path.dirname(__file__)
            with open(dir + '/help.json') as help_file:
                __main__.message.plugin.plugin.help_dict = json.load(help_file)

        if cmd == 'all_cmd':
            print(__main__.message.plugin.plugin.help_dict)
            msg = ''
            for key in __main__.message.plugin.plugin.help_dict :
                alia_list = ' '.join(__main__.message.plugin.plugin.help_dict[key]['alia'])
                help_info = __main__.message.plugin.plugin.help_dict[key][index]
                cmd_help = '命令：' + alia_list + '\n帮助：' + help_info
                msg += cmd_help
                msg += '\n'
        else:
            if cmd in __main__.message.modules.command_dict:
                cmd = __main__.message.modules.command_dict[cmd]
            if cmd in __main__.message.plugin.plugin.help_dict:
                alia_list = ' '.join(__main__.message.plugin.plugin.help_dict[cmd]['alia'])
                help_info = __main__.message.plugin.plugin.help_dict[cmd][index]
                cmd_help = '命令：' + alia_list + '\n帮助：' + help_info
                msg = cmd_help
            else:
                msg = 'command not found'
        print(msg)
        return msg