class offline_file:
    def __init__(self,api_queue,api_res,log_queue):
        self.api_queue = api_queue
        self.api_res = api_res
        self.log_queue =log_queue

    def do(self,data):
        print('recived file')
        self.log_queue.put([1,data])
        user_id =  data['user_id']
        file_name = data['file']['name']
        file_url = data['file']['url']
        self.log_queue.put([1,file_url])

