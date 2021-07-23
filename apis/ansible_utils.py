import ansible_runner
import os, sys
import json
from .config_utils import config
from getopt import getopt, GetoptError

def auIsOk(runner, ip):
  return ip in runner.stats['ok'].keys()
def auIsProcessed(runner, ip):
  return ip in runner.stats['processed'].keys()
def auIsChanged(runner, ip):
  return ip in runner.stats['changed'].keys()
def auIsSkipped(runner, ip):
  return ip in runner.stats['skipped'].keys()
def auIsFailed(runner, ip):
  return ip in runner.stats['failures'].keys()
def auOutput(runner, ip):
  return runner.stdout.read()

ansibleRoot = config.get("Default", "ansible_root", fallback="")

def cleanHosts(arg):
  os.remove(f"{ansibleRoot}/inventory/hosts")

def __result(runner, ip, eventFn=None):
  if eventFn is None:
    return {'ok':auIsOk(runner, ip), 'changed':auIsChanged(runner, ip), 'failed': auIsFailed(runner, ip)}
  details = []
  for host_event in r.events:
    if host_event['event'] == 'runner_item_on_ok':
      task = host_event['event_data']['task']
      details.append( eventFn(host_event['event_data']) )
  return {'ok':auIsOk(runner, ip), 'changed':auIsChanged(runner, ip), 'failed': auIsFailed(runner, ip), 'details': details}

def __invokePlaybook(ip, playbook, extravars = None):
  r = ansible_runner.run(private_data_dir=ansibleRoot,
    playbook=playbook,
    finished_callback=cleanHosts,
    inventory=ip,
    extravars=extravars
  )
  return __result(r, ip)

def provision(ip):
  #return __invokePlaybook(ip, 'pb.yaml')
  return __invokePlaybook(ip, 'provisioning.yaml')

def stopBeats(ip):
  return __invokePlaybook(ip, 'stop-beats.yaml')

def startBeats(ip):
  return __invokePlaybook(ip, 'start-beats.yaml')

def stopIPS(ip):
  return __invokePlaybook(ip, 'stop-ips.yaml')

def startIPS(ip):
  return __invokePlaybook(ip, 'start-ips.yaml')

def installModSecRules(ip, webserver, ruleset):
  return __invokePlaybook(ip, f'{webserver}/{ruleset}/install.yaml')

def uninstallModSecRules(ip, webserver, ruleset):
  return __invokePlaybook(ip, f'{webserver}/{ruleset}/uninstall.yaml')

def installApplicationRules(ip, application, version):
  print(f'INSTALL --{ip}-- --{application}-- --{str(version)}--')
  return __invokePlaybook(ip, f'rulesets/{application}/install.yaml', {'version': version})

def checkStatus(ip):
  return __invokePlaybook(ip, 'check-status.yaml', lambda event_data: {
    'task': event_data['task'], 
    'name': event_data['res']['name'], 
    'state': event_data['res']['state']
  })

if __name__ == "__main__":
  ip = '192.168.0.45'

  try:
    opts, args = getopt(sys.argv[1:], "psSrRa:", ["provision", "stop-beats", "stop-ips", "run-beats", "run-ips", "ip="])
  except GetoptError as err:
    print(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

  taskFn = None

  for o, a in opts:
    if o in ("-a", "--ip"):
      ip = a

    if o in ("-p", "--provision"):
      taskFn = provision
    elif o in ("-s", "--stop-beats"):
      taskFn = stopBeats
    elif o in ("-S", "--stop-ips"):
      taskFn = stopIPS
    elif o in ("-r", "--run-beats"):
      taskFn = startBeats
    elif o in ("-R", "--run-ips"):
      taskFn = startIPS

  if taskFn is not None:
    print(taskFn(ip))
