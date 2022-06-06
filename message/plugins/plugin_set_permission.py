from xmlrpc.client import FastMarshaller
from . import base_utility
import __main__
import os
import json
alia = ['设置权限']
permission = {
    'group' : [False,[]],
    'private' : [False,[1194436766]],
    'member_id' : {'all_1194436766':''},
    'role' : ''
}
help = {
    'brief_help' : '来看看你是第几个进群的吧～',
    'more' : '直接输入 /进群顺序 ，就可以知道你是第几个进群的了',
    'alia': alia
}
class set_permission(base_utility.base_utility):
    def run(self,data):
        super().run(self,data)
        self.send_back_msg('请输入要设置权限的命令')
    def main(self):
        res = yield 1
        command = res['message']
        if command in __main__.message.plugins.command_dict:
            command = __main__.message.plugins.command_dict[command]
            permission_file_path = 'permission/'+ command +'_permission.json'
            with open(permission_file_path) as permission:
                permission = json.load(permission)
            private_mode = permission['private'][0]
            group_mode = permission['group'][0]
            private_special = permission['private'][1]
            group_special = permission['group'][1]
            special_member = list(permission['member_id'].keys())
            group_role_requirement = permission['group'] if permission['group'] == '' else '在本群身份需要是' + permission['group']
            msg = "当前私聊为:%s模式,%s有:%s \n 当前群聊为%s模式,%s有:%s \n例外成员为 \n %s \n 请输入须要求修改的权限 [群聊、私聊、群成员、群身份]，如果输入的是其他，则会终止执行" %(private_mode,private_mode,private_special,group_mode,group_mode,group_special,special_member,group_role_requirement)
            self.send_back_msg(res,msg)
            res = yield 2
            command = res['message']
            if command not in ['群聊','私聊','群成员','群身份'] :
                return False
            else:
                if command == '群聊':
                    edit_target = 'group'
                    option = ['增加名单','删除名单','改为白名单模式','改为黑名单模式']
                elif command == '私聊':
                    edit_target = 'private'
                    option = ['增加名单','删除名单','改为白名单模式','改为黑名单模式']
                elif command == '群成员':
                    edit_target = 'member_id'
                    option = ['增加名单','删除名单']
                elif command == '群身份':
                    edit_target = 'role'
                    option = ['修改身份']
            msg = "当前选择 %s ,支持的命令为: %s 请输入命令，可以输入空格后输入删除/增加的项目" %(command,option)
            self.send_back_msg(res,msg)
            res = yield 3
            command = res['message']
            command = command.split(' ')
            func = {
                '增加名单':self.add_to_list,
                '删除名单':self.delete_from_list,
                '改为白名单模式':self.swich_whitelist_mode,
                '改为黑名单模式':self.swich_blacklist_mode,
                '修改身份':self.editrole
            }
            if command[0] not in option:
                return False
            if len(command) >= 2:

                permission[command]

        else:
            self.send_back_msg('command not found')

    def add_to_list(self,edit_target,permission,item):
        if edit_target in ['group','private']:
            permission[edit_target][1].append(item)
        else:
            permission[edit_target].append(item)
        
    def delete_from_list(self,edit_target,permission,item):
        if edit_target in ['group','private']:
            permission[edit_target][1].pop(item)
        else:
            permission[edit_target].pop(item)

    def swich_whitelist_mode(self,edit_target,permission,*arg):
        if permission[edit_target][0]:
            return permission
        else:
            permission[edit_target][0] = True
            permission[edit_target][1] = []
            return permission

    def swich_blacklist_mode(self,edit_target,permission,*arg):
        if not permission[edit_target][0]:
            return permission
        else:
            permission[edit_target][0] = False
            permission[edit_target][1] = []
            return permission

    def editrole(self,edit_target,permission,item):