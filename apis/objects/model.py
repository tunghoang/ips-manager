from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('object', {
    'idObject': Integer,
    'name': String,
    'idNode': Integer,
    'description': String 
  },mask='*');
  return model