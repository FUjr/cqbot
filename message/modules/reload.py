import json
import sys
import os

alia = ['reload']

permission = {
    'group' : [False,[]],
    'private' : [False,[1194436766,]],
    'member_id' : {},
    'role' : ''
}
help = {
    'brief_help' : '用于刷新新的插件',
    'more' : '用于刷新新的插件，仅我可用',
    'alia' : alia
}


class reload:
    def __init__(self,api_queue,api_res_queue,log_queue) -> None:
        self.log_queue = log_queue

    def run(self,data) -> object:
        command_dict = {} 
        help_info_dir = {}
        dir = os.path.dirname(__file__)
        print(dir)
        filelist = os.listdir(dir)
        for i in filelist:
            if i.endswith('py'):
                module = i.replace('.py',"")
                modulename = __name__.replace('reload',"") + module
                __import__(modulename)
                try: 
                    alias = getattr(sys.modules[modulename],'alia')
                    for alia in alias:
                        command_dict[alia] = module
                except Exception as e:
                    pass
                try: 
                    helps = getattr(sys.modules[modulename],'help')
                    help_info_dir[module] = helps
                except Exception as e:
                    pass
        with open(dir + '/help.json','w') as hlep_file:
            json.dump(help_info_dir,hlep_file)
        with open(dir + '/command.json','w') as command_file:
            json.dump(command_dict,command_file)
        return False

