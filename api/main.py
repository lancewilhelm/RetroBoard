#!/usr/bin/env python3
from utils import api
import routes 
import logging
import os

# Start the quart server if this file was called
if __name__ == '__main__':
    logging.info('starting the flask server')
    api.run(host='0.0.0.0')
