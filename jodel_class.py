import threading
import time
import jodel_api
import datetime
from signal_handler import SignalHandler
from post_overview import Post_overview
from downloader import Downloader
import signal
import queue
from db import Posts


class Jodel():
    def __init__(self,):
        self.jodel = None
        self.stopper = None
        self.threads = None
        self.q = queue.Queue()

    def start(self):
        self.stopper = threading.Event()
        self.threads = []
        handler = SignalHandler(self.stopper, self.threads)

        downloader = Downloader(1, 'main', self.stopper, self.q)
        thread = Post_overview(1, 'main', self.stopper, self.q)
        self.threads.append(thread)
        self.threads.append(downloader)

        signal.signal(signal.SIGINT, handler)

        for t in self.threads:
            t.start()

        for t in self.threads:
            t.join()
