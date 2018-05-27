import threading
import time
from db import Posts
from db import JodelDB
import requests
import json

import datetime


class Post_detail(threading.Thread):
    def __init__(self, threadID, name, stopper, q, post_q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stopper = stopper
        self.post_q = post_q
        self.q = q
        self.db = JodelDB()

    def run(self):
        format = '%Y-%m-%dT%H:%M:%S.%fZ'
        sleep_time = 5
        while not self.stopper.is_set():
            item = self.post_q.get()
            if item is None:
                time.sleep(1)
            else:
                post = self.get_post(item['id'])
                try:
                    for comment in post['results']['comments']:
                        if comment['image'] is not '':
                            self.q.put({'url': comment['image'],
                                        'id': '{}_{}'.format(item['id'], comment['id']), 'gender' : comment['author']['gender_id']})
                    self.post_q.task_done()
                    print('sleep for {} {}'.format(item['id'], item['sleep_time']))
                    time.sleep(item['sleep_time'])
                    if item['sleep_time'] < 300:
                        self.post_q.put({'id':item['id'], 'sleep_time':item['sleep_time']+1})
                except TypeError:
                    print('{} failed'.format(item))

    def get_post(self,id):
        url = "https://secretgermanjodel.com/api/comments/get"
        jar = requests.cookies.RequestsCookieJar()
        jar.set('SGJ_TOKEN', '22481-f172ff0e3b4baf76dc94d0f0fe03a517d84e18c1c2007c68a9b66a2986fe4bb7dbbc6f46', domain="secretgermanjodel.com")
        data = {'id':id, 'direction':1,'last_id':0,'comment_id':0, 'jodel_needed':1,'notification_id':0,'special':0}
        r = requests.post(url, cookies=jar, data=data )
        r.encoding = "utf-8-sig"
        return json.loads(r.text)
