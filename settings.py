import os

##
## This is the "new" configuration method...
## There are a lot of hard coded values throughout backoffice.py that need to me moved into here
##
## Also, sorting between production and test values would be a nice TODO
##


class TestingConfig(Config):
    TESTING = True
    DEBUG = False    



