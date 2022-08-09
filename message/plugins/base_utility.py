import json
import asyncio
import os
from PIL import Image, ImageDraw, ImageFont
import __main__
class base_utility:
    def __init__(self,first_message,api_queue,api_res_queue,log_queue) -> None:
        self.api_queue  = api_queue
        self.api_res_queue = api_res_queue
        self.log_queue = log_queue
        self.first_message = first_message
        self.trigger = {
            'account_id' : [self.first_message["user_id"]],
        }

    
    def text_to_image(self,texts:list or str):
        start_x = 10
        start_y = 10
        step = 18
        font_size =15
        max_word_perline = 15
        font = 'Dengb.ttf'
        
        if isinstance(texts,str):
            texts = [texts]
        rows_count = len(texts)
        longest_x = 0
        for text in texts:
            x_length = 0
            for  i in text:
                if '\u4e00' <= i <= '\u9fff':
                    x_length += step
                else:
                    x_length += step/2
            if x_length > longest_x:
                longest_x = x_length
            row_count = x_length / step / max_word_perline + 1
            rows_count += int(row_count)
        column_count = int(longest_x / step ) +1 
        if column_count > max_word_perline:
            column_count = max_word_perline + 1
        
        img_x = column_count * (step+1)
        img_y = rows_count * (step+1)
        
        
        im = Image.new('RGB', (img_x,img_y), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(font, font_size)
        
        
        draw_x = start_x
        draw_y = start_y
        for text in texts:
            index = 0
            for j in text:
                index += 1
                draw.text((draw_x, draw_y), j, (0, 0, 0), font=font)
                if '\u4e00' <= j <= '\u9fff':
                    draw_x += step
                else:
                    draw_x += step/2
                if draw_x > img_x - step/2:
                    draw_y += step
                    draw_x = start_x
                
            draw_y += step*2
            draw_x = start_x
        im.save('tmp/%s.jpg' %id(texts))
        return 'tmp/%s.jpg' %id(texts)
    
    def send_image(self,path):
        root_path = os.path.dirname(os.path.abspath(__main__.__file__))
        path = os.path.join(root_path,path)
        cq_code = '[CQ:image,file=file://' + path + ']'
        self.send_back_msg(cq_code)
        
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
                    
    def recall_msg(self,id):
        if isinstance(id,dict):
            id = id['data']['message_id']
        recall_api = 'delete_msg'
        post_data = {
            'message_id' : id
        }
        self.query_api(recall_api,post_data)
        
            

    async def delay_callback(self,delay,function,*args,**kwargs):
        await asyncio.sleep(delay)
        function(*args,**kwargs)
        
    