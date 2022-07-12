from cmath import e
import re
import json
from . import base_utility
class cq_json(base_utility.base_utility):
    def run(self,data):
        rex = r'\[CQ:json,data=(.*?)\]'
        cqcode_list = re.findall(rex,data['message'])
        if len(cqcode_list) > 0:
            for i in cqcode_list:
                print(i)
                i = self.unescape(i)
                jsondata = json.loads(i)
                if 'com.tencent.miniapp' in jsondata['app']:
                    #miniapp
                    title = jsondata['meta']['detail_1']['title']
                    if title == '哔哩哔哩':
                    #bilibili
                        desc = jsondata['meta']['detail_1']['desc']
                        qqdocurl = jsondata['meta']['detail_1']['qqdocurl']
                        msg = """让我看看谁这么不乖，发小程序？
照顾一下可怜的电脑选手和tim选手吧~
【目前只支持哔哩哔哩】
摘要：%s
链接：%s
""" % (desc,qqdocurl)
                        self.send_back_msg(msg)
                        
        return data
    
    def unescape(self,data):
        unescape_dict = {'&amp;':'&','&#44;':',','&#93;':']','&#91;':'['}
        for i in unescape_dict:
            data = data.replace(i,unescape_dict[i])
        return data
        