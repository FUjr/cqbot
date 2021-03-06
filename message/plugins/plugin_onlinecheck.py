from xmlrpc.client import FastParser
from .get_ip import get_ip
import requests
from . import base_utility
import time
import __main__
import json
import asyncio

alia = ['窥屏检测','在线监测','在线检测']

permission = {
    'group' : [True,[]],
    'private' : [True,[]],
    'member_id' : {},
    'role' : 'member',
}
help = {
    'brief_help' : '发送/在线检测 即可检测有几个群友在线~',
    'more' : '发送/在线检测 即可检测有几个群友在线~',
    'alia' : alia
}

class plugin_onlinecheck(base_utility.base_utility):
    def run(self,data):    
        #发送一条包含xml的消息
        url = 'http://onlinecheck.fjrcn.cn/'
        random_code = ''.join(str(time.time()).split('.'))
        ramdomUrl = url + random_code
        self.random_code = random_code
        waittime = 30
        self.waittime = waittime
        xml_msg = """
<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<msg serviceID="1" templateID="12345" action="web" brief="%ds后自动撤回" sourceMsgId="0" url="www.baidu.com" flag="0" adverSign="0" multiMsgFlag="0">
<item layout="2" advertiser_id="0" aid="0"><picture cover="%s" w="0" h="0" />
<title>%ds自动撤回</title><summary>检测中，%d自动撤回</summary></item><source name="" icon="%s/none" action="" appid="-1" /></msg>
        """% (waittime,ramdomUrl,waittime,waittime,ramdomUrl)
        CQcode = '[CQ:xml,data=%s]' % xml_msg
        self.id = self.send_back_msg(CQcode)
        #等待10s，撤回消息，发送检测结果
        self.local_ip = get_ip()
        asyncio.create_task(self.delay_callback(waittime,self.return_result))
        return False
        
                
    def get_ip_region(self,ip_address):
        res = ip_address[0:2] + (len(ip_address) - 6 ) * '*' + ip_address[-2:]
        if ":" in ip_address:
            ip_type = 6
        else:
            ip_type = 4
        if ip_type == 4:
            #url = 'http://opendata.baidu.com/api.php?query=%s&co=&resource_id=6006&oe=utf8' % ip_address
            return self.local_ip.get_ip(ip_address)
            
        else:
            url = 'http://ip-api.com/json/%s' % ip_address
        api = url
        res = requests.get(api)
        if res.status_code == 200:
            try:
                data =  json.loads(res.text)
                if ip_type == 6:
                    res = data["regionName"]+ data["regionName"] + data["city"]+ data["isp"]
                else:
                    res = data['data'][0]['location']
            except:
                res = ip_address[0:2] + (len(ip_address) - 6 ) * '*' + ip_address[-2:]
        return res
    
    def return_result(self):
        raw = False
        if 'rawip' in self.first_message['message']:
            raw = True
        buffer = '窥屏检测结果如下：\n'
        count = 0
        self.recall_msg(self.id)
        ips = set()
        res = requests.get('http://127.0.0.1:680/%s' % self.random_code)
        print(res.text)
        get_data = json.loads(res.text)
        if len(get_data) == 0:
            buffer = '没有群友在窥屏'
            self.send_back_msg(buffer)
            return False
        else:
            for data in get_data:
                if data['ip'] not in ips:
                    ips.add(data['ip'])
                    count += 1
                    if raw:
                        buffer += data['ip']
                    buffer += '来自 %s 的群友正在窥屏 \n' % self.get_ip_region(data['ip'])
          
        if count == 0:
            buffer = '没有群友在窥屏'
            self.send_back_msg(buffer)
        else:
            buffer += '共有 %d 个群友在窥屏' % count
            self.send_back_msg(buffer)
        self.local_ip.searcher.close()
        return False
        
        
    


            
        
        