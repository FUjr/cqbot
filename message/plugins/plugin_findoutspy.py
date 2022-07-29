from __future__ import barry_as_FLUFL
import random

from numpy import mat
from . import base_utility
import asyncio
import time
import re
alia = ['谁是卧底']

permission = {
    'group' : [True,[]],
    'private' : [True,[]],
    'member_id' : {},
    'role' : 'member'
}
help = {
    'brief_help' : '谁是卧底',
    'more' : '谁是卧底',
    'alia' : alia
}


class plugin_findoutspy(base_utility.base_utility):
    def main(self) -> None:
        self.update_friend_list()
        self.trigger['message'] = ['加入']
#         self.send_back_msg("""欢迎使用谁是卧底
# 注意事项：
# 1、由于腾讯限制，请添加机器人好友，机器人才能给你发送你的身份
# 2、为了更好的体验，建议在机器人是管理员的群使用（防止插嘴）
# 3、发送"加入",即可加入 谁是卧底
# 4、游戏至少需要3人，至多可以10人，超过三人时，发起者发送“开始游戏”即可开启游戏
# 5、游戏准备期间，超过60s没有人加入，会自动开始游戏


# 游戏规则：
# 1、游戏规则就是谁是卧底的规则
# 2、如果机器人是管理员，会禁言参与者，按顺序解除禁言
# 3、如果机器人非管理员，会按顺序艾特参与者发言
# 4、如果违规发言3次会被踢出游戏
# 5、发言超时为60s，超时会轮到下一个人发言""")
        self.send_back_msg('欢迎使用谁是卧底，请添加机器人好友之后在群里发送“加入”。凑够3人以上发起者发送：开始游戏')
        initiator = self.first_message['user_id']
        self.member_list = [initiator]
        self.timeouter = 0
        
        
        
        
        #游戏准备环节,拉人
        while (len(self.member_list) < 10):
            asyncio.create_task(self.timeout_send(15,{'message':'开始游戏','user_id':initiator,'self_id':'timeout!'}))
            res = yield 1
            if res['user_id'] not in self.member_list:
                if res['user_id'] not in self.friend_list:
                    self.send_back_msg('请添加机器人好友之后再次发送“加入”')
                    self.update_friend_list()
                    continue
                self.trigger['account_id'].append(res['user_id'])
                self.member_list.append(res['user_id'])
                self.send_back_msg('欢迎加[CQ:at,qq=%s]入谁是卧底，目前已有%d人' % (res['user_id'],len(self.member_list)))
            elif res['message'] == '开始游戏':
                if res['user_id'] == initiator and len(self.member_list) > 2:
                    del self.trigger['message']
                    self.last_join = 0
                    break
                else:
                    if res['self_id'] == 'timeout!':
                        continue
                    self.send_back_msg('请凑满3人,由发起者发送开始游戏,才能开始')
                    
        #游戏开始环节，发送身份
        self.timeouter += 1
        print(self.timeouter)
        post_data = {
            'message':"",
            'user_id':"",
        }
        api = 'send_msg'
        id_list,spy_index = self.gen_identity_list()
        spy = self.member_list[spy_index]
        print(spy)
        for i in range(len(self.member_list)):
            post_data['message'] = '你的身份是%s' % id_list[i]
            post_data['user_id'] = self.member_list[i]
            self.query_api(api,post_data)
        self.send_back_msg('请各位查阅自己私聊的身份，组织一下语言。时间15秒钟')
        asyncio.create_task(self.timeout_send(15,'start_game'))
        while True:
            res = yield 1
            if res == 'start_game':
                break
        self.send_back_msg("""游戏正式开始！！！！请参与者尽量按照机器人艾特的顺序发言。""") 
        #游戏开始环节
        
        
        ban_dict = {}
        skip = []
        while (len(self.member_list) > 2 and spy in self.member_list):
            #陈述环节
            index = 0
            while (index < len(self.member_list)):
                index += 1
                
                if self.member_list[index-1] in skip:
                    skip.remove(self.member_list[index-1])
                    continue
                
                self.send_back_msg('请[CQ:at,qq=%s]发言，发言时间60秒钟' % self.member_list[index-1])
                self.timeouter += 1
                asyncio.create_task(self.timeout_send(60,'skip%s' % self.member_list[index-1]))
                res = yield 1
                if res == 'skip%s' % self.member_list[index-1]:
                    self.send_back_msg('[CQ:at,qq=%s]发言超时啦，自动跳过' % self.member_list[index-1])
                    continue
                if res['user_id'] != self.member_list[index-1]:
                    index = index - 1
                    if ban_dict.get(res['user_id']) is None:
                        ban_dict[res['user_id']] = 1
                    else:
                        ban_dict[res['user_id']] += 1
                    if ban_dict[res['user_id']] >= 3:
                        self.send_back_msg('[CQ:at,qq=%s] 三次在他人发言时间发言，被机器人投票出局啦~' % res['user_id'])
                        self.member_list.remove(res['user_id'])
                        self.trigger['account_id'].remove(res['user_id'])
                        continue
                    self.send_back_msg('[CQ:at,qq=%s]还不是你的发言时间哦，由于你已经发言，下次你的发言会被跳过。（%d/3)' % (res['user_id'],ban_dict[res['user_id']]))
                    skip.append(res['user_id'])

            #投票环节
            self.send_back_msg('请30秒内投票，@你认为的卧底，否则会计算弃票')
            vote_result = {}
            had_vote = set()
            asyncio.create_task(self.timeout_send(30,'break'))
            while (len(had_vote) < len(self.member_list)):
                res = yield 1
                if res == 'break':
                    break
                if res['user_id'] in had_vote:
                    self.send_back_msg('你已经投过票了，请不要重复投票')
                    continue
                else:
                    rex = r'qq=(\d+)'
                    match = re.findall(rex,res['message'])
                    if len(match) == 0:
                        continue
                    elif int(match[0]) not in self.member_list:
                        print(self.member_list)
                        self.send_back_msg('请艾特游戏内成员')
                    else:
                        had_vote.add(res['user_id'])
                        if vote_result.get(int(match[0])) is None:
                            vote_result[int(match[0])] = 1
                        else:
                            vote_result[int(match[0])] += 1
                             
            self.timeouter += 1
            #结果环节
            max_vote = 0
            max_list = []
            for key in vote_result:
                if vote_result[key] > max_vote:
                    max_list = [key]
                    max_vote = vote_result[key]
                elif vote_result[key] == max_vote:
                    max_list.append(key)
            if len(max_list) == 1:
                self.member_list.remove(max_list[0])
                self.trigger['account_id'].remove(max_list[0])
                self.send_back_msg('[CQ:at,qq=%s]被投票出局' % max_list[0])
                if spy not in self.member_list:
                    break
            elif len(max_list) == 0:
                self.send_back_msg('超过30秒没有人投票，退出游戏')
            elif len(max_list) > 1:
                same = ''
                for i in self.member_list:
                    skip.append(i)
                for i in max_list:
                    print(skip)
                    skip.remove(i)
                    same += ('[CQ:at,qq=%s]' % i)
                self.send_back_msg('出现同票，%s重新陈述' % same) 
                continue
            
        if spy in self.member_list:
            self.send_back_msg('卧底成功')
        else:
            self.send_back_msg('卧底失败')

            
    def gen_identity_list(self):
        word_list = [['老婆','女朋友'],["汤圆","丸子"],["哈密瓜","西瓜"],["包子","水饺"],["汉堡包","肉夹馍"],["宫锁心玉","宫锁珠帘"],["步步惊心","宫锁心玉"],["钢笔","中性笔"],["玫瑰","月季"],["董永","许仙"],["若曦","晴川"],["谢娜","李湘"],["孟非","乐嘉"],["牛奶","豆浆"],["保安","保镖"],["白菜","生菜"],["辣椒","芥末"],["赵敏","黄蓉"],["海豚","海狮"],["水盆","水桶"],["唇膏","口红"],["小笼包","灌汤包"],["薰衣草","满天星"],["富二代","高富帅"]]
        length = len(self.member_list)
        wordlist_index = random.randint(0,len(word_list)-1)
        random_common = random.randint(0,len(word_list[wordlist_index])-1)
        random_spy = random.randint(0,len(word_list[wordlist_index])-1)
        while random_common == random_spy:
            random_spy = random.randint(0,len(word_list[wordlist_index])-1)
        common_word = word_list[wordlist_index][random_common]
        spy_word = word_list[wordlist_index][random_spy]
        random_spy_index = random.randint(0,length-1)
        id_list = [common_word] * length
        id_list[random_spy_index] = spy_word
        return id_list,random_spy_index
    
    def update_friend_list(self):
        friend_list_api = 'get_friend_list'
        res = self.query_api(friend_list_api,{})
        self.friend_list = []
        for i in res['data']:
            self.friend_list.append(i['user_id'])
    
    async def timeout_send(self,timeout,send_data):
        self.timeouter += 1
        this_timeouter = self.timeouter
        print(self.timeouter)
        print(this_timeouter)
        await asyncio.sleep(timeout)
        

        if self.timeouter == this_timeouter:
            print('已跳过，发送了%s' % send_data)
            try:
                self.g.send(send_data)
            except Exception as e:
                print(e)
        print('失效了%s' % send_data)
        
        
                