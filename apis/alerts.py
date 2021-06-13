from flask import request
from flask_restplus import Namespace, Resource, reqparse
from werkzeug.exceptions import *
from .app_utils import *
from .config_utils import config
import requests
import os
import calendar;
import time;
def sendMessage(text, token, chatId):
  return requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data = {
      'chat_id': chatId,
      'text': text
    }
  )
def registerWebHook(url, token, certFile):
  r = requests.post(
    f"https://api.telegram.org/bot{token}/setWebhook",
    data = {
      'url': url, 
    },
    files = {
      'certificate': open(certFile, 'rb')
    } 
  )
  if r.ok:
    print(r.text)
  else:
    print(f"{r.status_code} {r.reason}")

__registerUrl = config.get('telegram', 'callback_url')
token = config.get('telegram', 'token')
__certFile = config.get('telegram', 'cert_file')
groupChatId = config.get('telegram', 'group_chat_id')

print(f"https://api.telegram.org/bot{token}/setWebhook")
print({
  'url': __registerUrl, 
  'certificate': open(__certFile, 'rb')
})

registerWebHook(__registerUrl, token, __certFile)


botAlertApi = Namespace('bot_alert', "bot alerts")

@botAlertApi.route('/')
class BotAlert(Resource):
  @botAlertApi.doc("Callback url for bot alert")
  def post(self):
    doLog(f"bot alert received \n{botAlertApi.payload}")
    message = botAlertApi.payload.get('message', botAlertApi.payload.get('edited_message'))
    if message is None:
      return "bot alert received"
    text = message['text']
    print(f"{token} {text} {groupChatId}")
    r = sendMessage(text, token, groupChatId)
    if r.ok:
      print(r.text)
    else:
      print(f"{r.status_code} {r.reason}")

    return "bot alert received"
