#!/usr/bin/env python3
from utils import api
import routes 
import logging
import os
import ledTasks

# Start the flask server if this file was called as __main__
if __name__ == '__main__':
	clock = ledTasks.Picture()
	ledTasks.running_tasks.append(clock)
	clock.start()
	
	logging.info('STARTING THE WARP ENGINES (starting flask)')
	api.run(host='0.0.0.0')
