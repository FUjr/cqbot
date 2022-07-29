import time
from . import load_cqcode
from . import load_plugin
from . import plugins
import re
import asyncio

class distribute:
    def __init__(self,api_queue ,api_res_queue ,log_queue,dialog_livetime: int = 360 ,dialog_max_num: int = 1000):
        self.api_queue = api_queue
        self.api_res_queue = api_res_queue
        self.log_queue = log_queue
        #三个管道，用于接收api消息，api消息处理结果，日志
        self.group_dialog_dict = {}
        self.private_dialog_dict = {}
        
        #最后活跃的聊天
        self.dialog_livetime = dialog_livetime
        #默认超时时间360s
        self.dialog_max_num = dialog_max_num
        self.cqcode = load_cqcode.load_cqcode(self.api_queue,self.api_res_queue,self.log_queue)
        

    def distribute(self,data : dict) -> None:
        #处理cq码
        if '[CQ:' in data['message']:
            data = self.cqcode.distribute_cqcode(data)    
        
        if data['message_type'] == 'private':
            user_id = data['user_id']
            dialog_dict = self.private_dialog_dict
            if str(user_id) in dialog_dict:
                selected_dialog_list = dialog_dict[str(user_id)]
            else:
                dialog_dict[str(user_id)] = []
                selected_dialog_list = dialog_dict[str(user_id)]
                
        elif data['message_type'] == 'group':
            group_id = data ['group_id']
            user_id = data['user_id']
            dialog_dict = self.group_dialog_dict
            if str(group_id) in dialog_dict:
                selected_dialog_list = dialog_dict[str(group_id)]
            else:
                dialog_dict[str(group_id)] = []
                selected_dialog_list = dialog_dict[str(group_id)]
        
        
        dialog = False
        self.check_lifetime(selected_dialog_list)
        if len(selected_dialog_list) > 0:
            try:
                for d in selected_dialog_list:
                    res = self.deal_trigger(d.trigger,data)
                    if res == True:
                        dialog = d
                        del selected_dialog_list[selected_dialog_list.index(d)]
            #如果触发了触发器，会直接返回第一个成功触发的对话对象.因此触发器应当小心编写，以免导致占用其他对话
                        break     
            except Exception as e:
                self.log_queue.put([5,'触发器错误：'+ str(e)])


        if not dialog:
            dialog = self.new_dialog(data)
            if dialog:
                dialog.lastcall = time.time()
                selected_dialog_list.append(dialog)

        else:
            need_content = dialog.handle_content(data)
            if need_content:
                dialog.lastcall = time.time()
                selected_dialog_list.append(dialog)
            
        
    



    def new_dialog(self,data : dict) -> object:
        dialog = load_plugin.load_plugin(self.api_queue,self.api_res_queue,self.log_queue)
        #初始化对话参数
        dialog = dialog.new_dialog(data)
        
        return dialog
    
    def check_lifetime(self,dialog_list:list) -> bool:
        next_check = 600
        if len(dialog_list) == 0:
            return False
        
        for i in dialog_list:
            if hasattr(i,'lastcall'):
                if not hasattr(i,'lifetime'):
                    lifetime = self.dialog_livetime
                    res = time.time() - i.lastcall
                else:
                    lifetime = i.lifetime
                    
                if res > lifetime:
                    dialog_list.remove(i)
                    self.log_queue.put([1,'对话已过期，已移除'])
                else:
                    if res > next_check:
                        next_check = res
        asyncio.create_task(self.delay_callback(next_check,self.check_lifetime,dialog_list))
            
    
    
    def deal_trigger(self,trigger:dict,data : dict) -> bool:
        """
        trigger type: dict 用于描述触发器类型[目前只支持account_id / message /function]，对每个trigger type的键值规定如下

        * account_id 是一个列表，满足列表qqid都可以参与其中。
        * message也是一个列表，可以是正则、也可以是字符串
        * function则是一个函数对象，传参为cqhttp的上报消息，由插件的函数判断是否触发
        """
        def account_id_trigger(account_id_list : list,data) -> bool:
            user_id = data['user_id']
            if user_id in account_id_list:
                return True
            return False
        
        def message_trigger(message_list : list,data) -> bool:
            message = data['message']
            for msg in message_list:
                if isinstance(msg,str):
                    if message == msg:
                        return True
                elif isinstance(msg,re.compile):
                    if message.match(msg):
                        return True
            return False
        def function_trigger(trigger_function,data) -> bool:
            res = trigger_function(data)
            if res:
                return True

        support_trigger = {'account_id':account_id_trigger,'message':message_trigger,'function':function_trigger}
        for i in trigger:
            if i in support_trigger:
                print('trigger type: '+i)
                if support_trigger[i](trigger[i],data):
                    return True

            
        
    async def delay_callback(self,delay,function,*args,**kwargs):
        await asyncio.sleep(delay)
        function(*args,**kwargs)