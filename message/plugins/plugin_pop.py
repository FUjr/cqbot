import requests
from PIL import Image
import io
import os 
import __main__
import re
from . import base_utility
alia = ['拍']
help = {
    'brief_help' : '发送拍【空格】@某个人，就可以获得他的表情包啦',
    'more' : '发送拍【空格】@某个人，就可以获得他的表情包啦',
    'alia' : alia
}
permission = {
    'group' : [True,[]],
    'private' : [True,[]],
    'member_id' : {},
    'role' : 'member'
}
class plugin_pop(base_utility.base_utility):
    def run(self,data):
        self.main()
        return False
    

    def send_image(self,path):
        root_path = os.path.dirname(os.path.abspath(__main__.__file__))
        path = os.path.join(root_path,path)
        cq_code = '[CQ:image,file=file://' + path + ']'
        self.send_back_msg(cq_code)
        
    def main(self):
        rex = r'qq=(\d{1,})'
        match = re.findall(rex, self.first_message['message'])
        if match:
            qqid = match[0]
            self.generate_image(qqid)
            self.send_image('rush/ava_%s.gif' % qqid)
            
            return False
        else:
            self.send_back_msg("拍【空格】@某个人，就可以获得他的表情包啦,也支持使用qq=xxxx的方式")
            return False 
        
        
        
    def generate_image(self,qqid):
        ava_api = 'http://q1.qlogo.cn/g?b=qq&s=640&nk=%s' % str(qqid)
        res = requests.get(ava_api)
        raw_ava = Image.open(io.BytesIO(res.content))
        raw_ava.convert('RGBA')
        for x in range(0,raw_ava.size[0]):
            for y in range(0,raw_ava.size[1]):
                if (x - raw_ava.size[0]*0.5)*(x - raw_ava.size[0]*0.5) + (y - raw_ava.size[1]*0.5)*(y - raw_ava.size[1]*0.5) > 0.25 * raw_ava.size[0]*raw_ava.size[0]:
                    raw_ava.putpixel((x,y),(0,0,0,0))
                    

        with open('pop_1.gif','rb') as f:
            gif = Image.open(f)
            gif_x = gif.size[0]
            gif_y = gif.size[1]
            gif_list = []
            bg = Image.new("RGBA", (gif_x, gif_y))
            moving_ava = Image.new("RGBA", (gif_x, gif_y))
            bg.paste(gif,(0,0))
            ava = raw_ava.resize((35,29))
            moving_ava.paste(ava,(40,40))
            
            bg = Image.alpha_composite(moving_ava,bg)
            gif_list.append(bg)
            count = 0
            y_index = [50,55,63,50,55,40,40]
            resize_y = [35,35,12,22,35,25,25]
            while True:
                try:
                    gif.seek(gif.tell() + 1)
                    bg = Image.new("RGBA", (gif_x, gif_y))
                    bg.paste(gif, (0,0))
                    ava = raw_ava.resize((35,resize_y[count]))
                    moving_ava.paste(ava,(40,y_index[count]))
                    
                    bg = Image.alpha_composite(moving_ava,bg)
                    gif_list.append(bg)
                    count += 1
                except:
                    print(gif.tell())
                    break
                

        gif_list[0].save('.\pop_2.gif',save_all=True,append_images=gif_list[1:], loop=0, duration=10,disposal=2)