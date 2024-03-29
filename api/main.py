#!/usr/bin/env python3
from setup import api, settings
import routes 
import logging
from apps._appbase import start_led_app

# Start the flask server if this file was called as __main__
if __name__ == '__main__':
	start_led_app(settings.main['running_apps'][0])
	logging.info('STARTING THE WARP ENGINES (starting flask)')
	try:
		api.run(host='0.0.0.0')
	except:
		api.run(host='0.0.0.0', port=3001)
