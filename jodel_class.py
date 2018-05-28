import threading
import time
import jodel_api
import datetime
from signal_handler import SignalHandler
from post_overview import Post_overview
from post_detail import Post_detail
from downloader import Downloader
import signal
from db import Posts


from rq import Queue
from redis import Redis


class Jodel():
    def __init__(self,):
        self.jodel = None
        self.stopper = None
        self.threads = None
        self.redis_conn = Redis(host='54.37.220.228')
        self.q = Queue('download', connection=self.redis_conn)
        self.post_q = Queue('posts', connection=self.redis_conn)

    def start(self):
        self.stopper = threading.Event()
        self.threads = []
        handler = SignalHandler(self.stopper, self.threads)



        #downloader = Downloader(1, 'main', self.stopper, self.q)
        thread = Post_overview(1, 'main', self.stopper, self.q, self.post_q)
        #for i in range(1,40):
        #    post_detail = Post_detail(i, 'main', self.stopper, self.q, self.post_q)
        #    self.threads.append(post_detail)
        self.threads.append(thread)
        #self.threads.append(downloader)

        signal.signal(signal.SIGINT, handler)

        for t in self.threads:
            t.start()

        for t in self.threads:
            t.join()
