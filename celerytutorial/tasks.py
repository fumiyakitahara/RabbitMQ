"""
https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#first-steps
"""
from celery import Celery

#Celeryの最初の引数は、現在のモジュールの名前(これがワーカーに該当する), 第二引数は broker キーワード引数で、使用するメッセージブローカの URL を指定
app = Celery('tasks', backend = 'rpc://', broker='amqp://localhost') #rabbitmqを使用する場合。

@app.task
def add(x, y):
    return x + y