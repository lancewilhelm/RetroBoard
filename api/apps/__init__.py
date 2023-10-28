def _get_apps_list():
	import os
	import sys, inspect
	from setup import settings

	apps = []
	globals_, locals_ = globals(), locals()
	dir_path = os.path.dirname(__file__)
	dir_name = os.path.basename(dir_path)
	
	for filename in os.listdir(dir_path):
		modulename, ext = os.path.splitext(filename)
		if modulename[0] != '_' and ext in ('.py', '.pyw'):
			subpackage = '{}.{}'.format(dir_name, modulename)
			# print(subpackage, globals_, locals_, modulename)
			module = __import__(subpackage, globals_, locals_, [modulename])
			app = [m for m in inspect.getmembers(sys.modules[module.__name__], inspect.isclass) if m[1].__module__ == subpackage][0]
			apps.append(app[0])
			settings.app_dict[app[0]] = app[1]

	settings.main['apps_list'] = apps

	return apps
	
if __name__ != '__main__':
	_get_apps_list()