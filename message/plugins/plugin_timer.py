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



from . import base_utility
class plugin_timer(base_utility.base_utility):
    def cmd_parse(self,requrie_cmd_sum,cmd_format):
        splited_cmd = self.first_message['message'].split(' ')
        if len(splited_cmd) != requrie_cmd_sum:
            self.send_back_msg('命令格式：%s' %cmd_format)
            return False
        else:
            return splited_cmd
    
    def parse_time(self,time_arg):
        time_arg = time_arg.replace('：',':').replace('点',":").replace('分','')
        local_time = time.localtime(time.time())
        if '.' in time_arg:
            if len(time_arg.split('.')[0].split('-')) == 2:
                timestruct = '%m-%d.%H:%M'
            elif len(time_arg.split('.')[0].split('-')) == 3:
                timestruct = '%m-%d.%H:%M'
                time_struct = time.strptime(time_arg,timestruct)
                time_struct.tm_year = local_time.tm_year
        elif '.' not in time_arg:
            rex = r'(\d{1,})'
            if not re.match(rex,time_arg):
                return False
            if 's' in time_arg:
                time_list = re.findall(rex,time_arg)
                if len(time_list) != 1:
                    return False
                return time_list[0]
            elif 'm' in time_list:
                time_list = re.findall(rex,time_arg)
                if len(time_list) != 1:
                    return False
                return time_list[0]*60
            elif 'h' in time_list:
                time_list = re.findall(rex,time_arg)
                if len(time_list) != 1:
                    return False
                return time_list[0]*60*60
            elif ':' in time_arg:
                timestruct = '%H:%M'
                time_struct = time.strptime(time_arg,timestruct)
                time_struct.tm_year = local_time.tm_year
                time_struct.tm_mon = local_time.tm_mon
                time_struct.tm_mday = local_time.tm_mday
                
        else:
            return False
        target_time = time.mktime(time_struct)
        gap_time = time.time() - target_time
        if gap_time < 0:
            return False
        else:
            return gap_time
        
    async def delay_callback(self,delay,function,*args,**kwargs):
        await asyncio.sleep(delay)
        function(*args,**kwargs)
     
    def main(self):
        support_form = '[19：00] [20:42] [19点29分] [6-10.18:20] [2022-6-9.18:15] [3s/m/h]'
        cmd_format = '/定时消息 定时 消息'
        require_cmd_sum = 3
        args = self.cmd_parse(require_cmd_sum,cmd_format)
        try:
            wait_time = self.parse_time(args[1])
            if isinstance(wait_time,float) or isinstance(wait_time,int):
                asyncio.create_task(self.delay_callback(args[0],self.send_back_msg,args[2]))
                self.send_back_msg('已设置定时%s秒 后发送%s' %(wait_time,args[1]))
            else:
                self.send_back_msg('请输入未来的时间或者正确的格式 %s' %support_form)
        except:
            self.send_back_msg('请输入正确的格式 %s' %support_form)