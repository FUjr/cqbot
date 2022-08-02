import request
from . import base_utility
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
    def __init__(self, config):
        super().__init__(config)
        self.url = 'https://tenapi.cn/resou/'


    def get_message(self):
        try:
            response = request.get(self.url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return None
        
    def run(self):
        res = self.get_message()
        resou = '现在热搜：'
        if res:
            for i in res[list]:
                resou += '%s 热度 %s \n' %(i['name'],i['hot'])
            self.send_back_msg(resou)
                
        return False
