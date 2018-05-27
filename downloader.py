import threading
import time
import requests


class Downloader(threading.Thread):
    def __init__(self, threadID, name, stopper, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stopper = stopper
        self.q = q

    def download(self, url, post_id, gender):
        url = url
        img_data = requests.get(url).content
        with open('images/{}/{}.jpg'.format(gender, post_id), 'wb') as handler:
            handler.write(img_data)

    def run(self):
        while not self.stopper.is_set():
            item = self.q.get()
            if item is None:
                time.sleep(1)
            else:
                print(item)
                self.download(item['url'], item['id'], item['gender'])
                self.q.task_done()
            if self.stopper.is_set():
                print('download stopped')
                q.join()
                break
