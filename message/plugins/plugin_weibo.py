import json
import requests
from . import base_utility
import time
import json
alia = ['resou','热搜']

permission = {
    'group' : [True,[]],
    'private' : [True,[]],
    'member_id' : {},
    'role' : 'member'
}
help = {
    'brief_help' : '发送/resou /热搜获取实时微博热搜',
    'more' : '发送/resou /热搜获取实时微博热搜',
    'alia' : alia
}
class plugin_weibo(base_utility.base_utility):
    def get_message(self):
        self.url = 'https://tenapi.cn/resou/'
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                return None
        except Exception as e:
            return None
        
    def run(self,data):
        res = self.get_message()
        resou = '[%s]热搜\n'%time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        if res:
            for i in res['list']:
                resou += '%d %s [热度 %s] \n' %(res['list'].index(i)+1,i['name'],i['hot'])
            self.send_back_msg(resou)
                
        return False
