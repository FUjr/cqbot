from importlib.metadata import distribution
from . import cqcode
import re
import sys

class load_cqcode():
    def __init__(self, api_queue, api_res_queue, log_queue,content_livetime: int = 300):
        self.content_livetime = content_livetime
        self.api_queue = api_queue
        self.api_res_queue  = api_res_queue
        self.log_queue = log_queue
        self.content = False
        
    def distribute_cqcode(self,data):
        rex = r'\[CQ:(.*?),.*?\]'
        cqcode_list = re.findall(rex,data['message'])
        #请注意，如果没有做防止重复处理，每次都返回不一样的值，会导致死循环
        for i in cqcode_list:
            data = self.handle_cqcode(i,data)
        return data
        
    def handle_cqcode(self,cqcode_type,data):
        if cqcode_type in list(cqcode.cqcode_dict.keys()):
            #若在字典内，尝试导入模块
            module_name = __name__.replace(__class__.__name__,'cqcode.') + cqcode.cqcode_dict[cqcode_type]
            __import__(module_name)
            handler = getattr(sys.modules[__name__.replace(__class__.__name__,'cqcode.') + cqcode.cqcode_dict[cqcode_type]], cqcode.cqcode_dict[cqcode_type])(data,self.api_queue,self.api_res_queue,self.log_queue)
            self.log_queue.put([1,'loaded: ' + cqcode.cqcode_dict[cqcode_type]])
            data = handler.run(data)
        return data