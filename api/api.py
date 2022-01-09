#!/usr/bin/env python3
from celery import Celery
from dotenv import load_dotenv
from quart import Quart, render_template, request, jsonify
from quart_cors import cors
import routes 

# Create the quart object
api = Quart(__name__)
cors(api)       # CORS BS that we likely don't need to worry about'

# Start the quart server if this file was called
if __name__ == '__main__':
    api.run(host='0.0.0.0')
