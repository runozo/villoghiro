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
"""This is the engine of the application. It takes decisions and do actions accordingly."""
import urllib, time, os
from urllib2 import Request, urlopen, URLError, HTTPError
# local imports
from cruncher import Cruncher

from random import Random
from account import Stuffs, Village

class Engine:
    def __init__(self,account):
        self.account = account
        self.cruncher = Cruncher()
        self.cruncher.login()
    def sendStuff(self,srcvill, dstvill,stuffs):
        """Send stuff from srcvill to dstvill
        Args:
            srcvill: Village source village
            dstvill: Village destination village
            stuffs: Stuffs amounts of stuffs
        """
        # go to main site with dorfID
        legno = stuffs.legno
        argilla = stuffs.argilla
        ferro = stuffs.ferro
        grano = stuffs.grano
        print "Sending from %s to %s %swood %sclay %siron %scrop" % (srcvill.name, dstvill.name, legno, argilla,ferro,grano)
        path = self.PATH_DORF2 + '?newdid=' + srcvill.dorfId
        self.browser.go(path)
        path = self.PATH_BUILD + '?id='+srcvill.marketId
        self.browser.go(path)
        s = self.browser.content()
        f = open("./dorf2_"+srcvill.dorfId, "w")
        f.write(s)
        f.close()
        capacity = self.parser.getMarketCapacity(s)
        data = urllib.urlencode({'action':'build.php','id':srcvill.marketId,'r1':legno,'r2':argilla,'r3':ferro,'r4':grano,'s1':'ok','s1.x':Random().randint(0, 30),'s1.y':Random().randint(0, 30), 'x':dstvill.x, 'y':dstvill.y})
        self.browser.go(path,data)
        vars = self.parser.getSendStuffVars(self.browser.content())
        print "kid=%s sz=%s cap=%s" % (vars['kid'],vars['sz'], capacity)
        #resp, data = http.post(path, data, $header);
        data = urllib.urlencode({'id':srcvill.marketId,'a':srcvill.dorfId,'sz':vars['sz'],'kid':vars['kid'],'r1':legno,'r2':argilla,'r3':ferro,'r4':grano,'s1.x':Random().randint(0, 30),'s1.y':Random().randint(0, 30),'s1':'ok'})
        self.browser.go(self.PATH_BUILD,data)
        print self.browser.content()
    def randomWait(self):
        """Waits a random amount of time"""
        time.sleep(Random().randint(0, 3))
    def __updateStuffs(self, village):
        url = self.PATH_DORF1 + "?newdid=%s" % (village.dorfId,)
        #print url
        self.randomWait()
        self.browser.go(url)
        #f = open("./"+dorfid, "w")
        #f.write(self.browser.content())
        #f.close()
        #print self.browser.content()
        vinfo = self.parser.getVillageInfos(self.browser.content())
        stock = vinfo['stock']
        prod = vinfo['production']
        village.stock = Stuffs(stock[TheParser.LEGNO],stock[TheParser.ARGILLA],stock[TheParser.FERRO],stock[TheParser.GRANO])
        village.production = Stuffs(prod[TheParser.LEGNO],prod[TheParser.ARGILLA],prod[TheParser.FERRO],prod[TheParser.GRANO])
    
    
