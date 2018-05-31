import threading

from flask import Flask, jsonify, abort, make_response, request
from redis import Redis
from rq import Queue

from work import Dispatcher

app = Flask(__name__)
#redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

dispatcher = Dispatcher()
queue = Queue(connection=Redis.from_url('redis://'), default_timeout=3600)
job = queue.enqueue_call(dispatcher.produce)

@app.route('/v1/task/<task_uuid>', methods=['GET'])
def get_task(task_uuid):
    if task_uuid not in dispatcher.tasks:
        abort(404)
    task = dispatcher.tasks[task_uuid]
    data = {'status': task.status, 'result': task.result}
    return jsonify(data)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/v1/task/', methods=['POST'])
def create_task():
    url = request.json['url']
    uuid = dispatcher.create_task(url)
    return jsonify({'task_uuid': uuid})


if __name__ == '__main__':
    app.run(debug=True)
