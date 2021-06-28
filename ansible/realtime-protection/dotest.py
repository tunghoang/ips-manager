from configparser import ConfigParser

def save(config, fname):
  with open(fname, 'w') as f:
    config.write(f)

config = ConfigParser()
config.read('realtime-protection.ini')
watchpaths = config.get('CLAMAV', 'watch_path')
watchpaths = watchpaths.split(',')
print(watchpaths)

save(config, 'test.ini')
