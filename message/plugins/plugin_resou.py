import json
import requests
from . import base_utility
import time
import json
alia = ['resou','热搜','微博热搜','’百度热搜','知乎热搜','抖音热搜']

permission = {
    'group' : [True,[]],
    'private' : [True,[]],
    'member_id' : {},
    'role' : 'member'
}
help = {
    'brief_help' : '发送/resou /热搜获取实时热搜(默认微博）',
    'more' : '发送/resou /热搜获取实时热搜（默认微博，后面跟上 抖音、知乎、百度可获得其他网站热搜',
    'alia' : alia
}
class plugin_resou(base_utility.base_utility):
    def get_message(self,url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                return None
        except Exception as e:
            print(e)
            return None
        
    def run(self,data):
        url = []
        resoutype = []
        if '抖音' in data['message']:
            url.append('https://tenapi.cn/douyinresou/')
            resoutype.append('抖音')
        if '知乎' in data['message']:
            url.append('https://tenapi.cn/zhihuresou/')
            resoutype.append('知乎')
        if 'bilibili' in data['message']:
            url.append('https://tenapi.cn/bilihot/')
            resoutype.append('bilibili')
        if '百度' in data['message']:
            url.append('https://tenapi.cn/baiduhot/')
            resoutype.append('百度')
        if '微博' in data['message']:
            url.append('https://tenapi.cn/resou/')
            resoutype.append('微博')
        if len(url) == 0:
            url.append('https://tenapi.cn/resou/')
            resoutype.append('微博')
        for thisurl in url:
            res = self.get_message(thisurl)
            resou = '[%s]%s热搜\n'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),resoutype[url.index(thisurl)])
            if res:
                for i in res['list']:
                    
                    if resoutype[url.index(thisurl)] == '抖音' or resoutype[url.index(thisurl)] == '微博' or resoutype[url.index(thisurl)] == '百度':
                        resou += '%d %s [热度 %s] \n' %(res['list'].index(i)+1,i['name'],i['hot'])
                    elif resoutype[url.index(thisurl)] == '知乎':
                        resou += '%d %s [关键词 %s] \n' %(res['list'].index(i)+1,i['query'],i['name'])
                    elif resoutype[url.index(thisurl)] == 'bilibili':
                        resou += '%d %s  \n' %(res['list'].index(i)+1,i['showname'])
            self.send_back_msg(resou)
                
        return False
