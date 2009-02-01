import os
class Config:
    """ Reads the config file at init and evaluates the Config's methods & properties"""
    def __init__(self,configfile=os.sep.join((os.pardir,'config','config.xml'))):
        print configfile