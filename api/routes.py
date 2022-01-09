from ledUtils import *
from quart import Quart, render_template, request, jsonify
from api import api

# Render index.html from templates if the user navigates to /
@api.route('/', methods=['GET'])
async def index():
    return await render_template('index.html')

# Rotating block demo api call
@api.route('/api/rotate', methods=['GET'])
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

@api.route('/api/test1', methods=['GET'])
async def test1():
    asyncio.get_event_loop().create_task(test1_func())
    return 'test1 done'

@api.route('/api/test2', methods=['GET'])
async def test2():
    asyncio.get_event_loop().create_task(test2_func())
    return 'test2 done'