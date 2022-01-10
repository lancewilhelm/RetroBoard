# Render index.html from templates if the user navigates to /
from flask import render_template
from utils import api
import ledTasks

@api.route('/', methods=['GET'])
def index_route():
    return render_template('index.html')

@api.route('/api/pixel', methods=['GET'])
def pixel_route():
    print('starting route function')
    try:
        ledTasks.pixel()
    except Exception as e:
        print(e)
        
    return 'OK'