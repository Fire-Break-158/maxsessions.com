##
## Library Imports
##

# Standard library imports
import json
import os
import sys

from datetime import (
    datetime, 
    timedelta
)
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from queue import Queue
from time import sleep


# Third-party imports
import psycopg2.pool
import requests

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import OAuth2Credentials
from simple_salesforce import Salesforce

# Local application/library-specific imports



##
## Class Definitions
##
class SalesforcePool:
    def __init__(self, config):
        self.max_size = config.get('MAX_POOL_SIZE', 5)
        self._credentials = {
            'username': config['SFUSER'],
            'password': config['SFPASS'],
            'security_token': config['SFTOKEN'],
            'domain': config['SFDOMAIN']
        }
        self._pool = Queue(maxsize=self.max_size)
        for _ in range(self.max_size):
            self._pool.put(self._create_connection())

    def _create_connection(self):
        return Salesforce(**self._credentials)

    def get_connection(self):
        return self._pool.get()

    def return_connection(self, connection):
        self._pool.put(connection)



##
## Utility Functions
##
def custom_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, timedelta):
        return str(obj)  # or, e.g., obj.total_seconds() if you prefer seconds
    raise TypeError ("Type %s not serializable" % type(obj))




def db_connect(config):
    db_connection_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=config['MAX_POOL_SIZE'],
        dbname=config['DBNAME'],
        user=config['DBUSER'],
        password=config['DBPASS'],
        host=config['DBHOST'], 
        port=config['DBPORT']
    )
    return(db_connection_pool)




def read_bit(number,index):
    #return the nth bit from x (counting from 0 from right)
    return (number >> index & 1)




def resultify_cursor(cursor):
   columns = [column[0] for column in cursor.description]
   results = []
   for row in cursor.fetchall():
      results.append(dict(zip(columns,row)))
   return(results)



def get_oidc_user_permissions(oidc):
    rawinfo = {}
    info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])
    username = info.get('preferred_username')
    email = info.get('email')
    user_id = info.get('sub')
    if user_id in oidc.credentials_store:
        access_token = OAuth2Credentials.from_json(oidc.credentials_store[user_id]).access_token
        headers = {'Authorization': 'Bearer %s' % (access_token)}
        rawinfo =  dict(json.loads(requests.get('https://keycloak.pacificbattleship.com/auth/realms/nmsn/protocol/openid-connect/userinfo', headers=headers).text)) #TODO: Hardcoded info!
    if 'client_roles' not in rawinfo.keys():
        rawinfo['client_roles'] = []
    return (rawinfo['client_roles'])



def get_oidc_user_info(oidc):
    userInfo = {}
    info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])
    user_id = info.get('sub')

    if user_id in oidc.credentials_store:
        access_token = OAuth2Credentials.from_json(oidc.credentials_store[user_id]).access_token
        headers = {'Authorization': 'Bearer %s' % (access_token)}
        userInfo = json.loads(requests.get('https://keycloak.pacificbattleship.com/auth/realms/nmsn/protocol/openid-connect/userinfo', headers=headers).text)    
    return (userInfo)



def set_bit(number, index, x):
    #Set the index:th bit of number to 1 if x is truthy, else to 0, and return the new value.
    mask = 1 << index       # Compute mask, an integer with just bit 'index' set.
    number &= ~mask         # Clear the bit indicated by the mask (if x is False)
    if x:
        number |= mask      # If x was True, set the bit indicated by the mask.
    return (number)         # Return the result, we're done.


















