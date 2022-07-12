import re
class cq_xml:
    def __init__(self, data, api_queue, api_res,log_queue):
        self.api_queue = api_queue
        self.api_res = api_res
        self.log_queue = log_queue
        self.content_livetime = 300
        
    def run(self,data):
        print(data)
        return data