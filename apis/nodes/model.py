from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('node', {
    'idNode': Integer,
    'idNodetype': Integer,
    'specs': Text 
  },mask='*');
  return model