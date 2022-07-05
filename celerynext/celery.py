from celery import Celery

#include 引数は、Worker が起動するときにインポートするモジュールのリスト
#第一引数にディレクトリを指定すると d.app,d.cerely...などを探す
app = Celery('celerynext',
             broker='amqp://',
             backend='rpc://',
             include=['celerynext.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()