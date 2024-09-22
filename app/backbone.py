##
## Library Imports
##

# Standard library imports
import json
import sys
import os

# Third-party imports
from flask import (
    g,
    render_template,
    request
)


# Local application/library-specific imports
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
#from functions import (
#    db_connect,
#)



##
## Setup and Housekeeping
##
app = create_app()
#configObject=str(('settings.'+ str(os.environ.get("FLASK_ENVIRONMENT","Development"))+'Config'))
#app.config.from_object(configObject)
#app.secret_key = app.config['SECRET_KEY']
#oidc = OpenIDConnect(app)
#app.oidc = oidc  # Attach oidc to the app
#db_connection_pool = db_connect(app.config)




@app.template_filter('json_pretty')
def json_pretty_filter(value):
    if isinstance(value, str):
        value = json.loads(value)    
    return json.dumps(value, indent=4)



@app.template_filter('asint')
def asint(value):
    return int(value)



##
## Setup complete, Routes below
##

@app.route('/')
def home():
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)

## coment: delete me
