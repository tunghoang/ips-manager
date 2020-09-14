from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('containmentRel', {
    'idContainmentRel': Integer,
    'idContainer': Integer,
    'idContainee': Integer 
  },mask='*');
  return model