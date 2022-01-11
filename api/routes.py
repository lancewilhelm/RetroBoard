# Render index.html from templates if the user navigates to /
from flask import render_template
from utils import api
import ledTasks
import threading
import logging

@api.route('/', methods=['GET'])
def index_route():
    return render_template('index.html')

@api.route('/api/app', methods=['GET'])
def pixel_route():
    logging.info('API request received for {}'.format('pixel'))
    mode_thread = threading.Thread(target=ledTasks.pixel, daemon=True)
    try:
        logging.debug('starting thread')
        mode_thread.start()
    except Exception:
        logging.exception('Exception occured in pixel route')
        
    return 'OK'