from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('settings', {
    'idSetting': Integer,
    'param': String,
    'value': String,
    'category': String 
  },mask='*');
  return model