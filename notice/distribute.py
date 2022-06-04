from  . import events
import sys
class distribute:
    def __init__(self,api_queue,api_res,log_queue) -> None:
        self.event_list = events.events_list
        self.api_queue = api_queue
        self.api_res = api_res
        self.log_queue =log_queue

    def distribute(self,data:dict) -> None:
        if data['notice_type'] in self.event_list:
            __import__('notice.events.'+ data['notice_type'] )
            handler = getattr(sys.modules['notice.events.' + data['notice_type']],data['notice_type'])(self.api_queue,self.api_res,self.log_queue)
            handler.do(data)
        else:
            pass
    
