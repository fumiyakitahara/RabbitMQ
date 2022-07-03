#!/usr/bin/env python
#二つ以上のキュー(Exchangeが必要)と二つ以上のワーカーのことを"publish/subscribe"
#プロデューサはメッセージをExchangeに送信しているのでどのキューに配送されたか知らない。
"""
Exchange Type: direct、topic、headers、fanout 
チュートリアル1,2でExchangeを使わなかったのは空の文字列 ("") で識別されるデフォルトのエクスチェンジを使用していたため
キューに名前を付けることは、プロデューサとコンシューマの間でキューを共有したい場合に必要だが、基本は使わない？

Bindingとは    Exchange とキューの間のその関係
"""


import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
#exhangeの名前をlogsに指定、タイプをfanout(繋がっているキューにブロードキャスト)に指定
channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
#queue=""だとランダムでキューの名前を入れてくれる
#コンシューマ接続が閉じられたら、キューは削除されなければなりません。exclusiveはそのための排他フラグとして使う
queue_name = result.method.queue

#この処理以降、logs exchange はキューにメッセージを追加します
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()