from flask import Flask

# Import blueprints
from app.blueprints.dockertools.dockertools import dockertools
from app.blueprints.familyphotos.familyphotos import familyphotos

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    # Register blueprints with URL prefixes
    app.register_blueprint(dockertools, url_prefix='/dockertools')
    app.register_blueprint(familyphotos, url_prefix='/familyphotos')

    
    return app
