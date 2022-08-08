import re
from . import base_utility
import requests
import extension.read_img as read_img
import cv2
import numpy as np
alia = ['fuck','auto']
help = {
    'brief_help' : '回复 理发店bot发的猜成语图片',
    'more' : '回复 理发店bot发的猜成语图片',
    'alia': alia
}
permission = {
    'group' : [True,[]],
    'private' : [False,[]],
    'member_id' : {},
    'role' : ''
}

class plugin_antiguess(base_utility.base_utility):
    def run(self,data):
        reply_re = r'.*?\[CQ:reply,id=(-?\d+)\].*?'
        reply_id = re.findall(reply_re,data['message'])
        if len(reply_id) == 0:
            self.send_back_msg(help['brief_help'])
            return False
        api = 'get_msg'
        post_data = {
            'message_id' : reply_id[0]
        }
        
        res = self.query_api(api,post_data)
        print(res)
        url_re = r'.*?\[CQ:image,.*?url=(.*?)].*?'
        url = re.findall(url_re,res['data']['message'])
        if len(url) == 0:
            self.send_back_msg(help['brief_help'])
            return False
        r = requests.get(url[0])
        
        im = cv2.imdecode(np.frombuffer(r.content, np.uint8), cv2.IMREAD_GRAYSCALE) 
        words = read_img.get_info(im)
        self.send_back_msg('  '.join(words))
        return False