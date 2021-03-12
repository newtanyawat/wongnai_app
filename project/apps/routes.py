from apps.server import app
from apps.user.routing import routes as accounts 
from apps.service.routing import routes as files 

def init_routes():
    app.register_blueprint(accounts, url_prefix="/api/accounts")
    app.register_blueprint(files, url_prefix="/api/files")
   
