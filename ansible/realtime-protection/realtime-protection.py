import time, os
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
from configparser import ConfigParser

  
## Read config from file
config_file = "realtime-protection.ini"
config_object = ConfigParser()

def save(config, fname):
  with open(fname, 'w') as f:
    config.write(f)

if os.path.isfile(config_file):
	config_object.read(config_file)
	WATCH_PATH = config_object.get("CLAMAV", "watch_path")
	LOG_PATH = config_object.get("CLAMAV", "log_path")
	print("Log location:", LOG_PATH)
	print("Monitor directories:", WATCH_PATH)
	WATCH_PATH = WATCH_PATH.split(",")

else:
  print(f"Configure file {config_file} does not exist")
  exit()
# LOG_PATH = '/var/log/clamav/log_virus.log'
# WATCH_PATH = ["/var/www/html/upload3/", "/var/www/html/upload1/", "/var/www/html/upload2/", "/var/www/html/upload/"]


## Scan virus and write to log functions
def addVirusToLog(log):
	with open(LOG_PATH , 'a') as f:
		f.write(log+"\n") 

def handleVirus(path):
	cmd = "sudo clamscan "+'"'+path+'"'
	# print(cmd)
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	p_status = p.wait()
	output = output.decode(encoding='UTF-8')
	state = output.find("Infected files: 1")
	if(state != -1):
		# addVirusToLog(path, str(datetime.datetime.now()))
		data = output.splitlines()
		path, warning = data[0].split(":")
		time_scan = data[10]
		date = str(datetime.datetime.now())
		log = "{} - File infected: {} - Virus Type: {} - Time scan: {} ".format(date, path,warning, time_scan)
		print(log)
		addVirusToLog(log)

## Class from watchdog to monitor changes in directories
class OnMyWatch:
	# Set the directory on watch
	watchDirectories = WATCH_PATH

	def __init__(self):
		self.observers = [] 

	def run(self):
		# event_handler = Handler()
		for dir in self.watchDirectories:
			if os.path.isdir(dir):
				print(dir)
				observer = Observer()
				observer.schedule(Handler(), dir, recursive = True)
				self.observers.append(observer)
			else:
				print("Dir not exist:", dir) 
		if len(self.observers) == 0:
			exit()
		for observer in self.observers:
			observer.start()
		try:
			while True:
				time.sleep(5)
		except:
			for observer in self.observers:
				observer.stop()
			print("Observers Stopped")
		
		for observer in self.observers:
			observer.join()

	# self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
	# self.observer.start()
	# try:
	# 	while True:
	# 		time.sleep(5)
	# except:
	# 	self.observer.stop()
	# 	print("Observer Stopped")

		# self.observer.join()


class Handler(FileSystemEventHandler):

	@staticmethod
	def on_any_event(event):
		if event.is_directory:
			return None
		# elif event.event_type == 'created':
		# 	# Event is created, you can process it now
		# 	print("Watchdog received created event - % s." % event.src_path)
		elif event.event_type == 'modified':
			# Event is modified, you can process it now
			print("Watchdog received modified event - % s." % event.src_path)
			path = str(event.src_path)
			try:
				handleVirus(path)
			except Exception as e:
				print(e)

if __name__ == '__main__':
	watch = OnMyWatch()
	watch.run()
