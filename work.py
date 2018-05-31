import hashlib
import random
import time
from collections import Counter
from urllib.request import urlopen

from lxml import html


class Task:
    def __init__(self, url):
        self.uuid = self.get_uuid()
        self.url = url
        self.status = 'queue'
        self.result = ''

    def get_uuid(self):
        abc = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
        secret_key = []
        for x in range(5):
            k = random.choice(abc.split())
            secret_key.append(k)
        h = hashlib.blake2b(digest_size=5)
        secret_key = ''.join(secret_key)
        h.update(secret_key.encode())
        uuid = h.hexdigest()
        return uuid

    def get_status(self, status):
        self.status = status

    def get_result(self):
        if self.url:
            self.get_status('running')
            try:
                page = urlopen(self.url).read()
                tree = html.fromstring(page)
                elements = tree.cssselect('*')
                tags = [_.tag for _ in elements]
                counter = Counter(tags)
                self.get_status('done')
                self.result = dict(counter)
            except:
                self.result = ''
                self.get_status('error')

    def get_data(self):
        data = {
            'task_uuid':
                {
                    self.uuid:
                        {
                            'status': self.status,
                            'result': self.result
                        }
                }
        }

        return data


class Dispatcher:
    def __init__(self):
        self.queue_url = []
        self.work_queue = []
        self.done_work = []

    def push(self, url):
        self.queue_url.append(url)

    def create_task(self):
        current_url = self.queue_url.pop(0)
        worker = Task(current_url)
        self.work_queue.append(worker)

    def produce(self):
        if len(self.work_queue) > 0:
            print('the work done')
            worker = self.work_queue.pop(0)
            worker.get_result()
            done = worker.get_data()
            self.done_work.append(done)



