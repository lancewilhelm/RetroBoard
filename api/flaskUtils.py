from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Import the LED Utility functions and items necessary for driving the matrix
from ledUtils import RotatingBlockGenerator

# Create the flask object
api = Flask(__name__)
CORS(api)       # CORS BS that we likley don't need to worry about

# Render index.html from templates if the user navigates to /
@api.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Rotating block demo api call
@api.route('/api/rotate', methods=['GET'])
def runRotate():
    # Create the object
    rotating_block_generator = RotatingBlockGenerator()

    # If the process does not already exists, run it and then display help
    if (rotating_block_generator.process({})):  
        print('block rotation succeeded') 
    else:
        print('block rotation failed') 
    
    return 'block rotating done'

@api.route('/api/clock', methods=['GET'])
def runClock():
    return 'clock done'