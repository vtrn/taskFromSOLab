#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request
from work import Task, Dispatcher
from threading import Thread
import collections

dispatcher = Dispatcher()

#m = Thread(target=dispatcher.produce, args=())
#m.start()

app = Flask(__name__)


@app.route('/v1/task/<task_uuid>', methods=['GET'])
def get_task(task_uuid):
    search_task = [task for task in dispatcher.done_work if [x for x in task['task_uuid'].keys()][0] == task_uuid]
    status = search_task[0]['task_uuid'][task_uuid]['status']
    result = search_task[0]['task_uuid'][task_uuid]['result']
    data = {'status':status, 'results':result}
    new_data = collections.OrderedDict(sorted(data.items(), key=lambda t: t[0]))
    if len(search_task) == 0:
        abort(404)
    return jsonify(new_data)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/v1/task/', methods=['POST'])
def create_task():
    url = {'url': request.json['url']}
    dispatcher.push(url['url'])
    dispatcher.create_task()
    index = len(dispatcher.work_queue) -1
    data = dispatcher.work_queue[index].get_data()
    uuid = [x for x in data['task_uuid'].keys()][0]
    dispatcher.produce()
    return jsonify({'task_uuid':uuid}), 201


if __name__ == '__main__':
    app.run(debug=True)
