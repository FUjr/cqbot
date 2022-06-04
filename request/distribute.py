from  . import request_type
import sys
class distribute:
    def __init__(self,api_queue,api_res,log_queue) -> None:
        self.request_type_list = request_type.request_type_list
        self.api_queue = api_queue
        self.api_res = api_res
        self.log_queue =log_queue

    def distribute(self,data:dict) -> None:
        if data['request_type'] in self.request_type_list:
            __import__(__name__.replace(__class__.__name__,'request_type.') + data['request_type'])
            handler = getattr(sys.modules[__name__.replace(__class__.__name__,'request_type.') + data['request_type']],data['request_type'])(self.api_queue,self.api_res,self.log_queue)
            handler.do(data)
        else:
            pass
    
