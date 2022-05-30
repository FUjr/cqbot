import json
class keng:
    def __init__(self,api_queue,api_res_queue,log_queue) -> None:
        self.api_queue  = api_queue
        self.api_res_queue = api_res_queue
        self.log_queue = log_queue

    def get_group_info(self):
        group_list_api = 'get_group_list'
        group_member_api = 'get_group_member_list'
        self.api_queue.put(group_list_api)
        group_list = json.loads(self.api_res_queue.get())['data']
        self.all_group_member_set = set() # 存储所有群成员
        self.group_member_dict = {}#存储每个群的成员
        self.group_info_index_by_id = {}
        self.member_info_index_by_id = {}
        self.same_group_dict = {}#储存每个成员所在的群列表
        for group_info in group_list:
            group_id = group_info['group_id']
            self.group_info_index_by_id[group_id] = group_info
            self.api_queue.put(group_member_api + '?group_id=' + str(group_id))
            group_member_list = json.loads(self.api_res_queue.get())['data']
            self.group_member_dict[group_id] = set()
            for member in group_member_list:
                member_id = member['user_id']
                self.member_info_index_by_id[member_id] = member
                self.group_member_dict[group_id].add(member_id)
                if member_id not in self.all_group_member_set:
                    self.all_group_member_set.add(member_id)
                else:
                    for key in self.group_member_dict:
                        if member_id in self.group_member_dict[key]:
                            if member_id not in self.same_group_dict:
                                self.same_group_dict[member_id] = [key]
                            if key not in self.same_group_dict[member_id]:
                                self.same_group_dict[member_id].append(key)
                

    def in_same_group_member(self,list1:list,list2:list) -> int:
        count = 0
        for key in self.same_group_dict:
            if self.bothin2list(self.same_group_dict[key],list1,list2):
                member_name = self.member_info_index_by_id[key]['nickname']
                group_name = []
                for group_id in self.same_group_dict[key]:
                    group_name.append(self.group_info_index_by_id[group_id]['group_name'])
                #self.log_queue.put([1,[member_name,key,group_name]])
                count = count + 1
        self.log_queue.put([1,"大雕一共割了%i个韭菜" %count])
        return count
    
    def bothin2list(self,list0,list1,list2):
        inlist1 = False
        inlist2 = False

        for i in list0:
            if i in list1:
                inlist1 = 1
            if i in list2:
                inlist2 = 1
        if inlist1 and inlist2:
            return True
        return False

    def notonlyin(self,list0,list1):
        inlist1 = False
        for i in list0:
            if i in list1:
                list0.remove(i)
                inlist1 = True
                break

        if len(list0) > 1 and inlist1:
            return True
        return False

    def run(self,data) -> object:
        message = '来看看大雕坑了多少人去付费群吧～'
        if data['message_type'] == 'private':
            user_id = data['user_id']
            api = "send_group_msg?user_id=" + str(user_id) +"&message="  + message
            self.api_queue.put(api)
            self.api_res_queue.get()
        elif data['message_type'] == 'group':
            count = 0
            group_id = data['group_id']
            api = "send_group_msg?group_id=" + str(group_id) +"&message="  + message
            self.log_queue.put([1,api])
            self.api_queue.put(api)
            self.api_res_queue.get()
            self.get_group_info()
            count = self.in_same_group_member([group_id],[942566374])
            count = str(count)
            self.log_queue.put([1,count])
            api = "send_group_msg?group_id=" + str(group_id) +"&message=大雕在本群一共割了"  + count + "颗韭菜"
            self.log_queue.put([1,api])
            self.api_queue.put(api)
            self.api_res_queue.get()
        return False

    