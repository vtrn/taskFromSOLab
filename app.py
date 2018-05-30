#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request
from test import Cell, Dispacher
from threading import Thread

tasks = Dispacher()

Thread(target=tasks.hadle, args=()).start()

app = Flask(__name__)


@app.route('/GET/v1/task_uuid/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks.tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    cell = {'status': task[0]['task']['status'], 'result': task[0]['task']['result']}
    return jsonify(cell)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/POST/v1/task', methods=['POST'])
def create_task():
    url = {'url': request.json['url']}
    id = len(tasks.queue)+1
    tasks.queue.append({id:Cell(url['url'],uuid=id)})
    return jsonify({'task_uuid': id, 'status': tasks.queue[id-1][id].status}), 201


if __name__ == '__main__':
    app.run(debug=True)
