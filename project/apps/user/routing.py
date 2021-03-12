from flask import Blueprint
from ..user import controller

routes = Blueprint('/api/accounts', __name__)

routes.add_url_rule(
    'regis',
    'Register',
    controller.registor,
    methods=["GET"]
)

routes.add_url_rule(
    'login',
    'Login',
    controller.login,
    methods=["GET"]
)

routes.add_url_rule(
    'logout',
    'Logout',
    controller.logout,
    methods=["GET"]
)

routes.add_url_rule(
    'service_registor',
    'Service_registor',
    controller.service_registor,
    methods=["POST"]
)

routes.add_url_rule(
    'service_login',
    'service_Login',
    controller.service_login,
    methods=["POST","GET"]
)
