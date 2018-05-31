from flask import Flask, jsonify, abort, make_response, request
from redis import Redis
from rq import Queue

from work import get_result, Task

app = Flask(__name__)
queue = Queue(connection=Redis())


@app.route('/v1/task/<task_uuid>', methods=['GET'])
def get_task(task_uuid):
    job = queue.fetch_job(task_uuid)
    if job is None:
        abort(404)
    task = job.result
    if task is None:
        task = Task()
    return jsonify(task)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/v1/task/', methods=['POST'])
def create_task():
    import uuid
    url = request.json['url']
    uuid = uuid.uuid4().hex
    queue.enqueue(get_result, url, job_id=uuid)
    return jsonify({'task_uuid': uuid})


if __name__ == '__main__':
    app.run(debug=True)
