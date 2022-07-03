""""
ワークキュー（別名：タスクキュー）の主な考え方は、
リソースを大量に消費するタスクをすぐに実行せず、その完了を待つ必要がないようにすることです。
その代わりに、タスクを後で実行するようにスケジューリングすること。
"""


#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE#これを指定することでメッセージを再起動などの時に消えないようにする
    ))
print(" [x] Sent %r" % message)
connection.close()