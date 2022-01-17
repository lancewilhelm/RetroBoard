# Render index.html from templates if the user navigates to /
import time
from flask import render_template, request
from utils import api, settings
import ledTasks
import logging

#-------------------------------------------------------------------------
# Routes:
#-------------------------------------------------------------------------
# Index route for api
@api.route('/', methods=['GET'])
def index_route():
	return render_template('index.html')

# App route for api
@api.route('/api/app', methods=['POST'])
def pixel_route():
	request_form = request.get_json()
	logging.info('API request received for {}'.format(request_form['app']))

	if len(ledTasks.running_tasks) == 0:
		if request_form['app'] != 'clear':
			task = ledTasks.task_dict[request_form['app']]
			ledTasks.running_tasks.append(task)
			task.start()
		return 'OK'

	else:
		task = ledTasks.running_tasks[0]
		if request_form['app'] == 'clear':
			task.stop()
			task.join()
			ledTasks.running_tasks = []
		elif task.name != request_form['app']: 
			task.stop()
			task.join()
			ledTasks.running_tasks = []
			task = ledTasks.task_dict[request_form['app']]
			ledTasks.running_tasks.append(task)

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
		settings.importSettings()
		return "OK"