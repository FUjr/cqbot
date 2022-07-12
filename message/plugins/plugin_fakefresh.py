import time
import re
from tokenize import group
from . import base_utility
alia = ['真假新生']
help = {
    'brief_help' : '发送 /真假新生 @要查的人 就可以知道有几个人是真的新生',
    'more' : '发送 /真假新生 @要查的人 机器人会告诉你，xxx还进了哪些群（和机器人的共同群）、进群时间',
    'alia' : alia
}
permission = {
    'group' : [True,[]],
    'private' : [False,[]],
    'member_id' : {},
    'role' : 'member'
}
class plugin_fakefresh(base_utility.base_utility):
    
    
    def run(self,data):
        self.cache_data = {}
        at_info = self.first_message['message']
        rex = r'qq=(\d{1,})'
        check_qq = re.findall(rex,at_info)
        if 'all' in self.first_message['message']:
            self.check_all()
            return False
        if len(check_qq) == 0:
            self.send_back_msg('请发送 /真假新生 @要查的人')
            return False
        else :
            for i in check_qq:
                res = self.get_fakefresh_info(i)
                if len(res) > 0:
                    self.send_back_msg(self.get_at_info(i) + '进入本群的时间为' + self.attend_group_time() + '\n还在这些群里：' + '\n'.join(res))
                else:
                    self.send_back_msg(self.get_at_info(i) + '还没有进入其他群.\n ' + '进入本群的时间为' + self.attend_group_time() )
            return False
        
    def get_fakefresh_info(self,qq) -> False:
        if qq == str(self.first_message['self_id']):
            self.send_back_msg('这么可爱的机器人，怎么可能不是新生呢，快来调戏我')
            return False
        elif qq == '1194436766':
            self.send_back_msg('这么可爱的汤姆，怎么可能不是新生呢')
            return False

        same_group = []
        group_list,group_name_list = self.get_group_list()
        for i in group_list:
            group_name = group_name_list[group_list.index(i)]
            res = self.if_in_other_group(i,qq)
            if (res):
                same_group.append(group_name)
        return same_group
    
    def get_at_info(self,qq) -> str:
        at_info = '[CQ:at,qq=%s]' % qq
        return at_info       
    
    def get_group_list(self) -> list:
        group_list = []
        group_name = []
        group_list_res = self.query_api('get_group_list',{})
        for i in group_list_res['data']:
            group_list.append(i['group_id'])
            group_name.append(i['group_name'])
        return group_list,group_name
    
    def if_in_other_group(self,group_id,qq) -> str:
        in_other = False
        if self.cache_data.get(group_id) == None:
            res = self.query_api('get_group_member_list',{'group_id':group_id})
            self.cache_data[group_id] = res
        else:
            res = self.cache_data[group_id]
        
        for i in res['data']:
            if str(i['user_id']) == str(qq):
                in_other += True
        return in_other
    
    def attend_group_time(self,qq) -> str:
        res = self.query_api('get_group_member_info',{'group_id':self.first_message['group_id'],'user_id':qq})
        timestamp =   res['data']['join_time']
        dt = time.localtime(timestamp)
        return '进本群时间是%s' % time.strftime("%Y-%m-%d %H:%M:%S",dt)
    
    def check_all(self):
        get_user_id_api = 'get_group_member_list'
        user_id_list = self.query_api(get_user_id_api,{'group_id':self.first_message['group_id']})
        group_list,group_name_list = self.get_group_list()
        report_dict = {}
        count = 0
        for i in group_name_list:
            report_dict[i] = 0
        for i in user_id_list['data']:
            if str(i['user_id']) == str(self.first_message['self_id']):
                continue
            if str(i['user_id']) == '1194436766':
                continue
            if str(i['user_id']) == '2854196310':
                continue
            in_other = False
            for j in group_list:
                if j == self.first_message['group_id']:
                    continue
                res = self.if_in_other_group(j,i['user_id'])
                if (res):
                    in_other = True
                    report_dict[group_name_list[group_list.index(j)]] += 1
            if in_other:
                count += 1
        none_zero = '\n'.join([i + ':' + str(report_dict[i]) for i in report_dict if report_dict[i] > 0])
        report = '本群共有%s人进入了其他群，各群人数为\n%s' % (str(count),none_zero)
        self.send_back_msg(report)