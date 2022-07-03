#キューからメッセージを受け取るプログラム、つまりワーカー
#起動方法
#https://qiita.com/suke_masa/items/5d583462727660663fde#rabbitmq%E3%81%AE%E8%A8%AD%E5%AE%9A%E5%BF%85%E8%A6%81%E3%81%AB%E5%BF%9C%E3%81%98%E3%81%A6-1 

import pika,sys,os

#rabbtimqサーバーとコネクションを作る
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    #receve側でもキューを宣言しておく
    channel.queue_declare(queue='hello')

    """
    補足
    rabbitmqctl list_queues どれだけのメッセージがあるか確認できる
    """

    #メッセージを受信するたびに、このコールバック関数が Pika ライブラリによって呼び出されます
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    #コールバック関数がhelloキューからメッセージを受信するようにRabbitMQに指示する
    channel.basic_consume(queue='hello',
                        auto_ack=True,
                        on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)