from . import base_utility
import __main__
import os
import json
import re
alia = ['设置权限']
permission = {
    'group' : [False,[]],
    'private' : [False,['1194436766']],
    'member_id' : {'all-1194436766':''},
    'role' : ''
}
help = {
    'brief_help' : '来看看你是第几个进群的吧～',
    'more' : '直接输入 /进群顺序 ，就可以知道你是第几个进群的了',
    'alia': alia
}
class plugin_set_permission(base_utility.base_utility):
    def run(self,data):
        self.g = self.main()
        next(self.g)
        self.send_back_msg('请输入要设置权限的命令')
        return self
        
    def main(self):
        res = yield 1
        #等待需要修改的指令名称
        command = res['message']
        if command in __main__.message.plugins.command_dict:
            command = __main__.message.plugins.command_dict[command]
            permission_file_path = os.path.dirname(__file__) + os.sep + 'permission' + os.sep + command +'_permission.json'
            if not os.path.exists(permission_file_path):
                self.send_back_msg('该命令没有设置权限,请先触发一次该命令')
                return
            
            with open(permission_file_path) as permission:
                permission = json.load(permission)
            private_mode = '黑名单' if permission['private'][0] else '白名单'
            group_mode = '黑名单' if permission['group'][0] else '白名单'
            private_special = ','.join(permission['private'][1]) if permission['private'][1] else '无'
            group_special = ','.join(permission['group'][1]) if permission['group'][1] else '无'
            special_member = ','.join(list(permission['member_id'].keys())) if permission['member_id'] else '无'
            group_role_requirement = permission['role'] if permission['role'] == '' else '在本群身份需要是' + permission['role']
            #加载权限列表，并输出
            
            msg = "当前私聊为:%s模式,%s有:%s \n 当前群聊为%s模式,%s有:%s \n例外成员为 %s \n %s \n 请输入须要求修改的权限 [群聊、私聊、群成员、群身份]，如果输入的是其他，则会终止执行" %(private_mode,private_mode,private_special,group_mode,group_mode,group_special,special_member,group_role_requirement)
            self.send_back_msg(msg)
            
            res = yield 2
            #获取需要修改的对象
            command = res['message']
            if command not in ['群聊','私聊','群成员','群身份'] :
                self.send_back_msg('输入的选项不支持，已退出')
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
            self.send_back_msg(msg)
            res = yield 3
            #获取需要修改的项目 除了黑白名单，指令 + 名单的入参
            
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
                #如果输入的不是支持的命令，则终止执行
                self.send_back_msg('输入的命令不支持，已退出')
                return False
            
            if len(command) >= 2:
                #如果多于一个参数，则判断是否改黑白名单模式，如果不是，则将后面的参数直接传递给函数
                if command[0] in ['改为白名单模式','改为黑名单模式']:
                    res = funct(edit_target,permission)
                else:
                    itme = res['message'].replace(command[0],'')
                    funct = func[command[0]]
                    res = funct(edit_target,permission,itme)
                    
            elif len(command) == 1:
                funct = func[command[0]]
                if command[0] in ['改为白名单模式','改为黑名单模式'] :
                    res = funct(edit_target,permission)
                else:
                    self.send_back_msg('请输入要添加/删除的成员')
                    res = yield 4
                    item = res['message']
                    res = funct(edit_target,permission,item)
                with open(permission_file_path,'w') as permissionfile:
                    json.dump(res,permissionfile)
                __main__.message.load_plugin.load_plugin.permission_dict = res
                
        else:
            self.send_back_msg('command not found')

    def add_to_list(self,edit_target,permission,item):
        rex = r'(\d{3,})'
        itemlist = []
        for i in item.strip(' ').split(' '):
            if  re.search(rex,i):
                i = re.findall(rex,i)
                itemlist = itemlist + i
        if edit_target in ['group','private']:
            permission[edit_target][1] += itemlist
        else:
            for i in itemlist:
                if self.first_message['message_type'] != 'group':
                    return permission
                else:
                    i = str(self.first_message['group_id']) + '-' + i
                    permission[edit_target].append(i)
        self.send_back_msg('修改完成')
        return permission
        
    def delete_from_list(self,edit_target,permission,item):
        rex = r'(\d{3,})'
        for i in item.strip(' ').split(' '):
            if edit_target in ['group','private']:
                if re.search(rex,i):
                    i = re.findall(rex,i)[0]
                    if i in permission[edit_target][1]:
                        permission[edit_target][1].remove(i)
            elif edit_target == 'member_id':
                if re.search(rex,i):
                    i = re.findall(rex,i)[0]
                    if self.first_message['message_type'] != 'group':
                        self.send_back_msg('请在群聊中使用该命令')
                        return permission
                    else:
                        i = str(self.first_message['group_id']) + '-' + i
                        if i in permission[edit_target]:
                            permission[edit_target].remove(i)
        self.send_back_msg('修改完成')
        return permission

    def swich_whitelist_mode(self,edit_target,permission):
        if not permission[edit_target][0]:
            self.send_back_msg('与原来的模式相同，无需修改')
            return permission
        else:
            permission[edit_target][0] = False
            permission[edit_target][1] = []
            self.send_back_msg('模式已修改为白名单模式')
            return permission

    def swich_blacklist_mode(self,edit_target,permission):
        if  permission[edit_target][0]:
            self.send_back_msg('与原来的模式相同，无需修改')
            return permission
        else:
            permission[edit_target][0] = True
            permission[edit_target][1] = []
            self.send_back_msg('模式已修改为黑名单模式')
            return permission

    def editrole(self,edit_target,permission,item):
        permission[edit_target] = item
        self.send_back_msg('修改完成')
        return permission