class low_level_plugin:
    def __init__(self,api_queue,api_res_queue,log_queue) -> None:
        self.api_queue =api_queue
        self.api_res_queue = api_res_queue
        self.log_queue = log_queue
    
    def run(self,data):
        #如果返回False则继续往下执行，返回True则结束
        self.log_queue.put([0,data])
        return False