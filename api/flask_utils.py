from ledTasks import *
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Create the quart object
api = Flask(__name__)
CORS(api)       # CORS BS that we likely don't need to worry about'

# Render index.html from templates if the user navigates to /
@main.route('/', methods=['GET'])
async def index():
    return await render_template('index.html')

# Rotating block demo api call
@main.route('/api/rotate', methods=['GET'])
async def runRotate():
    # Create the object
    rotating_block_generator = RotatingBlockGenerator()
    
    # Try running the block rotation
    try:
        rotating_block_generator.run({})
    except Exception as e:
        print("Error starting animation\n")
        print(e)

    return 'block rotation done'

@main.route('/api/clock', methods=['GET'])
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

@main.route('/api/pixel', methods=['GET'])
async def pixel():
    # Create the object
    simple_pixel = SimplePixel()
    tasks = asyncio.all_tasks()
    print(tasks)    # Try running the block rotation
    try:
        simple_pixel.run({})
    except Exception as e:
        print("Error starting animation\n")
        print(e)
    return 'pixel done'

@main.route('/api/test1', methods=['GET'])
async def test1():
    asyncio.get_event_loop().create_task(test1_func())
    return 'test1 done'

@main.route('/api/test2', methods=['GET'])
async def test2():
    asyncio.get_event_loop().create_task(test2_func())
    return 'test2 done'