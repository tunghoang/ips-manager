from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('control', {
    'dummy': Integer 
  },mask='*');
  return model

def create_response_model(api):
  model = api.model('controlResponse', {
    'success': Boolean,
    'online': Boolean,
    'enabled': Boolean,
    'data': String
  },mask='*');
  return model
