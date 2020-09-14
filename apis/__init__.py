from flask_restplus import Api
api = Api(title="IPS Manager", version="1.0")

from .roles import create_api as create_roles
api.add_namespace(create_roles())
from .users import create_api as create_users
api.add_namespace(create_users())
from .userRoleRels import create_api as create_userRoleRels
api.add_namespace(create_userRoleRels())
from .nodetypes import create_api as create_nodetypes
api.add_namespace(create_nodetypes())
from .nodes import create_api as create_nodes
api.add_namespace(create_nodes())
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
