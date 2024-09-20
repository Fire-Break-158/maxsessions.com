##
## Library Imports
##

# Standard library imports
import datetime
import functools
import json
import signal
import sys
import os
import time
import traceback

from queue import Queue

# Third-party imports
#import psycopg2
#import requests

from flask import (
    g,
    render_template,
    request
)
#from flask_oidc import OpenIDConnect
#from oauth2client.client import OAuth2Credentials
#from werkzeug.exceptions import NotFound

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
configObject=str(('settings.'+ str(os.environ.get("FLASK_ENVIRONMENT","Development"))+'Config'))
app.config.from_object(configObject)
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



#@app.errorhandler(Exception)
#def handle_error(e):
#    # Check if the error is a 404 and retrieve the original URL
#    original_url = None
#    if isinstance(e, NotFound):
#        original_url = request.url
#
#    # This error handler will handle exceptions not caught by a try/except block
#    rootUrl=request.url_root
#    previousUrl = request.referrer if request.referrer else request.url_root
#
#    # Modify the message to include the original_url for 404 errors
#    if original_url:
#        message = f"Could not find the requested page: {original_url}. Please try again by going <a href='{previousUrl}'>back</a> to the previous page or return to the <a href='{rootUrl}'>Backoffice Home</a>"
#    else:
#        message = f"Please try again by going <a href='{previousUrl}'>back</a> to the previous page or return to the <a href='{rootUrl}'>Backoffice Home</a>"
#
#    trace = traceback.format_exc()
#    exc_type, exc_value, exc_traceback = sys.exc_info()
#    traceback_details = traceback.format_exception(exc_type, exc_value, exc_traceback)
#    formatted_traceback = ''.join(traceback_details)
#    debugInfo = f'''
#    <b>Debugging Information Below:</b><br>
#    <pre>
#    {formatted_traceback}
#    </pre>
#    '''
#    print(f"{str(e)}\n {str(message)}\n {str(debugInfo)}")
#    return render_template('response.html', responseType='Error', data=str(e), data2=message, data3=debugInfo, sideMenu=False)





#def with_postgres_connection(func):
#    @functools.wraps(func)
#    def wrapper(*args, **kwargs):
#        # Acquire a connection from the pool
#        global db_connection_pool  # Declare as global
#        conn = db_connection_pool.getconn()
#        if conn is None:
#            return "Failed to acquire PostgreSQL connection"
#        try:
#            # Pass the connection to the wrapped function
#            kwargs['db'] = conn
#            result = func(*args, **kwargs)
#        except psycopg2.OperationalError as e:
#            if str(e) == "server closed the connection unexpectedly":
#                # Reestablish the connection pool and connection
#                db_connection_pool = dbConnect(app.config)
#                conn = db_connection_pool.getconn()
#                kwargs['db'] = conn
#                result = func(*args, **kwargs)
#            else:
#                # Reraise the exception if it's not the expected error
#                raise
#        finally:
#            # Release the connection back to the pool
#            db_connection_pool.putconn(conn)
#        return result
#    return wrapper



##
## Setup complete, Routes below
##

@app.route('/')
def home():
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)

## coment: delete me
