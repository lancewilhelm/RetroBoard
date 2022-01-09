from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import ledTasks
from celery import Celery
from flask.helpers import make_response

# Create the quart object
api = Flask(__name__)
CORS(api)       # CORS BS that we likely don't need to worry about'

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='rpc://',
        broker='pyamqp://'
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery_app = make_celery(api)

# Render index.html from templates if the user navigates to /
@api.route('/', methods=['GET'])
async def index():
    return await render_template('index.html')

# Rotating block demo api call
@api.route('/api/rotate', methods=['GET'])
async def runRotate():
    # Create the object
    rotating_block_generator = ledTasks.RotatingBlockGenerator()
    
    # Try running the block rotation
    try:
        rotating_block_generator.run({})
    except Exception as e:
        print("Error starting animation\n")
        print(e)

    return 'block rotation done'

@api.route('/api/clock', methods=['GET'])
async def runClock():
    # Create the object
    run_text = RunText()
    
    # Try running the block rotation
    try:
        run_text.run({})
    except Exception as e:
        print("Error starting animation\n")
        print(e)

    return 'clock done'

@api.route('/api/pixel', methods=['GET'])
async def pixel():
    # Try running the block rotation
    try:
        task = ledTasks.test.delay()
        task.wait()
    except Exception as e:
        print("Error starting animation\n")
        print(e)
    return 'pixel done'

@celery_app.Task
def test():
    for i in range(5):
        print(i)
        return 'done'