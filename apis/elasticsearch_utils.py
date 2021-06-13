from .config_utils import config
from .app_utils import make_delete_request
from .config_utils import config

elasticsearch_url = config.get('elasticsearch', 'elasticsearch_url')
def delete_index(index_name):
  return make_delete_request(elasticsearch_url, '/' + index_name)
