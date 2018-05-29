import json
import requests
import datetime

def api_get_post(id):
    url = 'http://jodel1.tuxcall.de:5000/api/posts/{}'.format(id)
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return False

def api_get_comment(id):
    url = 'http://jodel1.tuxcall.de:5000/api/comments/{}'.format(id)
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return False

def api_create_post(id, text, gender, image, timestamp):
    if timestamp == '':
        api_create_post(id, text, gender, image)
    else:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        if not image == '':
            image = "/images/{}/{}".format(gender, image.split('/')[-1])
        data = {"id":id,"text":text, "gender":gender , "image": image, "timestamp" : str(datetime.datetime.fromtimestamp(int(timestamp)))}
        url = 'http://jodel1.tuxcall.de:5000/api/posts'
        r = requests.post(url, data=json.dumps(data) , headers=headers) 


def api_create_comment(post_id, comment_id, text, gender, image, timestamp):
    posts = api_get_post(post_id)
    comment = api_get_comment(comment_id)
    if posts and not comment:
        if not image == '':
            image = "/images/{}/{}".format(gender, image.split('/')[-1])
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = {"id":comment_id, "text":text, "post_id":post_id, "gender":gender, "image": image, "timestamp" : str(datetime.datetime.fromtimestamp(int(timestamp)))}
        url = 'http://jodel1.tuxcall.de:5000/api/comments'
        r = requests.post(url, data=json.dumps(data),headers=headers)


api_create_post(123, 'test',1,'','1527594085')
