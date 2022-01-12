#!/usr/bin/env python3
from utils import api
import routes 
import logging
import os

# Start the flask server if this file was called as __main__
if __name__ == '__main__':
	logging.info('starting the flask server')
	api.run(host='0.0.0.0')
