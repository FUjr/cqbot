import json
import sys
import os
import __main__
from importlib import reload

alia = ['reload']

permission = {
    'group' : [False,[]],
    'private' : [False,[1194436766]],
    'member_id' : {},
    'role' : 0
}

help = {
    'brief_help' : '用于刷新新的插件',
    'more' : '用于刷新新的插件，仅我可用',
    'alia' : alia
}


class reload_plugin:
    def __init__(self,api_queue,api_res_queue,log_queue) -> None:
        self.log_queue = log_queue

    def run(self,data) -> False:

        command = data['message'].split(' ')
        if len(command) == 1:
            self.reload_help()
            self.reload_alias()
        if len(command) == 2:
            if command[1] == 'help':
                self.reload_help()
            elif command[1] == 'alia':
                self.reload_alias()
        if len(command) == 3:
            if command[1] == 'permission':
                msg = self.reset_permission(command[2])
                msg = msg if msg != '' else 'command not found'
        return False

    def reload_help(self):
        dir = os.path.dirname(__file__)
        filelist = os.listdir(dir)
        help_info_dir = {}
        for i in filelist:
            if i.endswith('py'):
                module = i.replace('.py',"")
                modulename = __name__.replace(__class__.__name__,"") + module
                if modulename in sys.modules:
                    reload(sys.modules[modulename])
                else:
                    __import__(modulename)
                try: 
                    helps = getattr(sys.modules[modulename],'help')
                    help_info_dir[module] = helps
                except Exception as e:
                    pass
        with open(dir + '/help.json','w') as hlep_file:
            json.dump(help_info_dir,hlep_file)
        __main__.message.plugin.plugin.help_dict = help_info_dir
    def reload_alias(self):
        dir = os.path.dirname(__file__)
        filelist = os.listdir(dir)
        command_dict = {} 
        for i in filelist:
            if i.endswith('py'):
                module = i.replace('.py',"")
                modulename = __name__.replace(__class__.__name__,"") + module
                if modulename in sys.modules:
                    reload(sys.modules[modulename])
                else:
                    __import__(modulename)
                try: 
                    alias = getattr(sys.modules[modulename],'alia')
                    for alia in alias:
                        command_dict[alia] = module
                except Exception as e:
                    pass
        with open(dir + '/command.json','w') as command_file:
            json.dump(command_dict,command_file)
        __main__.message.modules.command_dict = command_dict

    def reset_permission(self,command):
        msg = ''
        permission_file_path = 'permission/'+ command +'_permission.json'
        if os.path.exists(permission_file_path):
            os.remove(permission_file_path)
            msg += 'removed' + permission_file_path
        if command in __main__.message.plugin.plugin.permission_dict:
            del __main__.message.plugin.plugin.permission_dict[command]
            msg += 'removed permission info in memery'
