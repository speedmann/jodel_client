import threading
import time
from db import Posts
from db import JodelDB
import requests
import json
from api import api_get_post, api_create_post

import datetime
from worker import download, monitor_post

class Post_overview(threading.Thread):
    def __init__(self, threadID, name, stopper, q, post_q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stopper = stopper
        self.q = q
        self.post_q = post_q
        self.db = JodelDB()

    def run(self):
        format = '%Y-%m-%dT%H:%M:%S.%fZ'
        sleep_time = 5
        while not self.stopper.is_set():
            posts = self.get_posts()
            try:
                for post in posts['results']['jodels']:
                    if api_get_post(post['id']):
                        pass
                    else:
                        data = {"id":post['id'],"text":post['text']}
                        api_create_post(post['id'], post['text'], post['author']['gender_id'], post['image'], post['timestamp'])
     
                        if post['image'] is not '':
                            self.q.enqueue(download, post['image'], post['id'], post['author']['gender_id'])
                        #self.post_q.put({'id': post['id'], 'sleep_time' : 10 })
                        self.post_q.enqueue(monitor_post, post['id'], time.time()+10, 10)
            except KeyError:
                print(posts)
                #print('{} sleeping for {} seconds'.format(self.channel, sleep_time))
            for i in range(sleep_time):
                if self.stopper.is_set():
                    print('channel exit')
                    break
                else:
                    time.sleep(1)

    def get_posts(self):
        url = "https://secretgermanjodel.com/api/jodels/get"
        jar = requests.cookies.RequestsCookieJar()
        jar.set('SGJ_TOKEN', '22481-f172ff0e3b4baf76dc94d0f0fe03a517d84e18c1c2007c68a9b66a2986fe4bb7dbbc6f46', domain="secretgermanjodel.com")
        r = requests.post(url, cookies=jar, data= {'sort':0,'amount_loaded':0})
        r.encoding = "utf-8-sig"
        return json.loads(r.text)
