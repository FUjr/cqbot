import requests
import json

baseurl = 'http://192.168.3.5:678/'

group_list_api = baseurl + 'get_group_list'

group_member_api = baseurl + 'get_group_member_list'

group_list = json.loads(requests.get(group_list_api).text)['data']

group_data_dict = {}
for group_info in group_list:
    
    group_id = group_info['group_id']

    group_member_list = json.loads(requests.get(group_member_api + '?group_id=' + str(group_id)).text)['data']

    group_data = {
        'group_name' : group_info['group_name'],
        'unfriendly_list': [],
        'male_list': [],
        'female_list': [],
        'shut_up_list': []

    }
    for member_info in group_member_list:
        member_id = member_info['user_id']
        nickname = member_info['nickname']
        if member_info['unfriendly'] == True:
            group_data['unfriendly_list'].append((member_id,nickname))
        if member_info['sex'] == 'female':
            group_data['female_list'].append((member_id,nickname))
        if member_info['sex'] == 'male':
            group_data['male_list'].append((member_id,nickname))
        if member_info['shut_up_timestamp'] > 0:
            group_data['shut_up_list'].append((member_id,nickname,member_info['shut_up_timestamp']))
    
    group_data_dict[group_id] = group_data

for key in group_data_dict:
    unfriendly_num = len(group_data_dict[key]['unfriendly_list'])
    male_num = len(group_data_dict[key]['male_list'])
    female_num = len(group_data_dict[key]['female_list'])
    shut_up_num = len(group_data_dict[key]['shut_up_list'])
    print(group_data_dict[key]['group_name'])
    print(unfriendly_num,male_num,female_num,shut_up_num)
