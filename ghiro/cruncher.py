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
"""The HTML markup cruncher."""
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import re
import urllib
import libxml2dom

class Cruncher:
    def __init__(self):
        self.browser = Browser()
    def login(self,url,username,password):
        """Do the login
        Args:
            url: the url of the popular-web-based-game login page
            username: the username for the popular-web-based-game
            password: the password for the popular-web-based-game
        Returns:
            Bool if success or not
        """
        self.MAIN_URL = url # initialize some stuff
        self.PATH_LOGIN = self.MAIN_URL + "/login.php"
        self.PATH_DORF1 = self.MAIN_URL + "/dorf1.php"
        self.PATH_DORF2 = self.MAIN_URL + "/dorf2.php"
        self.PATH_BUILD = self.MAIN_URL + "/build.php"
        self.PATH_KARTE = self.MAIN_URL + "/karte.php"
        response= self.browser.open(url)
        assert self.browser.viewing_html()
        soup = BeautifulSoup(response.read())
        # inputs =  soup.findAll(lambda tag: tag.has_key('class') and tag['class'] == 'fm fm110')
        inputs =  soup.findAll(lambda tag: (tag.has_key('type') and (tag['type'] == 'text' or tag['type'] == 'password')))
        print inputs[0]['name']
        self.browser.select_form(name = "snd")
        self.browser[inputs[0]['name']] = username
        self.browser[inputs[1]['name']] = password
        response = self.browser.submit()  # submit current form
        print response.geturl()
        try:
            print "(%s) Accepted cookie: %s" % (username,response.info()['Set-Cookie'])
            return True 
        except KeyError:
            print "(%s) Login failed!" % (username,)
        return False
    def iscookieok(self, s=''):
        """Check if cookie is accepted
        Args:
            s: The markup to be parsed
        Returns:
            Bool if the cookie was accepted or not
        """
        if s: self.parse(s)
        
        divs = self.doc.getElementsByTagName("div")
        f = False
        for div in divs: 
            f = div.getAttribute("class")=='dname'
        return f
    def getFirstInfos(self,s=''):
        """Gets the list of all the dorfIDS
        Args:
            s: The markup to be parsed
        Returns:
            Dictionary containig the key/value dorfID/villagename
        """
        if s: self.parse(s)
        info = {} 
        ns = self.doc.getElementsByTagName("a")
        for n in ns:
            #print info(libxml2dom.Node_textContent)
            s = n.getAttribute('href')
            if s.find("?newdid=")!=-1:
                s = s[len("?newdid="):]
                info[s] = n.textContent #The village name is in textContent and the villageID in s
        return info
    def getVillageCoords(self, s=''):
        """Returns the coordinates of a village
        Args:
            s: The markup to be parsed
        Returns:
            Dictionary containig the coordinates
        """
        if s: self.parse(s)
        # we try to get village coordinates
        c = {}
        nx = self.doc.getElementById("x")
        ny = self.doc.getElementById("y")
        #print nx.textContent, ny.textContent
        c['x'] = nx.textContent
        c['y'] = ny.textContent
        return c
    def getVillageInfos(self,s=''):
        """Returns first infos needed to generate the account
        Args:
            s: The markup to be parsed
        Returns:
            Dictionary "info" containig another dict for the stocks and the production of a village
        """
        if s: self.parse(s)
        info,prod,stock = {},{self.LEGNO:'',self.ARGILLA:'',self.FERRO:'',self.GRANO:''},{self.LEGNO:'',self.ARGILLA:'',self.FERRO:'',self.GRANO:''}
        ns = self.doc.getElementsByTagName("td")
        i = 0
        for n in ns:
            # Get the stock
            if n.getAttribute('id')=='l4': stock[self.LEGNO] = n.textContent
            if n.getAttribute('id')=='l3': stock[self.ARGILLA] = n.textContent
            if n.getAttribute('id')=='l2': stock[self.FERRO] = n.textContent
            if n.getAttribute('id')=='l1': stock[self.GRANO] = n.textContent
            # Get the production rate
            if n.textContent == self.ARGILLA+':':
                m = re.search('-*[\d]+',ns[i+1].textContent)
                prod[self.ARGILLA] = m.group(0)
            if n.textContent == self.LEGNO+':':
                m = re.search('-*[\d]+',ns[i+1].textContent)
                prod[self.LEGNO] = m.group(0) 
            if n.textContent == self.FERRO+':':
                m = re.search('-*[\d]+',ns[i+1].textContent)
                prod[self.FERRO] = m.group(0) 
            if n.textContent == self.GRANO+':':
                m = re.search('-*[\d]+',ns[i+1].textContent)
                prod[self.GRANO] = m.group(0)  
            i += 1
        info['stock'] = stock
        info['production'] = prod
        return info
    def getMarketId(self,s=''):
        """Returns the market id
        Args:
            s: The markup to be parsed
        Returns:
            None if the market couldn't be found
            String with the ID of the market 
        """
        if s: self.parse(s)
        found = False
        t,tmp = '',''
        ns = self.doc.getElementsByTagName("area")
        #print len(self.MARKET)
        #exit()
        for n in ns:
            t = n.getAttribute('title') 
            if t:
                if len(t)>len(self.MARKET):
                    if t[0:len(self.MARKET)]==self.MARKET:
                        tmp = n.getAttribute('href')
                        found = True
                        break
        if found: 
            return tmp[len('buid.php?id=')+1:len(tmp)]
        else:
            return None
    def getSendStuffVars(self,s=''):
        if s: self.parse(s)
        vars = {}
        c = 0
        ns = self.doc.getElementsByTagName("input")
        for n in ns:
            t = n.getAttribute('name')
            if t:
                if t == 'kid': 
                    t = n.getAttribute('value')
                    vars['kid']=t
                if t == 'sz':
                    t = n.getAttribute('value')
                    vars['sz']=t
        return vars
    def getMarketCapacity(self, s=''):
        if s: self.parse(s)
        c = 0
        ns = self.doc.getElementsByTagName("b")
        for n in ns:
            try:
                if ns.textContent:
                    try:
                        c= int(ns.textContent)
                        if c>=500:
                            return c
                    except ValueError:
                        pass
            except AttributeError:
                pass
    def __updateFromDorf2(self, village):
        url = self.PATH_DORF2+ "?newdid=%s" % (village.dorfId,)
        #print url
        self.randomWait()
        self.browser.go(url)
        sx = self.browser.content()
        s = self.parser.getMarketId(sx)
        if s: 
            village.marketId = s
            print '%s market Id: %s' % (village.name,village.marketId)
        f = open("./dorf2_"+village.dorfId, "w")
        f.write(sx)
        f.close()
        #print self.browser.content()
    def __updateFromKarte(self, village):
        url = self.PATH_KARTE+ "?newdid=%s" % (village.dorfId,)
        self.randomWait()
        self.browser.go(url)
        sx = self.browser.content()
        s = self.parser.getVillageCoords(sx)
        f = open("./dorf2_karte_"+village.dorfId, "w")
        f.write(sx)
        f.close()
        if s: 
            #print '%s X:%s | Y:%s' % (village.name, s['x'], s['y'])
            village.x = s['x']
            village.y = s['y']