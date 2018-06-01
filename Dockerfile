FROM python:3

ADD requirements.txt ./
ADD api /api
ADD setup.py /setup.py

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP api/app.py
ENV REDIS_HOST redis

CMD for i in $(seq 2); do rq worker --url redis://$REDIS_HOST:6379/0 & done && python -m flask run --host=0.0.0.0