from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('permission', {
    'idPermission': Integer,
    'idRole': Integer,
    'idObject': Integer,
    'action': String 
  },mask='*');
  return model