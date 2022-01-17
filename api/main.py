#!/usr/bin/env python3
from utils import api, settings
import routes 
import logging
import ledTasks

# Start the flask server if this file was called as __main__
if __name__ == '__main__':
	ledTasks.start_led_app(settings.running_apps[0])
	
	logging.info('STARTING THE WARP ENGINES (starting flask)')
	api.run(host='0.0.0.0')
