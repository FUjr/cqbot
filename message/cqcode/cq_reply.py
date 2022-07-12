import re
from . import base_utility
class cq_reply(base_utility.base_utility):  
    def run(self,data):
        #命令前置功能
        rex = r'(\/.*)'
        command_list = re.findall(rex,data['raw_message'])
        if len(command_list) > 0:
            command = command_list[0]
            data['raw_message'] = data['raw_message'].replace(command, '')
            data['raw_message'] = command + ' ' + data['raw_message']
            print(data)
        return data