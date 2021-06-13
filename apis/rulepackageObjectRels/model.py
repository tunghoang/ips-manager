from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('rulepackageObjectRel', {
    'idRulepackageobjectrel': Integer,
    'idRulepackage': Integer,
    'idObject': Integer,
    'errored': Boolean,
    'synced': Boolean,
    'syncedAt': DateTime 
  },mask='*');
  return model