# Render index.html from templates if the user navigates to /
from flask import render_template
from utils import api
import ledTasks
import threading

@api.route('/', methods=['GET'])
def index_route():
    return render_template('index.html')

@api.route('/api/pixel', methods=['GET'])
def pixel_route():
    print('starting route function')
    test_thread = threading.Thread(target=ledTasks.pixel, daemon=True)
    try:
        test_thread.start()
        print('hopefully this shows immediately and not after the animation is done')
    except Exception as e:
        print(e)
        
    return 'OK'