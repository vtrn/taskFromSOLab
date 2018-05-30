import urllib.request
from lxml import html
from collections import Counter


class Cell:
    def __init__(self, url, uuid):
        self.url = url
        self.result = None
        self.uuid = uuid
        self.status = 'queue'

    def get_result(self):
        self.status = 'running'
        try:
            page = urllib.request.urlopen(self.url).read()
            tree = html.fromstring(page)
            elements = tree.cssselect('*')
            tags = [_.tag for _ in elements]
            counter = Counter(tags)
            self.result = counter
            self.status = 'done'
        except:
            self.status = 'error'

    def get_json(self):
        d = {
            'uuid': self.uuid,
            'status': self.status,
            'result': self.result
        }

        return d


class Dispacher:
    def __init__(self):
        self.tasks = []
        self.queue = []
        self.count = 1
        self.index = 0
    def create_task(self):
        task = self.queue[self.index][self.count]
        self.count += 1
        self.index += 1
        task.get_result()
        d = {'id': self.count, 'task': {'status': task.status, 'result': task.result}}
        self.tasks.append(d)
        return len(self.tasks)

    def hadle(self):
        while True:
            if len(self.queue) > 1:
                self.create_task()
            else:
                continue
#d = Dispacher()
#d.queue.append({0:Cell('https://www.lenta.ru', 0)})
#print(d.queue[0][0], d.tasks)
