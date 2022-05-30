from tokenize import group


class cq_image:
    def __init__(self, data, api_queue, api_res,log_queue):
        if 'type=flash' in data['message']:
            print(data)
            
            user_id = str(data['user_id'])
            
            
            try:
                group_id = '在群' + str(data['group_id']) + '发的闪照'
                
            except:
                group_id = '私聊发的闪照'
           
            api_queue.put('send_msg?user_id=' + str(1194436766) + '&message=' + user_id + group_id)
            log_queue.put([1,api_res.get()])
            message = data['message'].replace(',type=flash', '')
            api_queue.put('send_msg?user_id=' + str(1194436766) + '&message=' + message)
            log_queue.put([1,api_res.get()])
        else:
            pass

    