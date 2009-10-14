"The config class reads and write the config file and keeps relative data in memory for processing"
import os
from BeautifulSoup import BeautifulStoneSoup

class Config:
    """ Reads the config file at init and evaluates the Config's methods & properties"""
    def __init__(self,configfile=os.path.join(os.path.basename( __file__),os.pardir,'config','config.xml')):
        print os.path.abspath(configfile)
        try:
            f = open(os.path.abspath(configfile), "r")
        except IOError:
            print "Config file not found or unreadable (%s)" % (os.path.abspath(configfile),)
        else:
            if os.path.exists(configfile):
                soup = BeautifulStoneSoup(f.read())
                #inputs =  soup.findAll(lambda tag: tag.has_key('class') and tag['class'] == 'fm fm110')
                print "Config file found, parsing.."
            self.mainurl = "http://"
            self.accounts = []
     

