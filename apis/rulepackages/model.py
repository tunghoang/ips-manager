from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('rulepackage', {
    'idRulepackage': Integer,
    'idEnginetype': Integer,
    'application': String,
    'version': Integer,
    'appliedAt': DateTime,
    'status': String 
  },mask='*');
  return model