#!/usr/bin/env python3
from utils import api
import routes 
import logging
import os
import ledTasks

# Start the flask server if this file was called as __main__
if __name__ == '__main__':
	logging.debug('Starting the clock as an opening app')
	clock = ledTasks.Clock()
	ledTasks.tasks.append(clock)
	clock.start()
	
	logging.info('starting the flask server')
	api.run(host='0.0.0.0')
