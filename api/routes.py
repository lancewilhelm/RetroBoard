# Render index.html from templates if the user navigates to /
import time
from flask import render_template
from utils import api, matrix
import ledTasks
import logging

@api.route('/', methods=['GET'])
def index_route():
    return render_template('index.html')

@api.route('/api/app', methods=['GET'])
def pixel_route():
    logging.info('API request received for {}'.format('pixel'))
    if len(ledTasks.tasks) == 0:
        t1 = ledTasks.TestAnimation()
        ledTasks.tasks.append(t1)
        try:
            logging.debug('starting thread')
            t1.start()
        except Exception:
            logging.exception('Exception occured in pixel route')
            
        return 'OK'
    else:
        t2 = ledTasks.tasks[0]
        t2.stop()
        ledTasks.tasks = []
        return 'OK'