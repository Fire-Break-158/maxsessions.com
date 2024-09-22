import os

    

class ProductionConfig(Config):
    APP_ENVIRONMENT = 'Production'
    TESTING = False
    DEBUG = False    



class DevelopmentConfig(Config):
    APP_ENVIRONMENT = 'Software Development'
    TESTING = True
    DEBUG = True