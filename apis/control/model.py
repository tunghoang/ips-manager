from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('control', {
    'dummy': Integer 
  },mask='*');
  return model

def create_status_report(api):
  model = api.model('statusReport', {
    'online': Boolean,
    'enabled': Boolean,
    'data': String
  },mask='*');
  return model
