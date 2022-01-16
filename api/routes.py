# Render index.html from templates if the user navigates to /
import time
from flask import render_template, request
from utils import api, settings
import ledTasks
import logging
import json

#-------------------------------------------------------------------------
# Routes:
#-------------------------------------------------------------------------
# Index route for api
@api.route('/', methods=['GET'])
def index_route():
	return render_template('index.html')

# App route for api
@api.route('/api/app', methods=['GET'])
def pixel_route():
	logging.info('API request received for {}'.format('pixel'))

	if len(ledTasks.tasks) == 0:
		t1 = ledTasks.Clock()
		ledTasks.tasks.append(t1)
		try:
			logging.debug('starting thread')
			t1.start()
		except Exception:
			logging.exception('Exception occured in pixel route')
			
		return 'OK'

	else:
		t2 = ledTasks.tasks[0]
		t2.stop()
		ledTasks.tasks = []
		return 'OK'

# App route for settings pull
@api.route('/api/settings', methods=['GET', 'POST'])
def settings_route():
	logging.debug('settings request received')
	if request.method == 'GET':
		# Get the settings from the settings task
		with open('/home/pi/RetroBoard/settings.json', 'r') as filehandle:
			return filehandle.read()
	
	elif request.method == 'POST':
		settingsFromWeb = request.json
		# Write the settings to webpagesettings.txt
		settings.dumpSettings(settingsFromWeb)
		settings.loadSettings()
		return "OK"