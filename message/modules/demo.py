import sys
alia = ['demo']

permission = {
    'group' : [True,[]],
    'private' : [True,[]],
    'member_id' : {},
    'role' : ''
}
help = {
    'brief_help' : '这是我用来测试的，无意义',
    'more' : '这是我用来测试的，无意义',
    'alia' : alia
}

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
        