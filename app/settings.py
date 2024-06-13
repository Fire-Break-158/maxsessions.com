import os

class Config(object):
        MQTT_BROKER = {
        'Address': '172.16.10.10',
        'Port': 1883
    }

    
class ProductionConfig(Config):
    TESTING = False
    DEBUG = False    



class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True

    
    
class TestingConfig(Config):
    TESTING = True
    DEBUG = False    



