# Render index.html from templates if the user navigates to /
from flask import render_template, request
from utils import api, settings
import ledTasks
import logging
import threading

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
	logging.debug('API request received for {}. Tasks currently running {}'.format(request_form['app'], ledTasks.running_tasks))

	if len(ledTasks.running_tasks) == 0:
		if request_form['app'] != 'clear':
			task = ledTasks.task_dict[request_form['app']]
			print(task._started.is_set())
			ledTasks.running_tasks.append(task)
			task.start()
			print(task._started.is_set())
	else:
		task = ledTasks.running_tasks[0]
		if request_form['app'] == 'clear':
			task.stop()
			ledTasks.running_tasks = []
			task.join()
			print(task._started.is_set())
		elif task.name != request_form['app']: 
			task.stop()
			ledTasks.running_tasks = []
			task.join()
			task2 = ledTasks.task_dict[request_form['app']]
			ledTasks.running_tasks.append(task2)

	for thread in threading.enumerate():
		print(thread.name)

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