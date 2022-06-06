import json
import __main__
import sys
import os
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
            msg = '触发命令需要在关键词前增加/，如需获得某命令的帮助，请输入 /help xxx。'
            for key in __main__.message.load_plugin.load_plugin.help_dict :
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