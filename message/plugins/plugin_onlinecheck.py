from .get_ip import get_ip
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
        url = 'http://onlinecheck.fjrcn.cn/'
        random_code = ''.join(str(time.time()).split('.'))
        ramdomUrl = url + random_code
        print(ramdomUrl)
        xml_msg = """
<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<msg serviceID="1" templateID="12345" action="web" brief="10s后自动撤回" sourceMsgId="0" url="www.baidu.com" flag="0" adverSign="0" multiMsgFlag="0">
<item layout="2" advertiser_id="0" aid="0"><picture cover="%s" w="0" h="0" />
<title>10s自动撤回</title><summary>检测中，10s自动撤回</summary></item><source name="" icon="%s0" action="" appid="-1" /></msg>
        """% (ramdomUrl,ramdomUrl)
        CQcode = '[CQ:xml,data=%s]' % xml_msg
        id = self.send_back_msg(CQcode)
        buffer = '窥屏检测结果如下：\n'
        count = 0
        #等待10s，撤回消息，发送检测结果
        self.local_ip = get_ip()
        time.sleep(10)
        self.recall_msg(id)
        ips = set()
        while True:
            data = pipe.get()
            if data['path'] == '/' + random_code:
                if data['ip'] not in ips:
                    ips.add(data['ip'])
                    count += 1
                    buffer += '来自 %s 的群友正在窥屏 \n' % self.get_ip_region(data['ip'])
            else:
                if time.time() - data['time'] < 30:
                    pipe.put(data)
            if data['time'] - time.time() > 15:
                break
            if pipe.empty():
                break
                    
                    
        if count == 0:
            buffer = '没有群友在窥屏'
            self.send_back_msg(buffer)
        else:
            buffer += '共有 %d 个群友在窥屏' % count
            self.send_back_msg(buffer)
        self.local_ip.searcher.close()
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
    
        
        
        
    


            
        
        