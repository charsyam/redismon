from multiprocessing import Process


class AsyncJob:
    def __init__(self, cmd, queue, args):
        self.cmd = cmd
        self.args = args
        self.queue = queue

    def start(self):
        self.p = Process(target=self.cmd, args=(self.queue, self.args))
        self.p.start()
        self.p.join()

    def get(self):
        try:
            v = self.queue.get(False)
        except:
            v = None

        print("get: ", v)
        return v

    def join(self):
        self.p.join() 
