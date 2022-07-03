#!/usr/bin/env python
#キューにメッセージを送るプログラム

import pika #Python client

#rabbtimqサーバーとコネクションを作る
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#helloキューの作成。
channel.queue_declare(queue='hello')

"""
RabbitMQでは、メッセージを直接キューに送信することはできず、常にExchangeを経由する必要があります。
このExchangeは特別なもので、メッセージがどのキューに送られるべきかを正確に指定することができます。
キュー名は、routing_key パラメータで指定する必要があります。
"""

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

#接続を閉じる
connection.close()