import requests
from . import base_utility
import re
import os
alia = ['注册','注销账号']
help = {
    'brief_help' : '快速注册/删除论坛账号',
    'more' : '快速注册，会使用你的qq邮箱作为安全邮箱，只需要输入账号密码就可以快速注册',
    'alia' : alia
}
permission = {
    'group' : [False,['796777269','901798776','733051338','']],
    'private' : [True,[]],
    'member_id' : {13:14},
    'role' : ''
}
class plugin_regist_bbs(base_utility.base_utility):
    api_token = 'fjrfjrfjr'
    header = { 'api_token' : api_token}
    api_address = 'http://192.168.3.5:88/?api/'
    def main(self) -> None:
        if self.first_message['message'] == '注册':
            self.send_back_msg('快速注册论坛账号\n如果未指定用户名，将会用你的qq号作为用户名，如果需要制定用户名，请以 username password 的格式发送\n及空格前是用户名，空格后是密码。密码需要大于5位')
            res = yield 1
            if len(res['message'].split(' ')) == 2:
                #第一项为账号，第二项为密码
                username = res['message'].split(' ')[0]
                password = res['message'].split(' ')[1]
                #发送确认信息
            elif  len(res['message'].split(' ')) == 1:
                password = res['message'].split(' ')[0]
                username = res['sender']['nickname']
            mail_id = str(res['user_id']) +  '@qq.com'
            self.send_back_msg('请确认，你的账号是%s 密码是 %s.回复 确认 以外的信息都会终止执行' %(username,password))
            res = yield 2
            if res['message'] != '确认':
                self.send_back_msg('已退出')
                return False

            data = {
                    'api_token' : self.api_token,
                    'passwd' : password,
                    'user' : username,
                    'mail' : mail_id
                }
            res = requests.post(self.api_address + 'add.html',data=data)
            print(res.status_code)
            rex = r'(\d{3,})'
            message = res.text
            print(message)
            if re.match(rex,message):
                self.send_back_msg('注册成功，如果忘记密码，请用你的qq邮箱找回。现在可以尝试登陆了')
                self.set_ava()
            else:
                self.send_back_msg(res.text)
        elif self.first_message['message'] == '注销账号':
            self.send_back_msg('确认删除账号吗？此操作无法撤销！回复 确认 以外的都会中止注销')
            res = yield 1
            if res['message'] != '确认':  
                email = str(self.first_message['user_id']) + '@qq.com'
                data = {
                    'api_token' : self.api_token,
                    'mail' : email
                }
                delete_user_api = 'http://192.168.3.5:88/?api/delete_user.html'
                res= requests.post(delete_user_api,data=data)
                if res.text == 1:
                    self.send_back_msg('已删除账号')
                else:
                    self.send_back_msg('删除请求非法，可能是未注册或者已删除')
            else:
                self.send_back_msg('已中止注销')
        
        
    def set_ava(self) -> None:
        self.get_ava()
        set_ava_api = 'http://192.168.3.5:88/?api/ava.html'
        data = {
            'api_token' : self.api_token,
            'uid' : self.get_uid(self.first_message['user_id'])
        }
        res = requests.post(set_ava_api,data=data,files={'file':open(self.save_path,'rb')})
        print(res.text)
    
    def get_ava(self) -> None:
        if not os.path.exists('ava'):
            os.mkdir('ava')
        ava_api = 'http://q1.qlogo.cn/g?b=qq&s=640&nk=' + str(self.first_message['user_id'])
        self.save_path = 'ava' + os.sep + str(self.first_message['user_id']) + '.jpg'
        res = requests.get(ava_api)
        with open(self.save_path,'wb') as f:
            f.write(res.content)
            
    def get_uid(self,user_id) -> int:
        email = str(user_id) + '@qq.com'
        get_uid_api = 'http://192.168.3.5:88/?api/get_uid.html'
        data = {
            'api_token' : self.api_token,
            'mail' : email
        }
        res = requests.post(get_uid_api,data=data)
        return int(res.text)
    