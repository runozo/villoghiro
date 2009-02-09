import os
from BeautifulSoup import BeautifulStoneSoup

class Config:
    """ Reads the config file at init and evaluates the Config's methods & properties"""
    def __init__(self,configfile=os.path.join(os.pardir,'config','config.xml')):
        print configfile
        if os.path.exists(configfile):
            soup = BeautifulStoneSoup(open(configfile, "r").read())
            #inputs =  soup.findAll(lambda tag: tag.has_key('class') and tag['class'] == 'fm fm110')
            print "Config file found, parsing.."
        self.mainurl = "http://"
        self.accounts = []
     

