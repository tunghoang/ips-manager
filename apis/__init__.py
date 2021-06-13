from flask_restplus import Api
api = Api(title="IPS Manager", version="1.0")

from .roles import create_api as create_roles
api.add_namespace(create_roles())
from .users import create_api as create_users
api.add_namespace(create_users())
from .userRoleRels import create_api as create_userRoleRels
api.add_namespace(create_userRoleRels())
from .enginetypes import create_api as create_enginetypes
api.add_namespace(create_enginetypes())
from .engines import create_api as create_engines
api.add_namespace(create_engines())
from .objects import create_api as create_objects
api.add_namespace(create_objects())
from .containmentRels import create_api as create_containmentRels
api.add_namespace(create_containmentRels())
from .permissions import create_api as create_permissions
api.add_namespace(create_permissions())
from .login import create_api as create_login
api.add_namespace(create_login())
from .logout import create_api as create_logout
api.add_namespace(create_logout())
from .rulepackages import create_api as create_rulepackages
api.add_namespace(create_rulepackages())
from .control import create_api as create_control
api.add_namespace(create_control())
#from .alerts import botAlertApi
#api.add_namespace(botAlertApi)
