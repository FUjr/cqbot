import asyncio
import time
import re

alia = ['定时消息']

permission = {
    'group' : [True,[]],
    'private' : [True,[]],
    'member_id' : {},
    'role' : 'member'
}
help = {
    'brief_help' : '定时消息，命令格式 /定时消息 时间 消息，不允许有多个空格，连续空格',
    'more' : '定时消息，命令格式 /定时消息 时间 消息，不允许有多个空格，连续空格',
    'alia' : alia
}

group_scheduled_msg = {
    
} #以groupid_userid为键，预计发送时间和内容为值

private_scheduled_msg = {
    
} #以user_id为键，预计发送时间和内容为值
from . import base_utility
class plugin_timer(base_utility.base_utility):
    def cmd_parse(self,requrie_cmd_sum,cmd_format):
        splited_cmd = self.first_message['message'].split(' ')
        if len(splited_cmd) < requrie_cmd_sum:
            self.send_back_msg('命令格式：%s' %cmd_format)
            return False
        else:
            return splited_cmd
    
    def parse_time(self,time_arg):
        time_arg = time_arg.replace('：',':').replace('点',":").replace('分','')
        m_year = time.strftime('%Y',time.localtime())
        m_mon = time.strftime('%m',time.localtime())
        m_mday = time.strftime('%d',time.localtime())
        if '.' in time_arg:
            if len(time_arg.split('.')[0].split('-')) == 2:
                time_arg =  m_year + '-' + time_arg
            elif len(time_arg.split('.')[0].split('-')) == 3:
                pass
            else:
                return False
                
        elif '.' not in time_arg:
            rex = r'(\d{1,})'
            if not re.match(rex,time_arg):
                return False
            if 's' in time_arg:
                time_list = re.findall(rex,time_arg)
                if len(time_list) != 1:
                    return False
                return time_list[0]
            elif 'm' in time_arg:
                time_list = re.findall(rex,time_arg)
                if len(time_list) != 1:
                    return False
                return int(time_list[0])*60
            elif 'h' in time_arg:
                time_list = re.findall(rex,time_arg)
                if len(time_list) != 1:
                    return False
                return int(time_list[0])*60*60
            elif ':' in time_arg:
                time_arg = m_year + '-' + m_mon + '-' + m_mday + '.' + time_arg 


                
                
        else:
            return False
        
        target_time = time.strptime(time_arg,"%Y-%m-%d.%H:%M")
        target_time = time.mktime(target_time)
        print(time_arg)
        gap_time = target_time - time.time()
        print(gap_time)
        if gap_time < 0:
            return False
        else:
            return gap_time

    def run(self,data):
        self.main()
        return False
    
    def main(self):
        support_form = '[19：00] [20:42] [19点29分] [6-10.18:20] [2022-6-9.18:15] [3s/m/h]'
        cmd_format = '/定时消息 定时 消息'
        require_cmd_sum = 3
        args = self.cmd_parse(require_cmd_sum,cmd_format)
        msg = ' '.join(args[2:])
        try:
            wait_time = int(self.parse_time(args[1]))
            if isinstance(wait_time,int):
                asyncio.create_task(self.delay_callback(wait_time,self.send_back_msg,msg))
                msg_id = self.send_back_msg('已设置定时%s秒 后发送%s' %(wait_time,msg))
                asyncio.create_task(self.delay_recall_message(msg_id['data']['message_id']))
            else:
                self.send_back_msg('请输入未来的时间或者正确的格式 %s' %support_form)
        except Exception as e:
            self.add_log(5,e.args)
            self.send_back_msg('请输入正确的格式 %s' %support_form)
            
    async def delay_recall_message(self,message_id) -> None:
        await asyncio.sleep(5)
        recall_api = 'delete_msg'
        post_data = {
            'message_id' : message_id
        }
        self.query_api(recall_api,post_data)
        
    def query_my_scheduled_msg(self):
        my_scheduled_list = []
        for i in list(group_scheduled_msg.keys()):
            each_user_id = i.split('_')[1]
            if each_user_id == str(self.first_message['user_id']):
                my_scheduled_list.append(i)
        for i in list(private_scheduled_msg.keys()):
            each_user_id = i
            if str(each_user_id) == str(self.first_message['user_id']):
                my_scheduled_list.append(i)
        return i
    
    def query_this_group_msg(self):
        pass