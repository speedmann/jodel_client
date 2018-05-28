import json
import requests

def api_get_post(id):
    url = 'http://localhost:5000/api/posts/{}'.format(id)
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return False

def api_get_comment(id):
    url = 'http://localhost:5000/api/comments/{}'.format(id)
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return False

def api_create_post(id, text, gender):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = {"id":id,"text":text, "gender":gender}
    url = 'http://localhost:5000/api/posts'
    r = requests.post(url, data=json.dumps(data) , headers=headers)

def api_create_comment(post_id, comment_id, text, gender):
    posts = api_get_post(post_id)
    comment = api_get_comment(comment_id)
    if posts and not comment:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = {"id":comment_id, "text":text, "post_id":post_id, "gender":gender}
        url = 'http://localhost:5000/api/comments'
        r = requests.post(url, data=json.dumps(data),headers=headers)