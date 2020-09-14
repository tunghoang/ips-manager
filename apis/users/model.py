from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('user', {
    'idUser': Integer,
    'username': String,
    'password': String 
  },mask='*');
  return model