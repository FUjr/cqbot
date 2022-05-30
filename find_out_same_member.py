import requests
import json

baseurl = 'http://192.168.3.5:678/'

group_list_api = baseurl + 'get_group_list'

group_member_api = baseurl + 'get_group_member_list'

group_list = json.loads(requests.get(group_list_api).text)['data']

all_group_member_set = set() # 存储所有群成员

group_member_dict = {}#存储每个群的成员

group_info_index_by_id = {}

member_info_index_by_id = {}

same_group_dict = {}#储存每个成员所在的群列表
for group_info in group_list:
    
    group_id = group_info['group_id']
    group_info_index_by_id[group_id] = group_info
    group_member_list = json.loads(requests.get(group_member_api + '?group_id=' + str(group_id)).text)['data']
    group_member_dict[group_id] = set()
    for member in group_member_list:
        member_id = member['user_id']
        member_info_index_by_id[member_id] = member
        group_member_dict[group_id].add(member_id)
        if member_id not in all_group_member_set:
            all_group_member_set.add(member_id)
        else:
            for key in group_member_dict:
                if member_id in group_member_dict[key]:
                    if member_id not in same_group_dict:
                        same_group_dict[member_id] = [key]
                    if key not in same_group_dict[member_id]:
                        same_group_dict[member_id].append(key)
                    
count = 0    
list1 = [108385127,574371223]
list2 = [942566374]
def bothin2list(list0,list1,list2):
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

def notonlyin(list0,list1):
    inlist1 = False
    for i in list0:
        if i in list1:
            list0.remove(i)
            inlist1 = True
            break

    if len(list0) > 1 and inlist1:
        return True
    return False


for key in same_group_dict:
    if bothin2list(same_group_dict[key],list1,list2):
        member_name = member_info_index_by_id[key]['nickname']
        group_name = []
        for group_id in same_group_dict[key]:
            group_name.append(group_info_index_by_id[group_id]['group_name'])
        print(member_name,key, group_name)
        count = count + 1
print("大雕一共割了%i个韭菜" %count)

