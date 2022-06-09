import os
import json
import sys


def reload_alias():
    dir = os.path.dirname(__file__)
    filelist = os.listdir(dir)
    command_dict = {} 
    for i in filelist:
        if i.endswith('py') and i.startswith('plugin_'):
            module = i.replace('.py',"")
            modulename = __name__.replace('.__init__','') + '.' + module
            __import__(modulename)
            try: 
                alias = getattr(sys.modules[modulename],'alia')
                for alia in alias:
                    command_dict[alia] = module
            except Exception as e:
                pass
    cmd_path = dir + os.sep + 'command.json'
    with open(cmd_path,'w') as command_file:
        json.dump(command_dict,command_file)


reload_alias()
cmd_path = os.path.dirname(__file__)  + os.sep + 'command.json'
with open(cmd_path,'r') as command_json:
    command_dict = json.load(command_json)
    