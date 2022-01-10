from flask import Flask
from flask_cors import CORS
from celery import Celery

# Create the quart object
api = Flask(__name__)
CORS(api)       # CORS BS that we likely don't need to worry about'

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='rpc://',
        broker='pyamqp://',
        imports=('ledTasks',)
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery_app = make_celery(api)

