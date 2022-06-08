import requests
for i in range(43):
    password = '123456'
    username = 'test' + str(i)
    mail = username + '@qq.com'
    api_token = 'fjrfjrfjr'
    data = {
                'api_token' : api_token,
                'passwd' : password,
                'user' : username,
                'mail' : mail
            }
    api = 'http://192.168.3.5:88/?api/add.html'
    res = requests.post(api,data=data)
    print(res)