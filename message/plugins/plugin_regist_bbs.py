import requests
from . import base_utility
import re
alia = ['注册']
help = {
    'brief_help' : '快速注册论坛账号',
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

        else:
            self.send_back_msg(res.text)
        
        
        