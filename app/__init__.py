from flask import Flask

# Import blueprints
from app.blueprints.dockertools.dockertools import dockertools

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    # Register blueprints with URL prefixes
    app.register_blueprint(dockertools, url_prefix='/dockertools')

    
    return app
