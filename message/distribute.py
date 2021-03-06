import time
from . import load_cqcode
from . import load_plugin
from . import plugins
from . import hook
import asyncio

class distribute:
    def __init__(self,api_queue ,api_res_queue ,log_queue,dialog_livetime: int = 360 ,dialog_max_num: int = 1000):
        self.api_queue = api_queue
        self.api_res_queue = api_res_queue
        self.log_queue = log_queue
        self.dialog_list = {}
        #储存的对话对象
        self.dialog_active_list = []
        #最后活跃的聊天
        self.dialog_livetime = dialog_livetime
        self.dialog_max_num = dialog_max_num
        self.hook = hook.hook(self.api_queue,self.api_res_queue,self.log_queue)
        self.cqcode = load_cqcode.load_cqcode(self.api_queue,self.api_res_queue,self.log_queue)

    def distribute(self,data : dict) -> None:
        if_continue = self.hook.run(data)
        if if_continue:
            return 0
        else:
            pass

        #处理cq码
        if '[CQ:' in data['message']:
            data = self.cqcode.distribute_cqcode(data)        
        if data['message_type'] == 'private':
            user_id = data['user_id']
            dialog_id = 'private_' + str(user_id)
        if data['message_type'] == 'group':
            group_id = data ['group_id']
            user_id = data['user_id']
            dialog_id = 'group_' + str(group_id) + '_' + str(user_id)
        #创建对话对象的唯一id
        if dialog_id in list(self.dialog_list.keys()):
            need_content = self.dialog_list[dialog_id].handle_content(data)
            #查看新消息是否需要保存状态
            if need_content :
                #若仍需要保存，则自身移动至活跃对象
                self.dialog_active_list.remove(dialog_id)
                self.dialog_active_list.append(dialog_id)
                if len(self.dialog_active_list) > self.dialog_max_num:
                    #若大于最大对话维持数，则删除最早的对话
                    self.dialog_list.pop(self.dialog_active_list.pop(0))
            else:
            #若无需保存状态，则删除自身
                self.dialog_active_list.remove(dialog_id)
                del self.dialog_list[dialog_id]
            return 0
        #如果存在则使用原有对象
        else:
        #如果不存在则新建对象
            dialog = self.new_dialog(data)
            if dialog :
                self.dialog_list[dialog_id] = dialog
                asyncio.create_task(self.delay_callback(dialog.content_livetime,self.check_lifetime,dialog_id))
                #c创建对话对象的生命周期检查
                self.dialog_active_list.append(dialog_id)
                self.log_queue.put([1,'新建了一个对话：'+ dialog_id])
            else:
                pass
            



    def new_dialog(self,data : dict) -> object:
        dialog = load_plugin.load_plugin(self.api_queue,self.api_res_queue,self.log_queue)
        #初始化对话参数
        dialog = dialog.new_dialog(data)
        
        return dialog
    
    def check_lifetime(self,dialog_id : str) -> bool:
        if dialog_id not in self.dialog_list:
            return False
        dialog = self.dialog_list[dialog_id]
        #对话检查生命周期
        time.time()
        since_last_chat = time.time() - dialog.last_time
        if since_last_chat > dialog.content_livetime:
            #若超过生命周期，则删除对话
            self.dialog_active_list.remove(dialog_id)
            del self.dialog_list[dialog_id]
            self.log_queue.put([1,'对话已过期：'+ dialog_id])
        else:
            
            asyncio.create_task(self.delay_callback(since_last_chat,self.check_lifetime,dialog_id))
            
            
    async def delay_callback(self,delay,function,*args,**kwargs):
        await asyncio.sleep(delay)
        function(*args,**kwargs)