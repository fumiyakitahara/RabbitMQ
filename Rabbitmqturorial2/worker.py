#!/usr/bin/env python
import pika
import time

#ワーカー(Consumer)はアプリ自体である。
#一つのキューからワーカーを二つ作るにはpython3 worker.pyを二回うつ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)#durableで再起動してもキューが失われない。これだけだとメッセージは失われる
print(' [*] Waiting for messages. To exit press CTRL+C')


#ack(nowledgement)はコンシューマから返送され、特定のメッセージが受信、処理され、RabbitMQがそれを自由に削除できることをRabbitMQに知らせます。
#ackが帰ってこない場合、RabbitMMQは処理されなかったと判断し、メッセージを再キューイングする
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag) #ワーカーが死んだ後すぐに、すべての未承認メッセージは再送される
    #RabbitMQはackされていないメッセージを解放できないので、どんどんメモリを消費する。

"""
Basic_ackを見落とすのミスをデバッグするために
sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged
"""

channel.basic_qos(prefetch_count=1) #RabbitMQに一度に1つ以上のメッセージをワーカーに与えないように指示するもの。一つのワーカーに重い処理が集中するのを防ぐ
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()