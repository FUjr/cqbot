import os
import __main__
import json
import asyncio


class base_utility:
    def __init__(self,first_message,api_queue,api_res_queue,log_queue) -> None:
        self.api_queue  = api_queue
        self.api_res_queue = api_res_queue
        self.log_queue = log_queue
        self.first_message = first_message

    

        
    def send_back_msg(self,message):
        if self.first_message['message_type'] == 'private':
            send_api = 'send_msg'
            user_id = self.first_message['user_id']
            post_data = {
                'user_id' : user_id,
                'message' : message
            }
        elif self.first_message['message_type'] == 'group':
            send_api = 'send_group_msg'
            user_id = self.first_message['user_id']
            group_id = self.first_message['group_id']
            post_data = {
                'user_id' : user_id,
                'group_id' : group_id,
                'message' : message
            }
        self.api_queue.put([send_api,post_data])
        return json.loads(self.api_res_queue.get())
    
    def add_log(self,log_level:int,log_msg):
        self.log_queue.put([log_level,log_msg])

    def run(self,data) -> object:
        self.g = self.main()
        next(self.g)
        return self

    def add(self,data) -> None:
        try:
            self.g.send(data)
        except StopIteration:
            return False
        return True

    def query_api(self,api,data):
        self.api_queue.put([api,data])
        return json.loads(self.api_res_queue.get())

    def check_group_role(self,role_level : int):
        role_map = {
            'owner' : 1,
            'admin' : 2,
            'member' : 3
        }
        if self.first_message['message_type'] == 'private':
            return False
        elif self.first_message['message_type'] == 'group':
            if 'sender' in self.first_message:
                if 'role' in self.first_message['sender']:
                    role = self.first_message['sender']['role']
                    this_dialog_role_level = role_map.get(role)
                    if this_dialog_role_level == None:
                        return False
                    elif isinstance(this_dialog_role_level,int):
                        if this_dialog_role_level <= role:
                            return True
        return False
                    
        

    def send_image(self,path):
        root_path = os.path.dirname(os.path.abspath(__main__.__file__))
        path = os.path.join(root_path,path)
        cq_code = '[CQ:image,file=' + path + ']'
        self.send_back_msg(cq_code)
        
    async def delay_callback(self,delay,function,*args,**kwargs):
        await asyncio.sleep(delay)
        function(*args,**kwargs)
        
    