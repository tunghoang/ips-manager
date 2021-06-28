import time
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

LOG_PATH = '/var/log/clamav/log_virus.log'
WATCH_PATH = "/tmp/virus"
def addVirusToLog(virus, time):
  with open(LOG_PATH , 'a') as f:
    f.write("{} Infected files:{}".format(time, virus))
class OnMyWatch:
  # Set the directory on watch
  watchDirectory = WATCH_PATH

  def __init__(self):
    self.observer = Observer()

  def run(self):
    event_handler = Handler()
    self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
    self.observer.start()
    try:
      while True:
        time.sleep(5)
    except:
      self.observer.stop()
      print("Observer Stopped")

    self.observer.join()


class Handler(FileSystemEventHandler):

  @staticmethod
  def on_any_event(event):
    if event.is_directory:
      return None

    elif event.event_type == 'created':
      # Event is created, you can process it now
      print("Watchdog received created event - % s." % event.src_path)
    elif event.event_type == 'modified':
      # Event is modified, you can process it now
      print("Watchdog received modified event - % s." % event.src_path)
      path = str(event.src_path)
      cmd = "sudo clamscan "+'"'+path+'"'
      print(path)
      p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
      (output, err) = p.communicate()
      p_status = p.wait()
      print(output)
      state = str(output).find("Infected files: 1")
      if(state != -1):
        addVirusToLog(path, str(datetime.datetime.now()))

if __name__ == '__main__':
  watch = OnMyWatch()
  watch.run()
