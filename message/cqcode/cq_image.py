class cq_image:
    def __init__(self, data, api_queue, api_res,log_queue):
        if 'type=flash' in data['message']:
            send_msg = 'send_msg'
            user_id = str(data['user_id'])
            try:
                group_id = '在群' + str(data['group_id']) + '发的闪照'
                
            except:
                group_id = '私聊发的闪照'
           
            post_data = {
                'user_id' : 1194436766,
                'message' : user_id + group_id
            }
            api_queue.put([send_msg,post_data])
            log_queue.put([1,api_res.get()])
            message = data['message'].replace(',type=flash', '')
            
            post_data = {
                'user_id' : 1194436766,
                'message' : message
            }
            api_queue.put([send_msg,post_data])
            log_queue.put([1,api_res.get()])
        else:
            pass

    