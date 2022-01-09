from quart import Quart, render_template, request, jsonify
from quart_cors import cors
import asyncio

# Import the LED Utility functions and items necessary for driving the matrix
from ledUtils import RotatingBlockGenerator, RunText

# Create the quart object
api = Quart(__name__)
cors(api)       # CORS BS that we likely don't need to worry about

# Render index.html from templates if the user navigates to /
@api.route('/', methods=['GET'])
async def index():
    loop = asyncio.get_event_loop()
    loop.close()
    return await render_template('index.html')

# Rotating block demo api call
@api.route('/api/rotate', methods=['GET'])
async def runRotate():
    # Create the object
    rotating_block_generator = RotatingBlockGenerator()
    
    # If the process does not already exists, run it and then display help
    rotating_block = asyncio.create_task(rotating_block_generator.process({}))
    await rotating_block
    return 'block rotating done'

@api.route('/api/clock', methods=['GET'])
async def runClock():
    # Create the object
    run_text = RunText()
    
    print('between class init and running')

    run_text.process({})

    return 'clock done'