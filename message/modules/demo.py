import sys
permission = {"permission" : "all"}
class demo:
    
    def __init__(self,api_queue,api_res_queue,log_queue) -> None:
        self.log_queue = log_queue

    def run(self,msg) -> object:
        self.g = self.main()
        next(self.g)
        self.g.send(msg)
        return self

    def add(self,msg) -> None:
        try:
            self.g.send(msg)
        except StopIteration:
            return False
        return True

    def main(self) -> None:
        res = yield 1
        self.log_queue.put([2,res])
        res = yield 2
        self.log_queue.put([2,res])
        res = yield 3
        self.log_queue.put([2,res])
        