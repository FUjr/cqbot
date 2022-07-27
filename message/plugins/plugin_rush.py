import re
from PIL import Image
import requests
import io
import os
import __main__
from . import base_utility
alia = ['揉']
help = {
    'brief_help' : '发送揉@某个人，就可以获得他的表情包啦',
    'more' : '发送揉@某个人，就可以获得他的表情包啦',
    'alia' : alia
}
permission = {
    'group' : [True,[]],
    'private' : [True,[]],
    'member_id' : {},
    'role' : 'member'
}
class plugin_rush(base_utility.base_utility):
    def generate_image(self,qqid):
        if isinstance(qqid, int):
            qqid = str(qqid)
        ava_api = 'http://q1.qlogo.cn/g?b=qq&s=640&nk=%s' % qqid
        res = requests.get(ava_api)
        ava = Image.open(io.BytesIO(res.content))
        ava.convert('RGBA')
        res_gif = []
        with open("hand.gif", "rb") as fp:
            hand = Image.open(fp)

            for i in range(0,4):
                    hand.seek(hand.tell() + 1)
                    hand_x = hand.size[0]
                    hand_y = hand.size[1]
                    bg = Image.new("RGBA", (hand_x, hand_y),'white')
                    hand.convert('RGBA')
                    if i < 3:
                        resized_ava = ava.resize((int(hand_x*(0.7)), int(hand_y*(0.7 - i * 0.1))))
                        bg.paste(resized_ava, (int(hand_x*(0.3)), int(hand_y*(0.3 + i * 0.1))))
                    else:
                        resized_ava = ava.resize((int(hand_x*(0.7)), int(hand_y*0.6)))
                        bg.paste(resized_ava, (int(hand_x*(0.3)), int(hand_y*0.4)))
                    bg = Image.alpha_composite(bg, hand)
                    for x in range(0,hand_x):
                        for y in range(0,hand_y):
                            r,g,b,a = bg.get_pyxel(x,y)
                            if (a == 0):
                                bg.put_pixel((x,y),(255,255,255,-1))
                            
                            
                    res_gif.append(bg)
        print('sussess_generate_image')
        res_gif[0].save('rush/ava_%s.gif' % qqid, save_all=True, append_images=res_gif[1:], loop=0, duration=3)
        
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
            self.send_back_msg("揉@某个人，就可以获得他的表情包啦,也支持使用qq=xxxx的方式")
            return False
        
        