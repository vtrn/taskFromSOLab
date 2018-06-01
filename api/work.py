from collections import Counter
from urllib.request import urlopen

from lxml import html


def get_result(url):
    if url:
        task = Task()
        task.status = 'running'
        try:
            page = urlopen(url).read()
            tree = html.fromstring(page)
            elements = tree.cssselect('*')
            tags = [_.tag for _ in elements]
            counter = Counter(tags)
            task.status = 'done'
            task.result = dict(counter)
        except AttributeError as e:
            task.result = str(e)
            task.status = 'error'
        return task


class Task:
    def __init__(self):
        self.status = 'queue'
        self.result = ''
