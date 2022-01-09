#!/usr/bin/env python3
from flask_utils import api

# Create the quart object
api = Quart(__name__)
cors(api)       # CORS BS that we likely don't need to worry about'

# Start the quart server if this file was called
if __name__ == '__main__':
    api.run(host='0.0.0.0')
