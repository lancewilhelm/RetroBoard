#!/usr/bin/env python3

# Import the Flask api object
from flaskUtils import api

# Start the flask server if this file was called
if __name__ == '__main__':
    api.run(host='0.0.0.0')
