# Render index.html from templates if the user navigates to /
from flask import render_template, request
from setup import api, settings
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
	logging.debug('API request received for {}. Task currently running {}'.format(request_form['app'], settings.current_thread))

	if settings.current_thread == None:
		if request_form['app'] != 'clear':
			ledTasks.start_led_app(request_form['app'])
	else:
		if request_form['app'] == 'clear':
			ledTasks.stop_current_led_app()
		elif request_form['app'] != settings.current_thread.name:
			ledTasks.stop_current_led_app()
			ledTasks.start_led_app(request_form['app'])

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
		settings_from_web = request.json
		# Write the settings to webpagesettings.txt
		settings.dump_settings(settings_from_web)
		settings.import_settings()
		return "OK"