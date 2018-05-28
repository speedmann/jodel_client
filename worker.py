import requests
import os.path
import requests
from rq import Queue
from redis import Redis
import time
import json
from api import api_create_comment

def download(url, post_id, gender):
    url = url
    name = url.split('/')[-1]
    if not os.path.isfile('/var/www/html/images/{}/{}.jpg'.format(gender, post_id)):
        img_data = requests.get(url).content
        with open('images/{}/{}'.format(gender, name), 'wb') as handler:
            handler.write(img_data)
        return True
    return False


def monitor_post(id, next_check, last_sleep):
    redis_conn = Redis(host='54.37.220.228')
    q = Queue('download', connection=redis_conn)
    post_q = Queue('posts', connection=redis_conn)
    if next_check < time.time():
        post = get_post(id)
        for comment in post['results']['comments']:
            api_create_comment(id, comment['id'], comment['text'], comment['author']['gender_id'])
            if comment['image'] is not '':
                q.enqueue(download, comment['image'], comment['id'], comment['author']['gender_id'])
        post_q.enqueue(monitor_post, id, time.time()+last_sleep+10, last_sleep+10)
    else:
        post_q.enqueue(monitor_post, id, next_check, last_sleep)

def get_post(id):
    url = "https://secretgermanjodel.com/api/comments/get"
    jar = requests.cookies.RequestsCookieJar()
    jar.set('SGJ_TOKEN', '22481-f172ff0e3b4baf76dc94d0f0fe03a517d84e18c1c2007c68a9b66a2986fe4bb7dbbc6f46', domain="secretgermanjodel.com")
    data = {'id':id, 'direction':1,'last_id':0,'comment_id':0, 'jodel_needed':1,'notification_id':0,'special':0}
    r = requests.post(url, cookies=jar, data=data )
    r.encoding = "utf-8-sig"
    return json.loads(r.text)
