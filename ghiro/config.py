#!/usr/bin/env python
#
# Copyright 2007 Ghiro.
#
# This software VilloGhiro is licensed under the GNU GPL License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.gnu.org/licenses/gpl.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""A convenient way to read the program configuration"""
import os
from BeautifulSoup import BeautifulStoneSoup

class Config:
    """Base class to read from the config file"""
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
     

