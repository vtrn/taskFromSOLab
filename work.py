import threading
import uuid
from collections import Counter
from urllib.request import urlopen
import time
from lxml import html


class Task:
    def __init__(self, url):
        self.task_uuid = self.get_uuid()
        self.url = url
        self.status = 'queue'
        self.result = ''

    def get_uuid(self):
        return uuid.uuid4().hex

    def set_status(self, status):
        self.status = status

    def get_result(self):
        if self.url:
            self.set_status('running')
            try:
                page = urlopen(self.url).read()
                tree = html.fromstring(page)
                elements = tree.cssselect('*')
                tags = [_.tag for _ in elements]
                counter = Counter(tags)
                self.set_status('done')
                self.result = dict(counter)
            except AttributeError as e:
                self.result = str(e)
                self.set_status('error')

class Dispatcher:
    def __init__(self):
        self.tasks = {}
        self.queue = []
        for i in range(2):
            threading.Thread(
                name = "Worker #" + str(i),
                target=self.produce,
                args=()
            ).start()

    def create_task(self, url):
        print('push new task')
        task = Task(url)
        self.tasks[task.task_uuid] = task
        self.queue.append(task.task_uuid)
        return task.task_uuid


    def produce(self):
        while True:
            try:
                uuid = self.queue.pop(0)
                task = self.tasks[uuid]
                task.get_result()
                print("[{}] {} is done".format(threading.current_thread().name, uuid))
            except IndexError:
                time.sleep(.100)

