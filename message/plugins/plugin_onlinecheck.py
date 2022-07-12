from ipaddress import ip_address
import requests
from . import base_utility
import time
import __main__
import json
alia = ['窥屏检测','在线监测']

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
        start = time.time()
        #创建一个简易http服务器线程，通过管道通信
        pipe = __main__.online_queue
        
        #发送一条包含xml的消息
        url = 'https://tmpporxy.fjrcn.cn/'
        random_code = ''.join(str(time.time()).split('.'))
        ramdomUrl = url + random_code
        print(ramdomUrl)
        xml_msg = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<msg serviceID="1">
<item><title>窥屏检测 10s后撤回</title></item>
<source name="窥屏检测 10s后撤回" icon="%s" action="" appid="-1" />
</msg>
        """% ramdomUrl
        CQcode = '[CQ:xml,data=%s]' % xml_msg
        id = self.send_back_msg(CQcode)
        buffer = '窥屏检测结果如下：\n'
        #等待10s，退出线程并撤回消息，发送检测结果
        time.sleep(10)
        self.recall_msg(id)
        while (not pipe.empty()):
            data = pipe.get()
            if data['path'] == '/' + random_code:
                res = self.get_ip_region(data['ip'])
                if res['status'] == '0':
                    region = res['data'][0]['location']
                    buffer += '来自 %s' %  region +  '\n'
                else:
                    buffer += 'ip %s' % data['ip']
            else:
                if time.time() - data['time'] < 30:
                    pipe.put(data)
        self.send_back_msg(buffer)
        return False
                
    def get_ip_region(self,ip_address):
        api = 'http://opendata.baidu.com/api.php?query=%s&co=&resource_id=6006&oe=utf8' %ip_address
        res = requests.get(api)
        return json.loads(res.text)
            
        
        