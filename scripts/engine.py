import urllib, time, os
from urllib2 import Request, urlopen, URLError, HTTPError
# local imports
from theparser import TheParser
from browser import Browser
from random import Random
from account import Account, Stuffs, Village

# globals 
MAIN_URL = "http://s7.travian.it/"
PATH_LOGIN = MAIN_URL + "login.php"
PATH_DORF1 = MAIN_URL + "dorf1.php"
PATH_DORF2 = MAIN_URL + "dorf2.php"
PATH_BUILD = MAIN_URL + "build.php"
PATH_KARTE = MAIN_URL + "karte.php"
# statics
class Engine:
    def __init__(self,account):
        self.account = account
        self.browser = Browser()
        self.parser = TheParser()
        self.__login()
    def sendStuff(self,srcvill, dstvill,stuffs):
            # go to main site with dorfID
            legno = stuffs.legno
            argilla = stuffs.argilla
            ferro = stuffs.ferro
            grano = stuffs.grano
            print "Sending from %s to %s %swood %sclay %siron %scrop" % (srcvill.name, dstvill.name, legno, argilla,ferro,grano)
            path = PATH_DORF2 + '?newdid=' + srcvill.dorfId
            self.browser.go(path)
            path = PATH_BUILD + '?id='+srcvill.marketId
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
            self.browser.go(PATH_BUILD,data)
            print self.browser.content()
    def randomwait(self):
        time.sleep(Random().randint(0, 3))
    def __login(self):
        " Do the login trying with cookie first."
        # go to the main site
        s = ''
        cookieok = False
        try:
            f = open(os.path.join(".", self.account.cookiename), "r")
            try:
                self.account.cookie=f.read()
            finally:
                f.close()
        except IOError: 
            print "Cookie doesn't exists"
        if self.account.cookie:
            print 'Cookie exists: '+self.account.cookie
            self.browser.cookie = self.account.cookie
            try:
                self.browser.go(PATH_DORF1)
            except HTTPError, e:
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
            except URLError, e:
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            else:
                cookieok = self.parser.iscookieok(self.browser.content())
                if cookieok:
                    print 'Cookie accepted, go ahead'
        if not cookieok:
            # Login in normal way
            data = None  
            print 'Login in normal way'
            try:
                self.browser.go(PATH_LOGIN, data)
            except HTTPError, e:
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
            except URLError, e:
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            else:
                lf = self.parser.getLoginForm(self.browser.content())
                data = urllib.urlencode({"action":"dorf1.php","login":lf['loginvalue'],lf['loginform_name']:self.account.username,lf['loginform_pass']:self.account.password, lf['loginform_hidden']:'',"autologin":"ja"})
                try:
                    self.browser.go(PATH_DORF1, data)
                except HTTPError, e:
                    print 'The server couldn\'t fulfill the request.'
                    print 'Error code: ', e.code
                except URLError, e:
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                else:
                    # we store the cookie for convenience
                    s = self.browser.content() # we must call content to get the cookies (crap)
                    self.account.cookie = self.browser.cookie
                    if self.account.cookie:
                        try:
                            f = open("./"+self.account.cookiename, "w")
                        except IOError, e:
                            print 'Reason: ',e.reason
                        else:
                            try:
                                f.write(self.account.cookie)
                            finally:
                                f.close()
                    # print s
                    self.parser.parse(s)
        self.account.loggedin = True
        info = self.parser.getFirstInfos()
        for dorfid,  name in info.items():
            self.account.villages[dorfid] = Village(name,dorfid)
        # Now we get infos from any villages
        print 'Reading Villages (first time)..'
        # We also get infos on dorf1, dorf2 and Karte
        print 'Getting all the info...'
        for dorfid, village in self.account.villages.items():
            self.__updateStuffs(village)
            self.__updateFromDorf2(village)
            self.__updateFromKarte(village)
        for dorfid, village in self.account.villages.items():
            print village.name,village.production.legno,village.production.argilla,village.production.ferro,village.production.grano, village.x, village.y
    def __updateStuffs(self, village):
        url = PATH_DORF1 + "?newdid=%s" % (village.dorfId,)
        #print url
        self.randomwait()
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
    def __updateFromDorf2(self, village):
        url = PATH_DORF2+ "?newdid=%s" % (village.dorfId,)
        #print url
        self.randomwait()
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
        url = PATH_KARTE+ "?newdid=%s" % (village.dorfId,)
        self.randomwait()
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
if __name__ == '__main__':
    a = Account('http://s3.travian.uk','username','password')
    ENG = Engine(a)
    #print a.villages
    ENG.sendStuff(a.villages['150634'], a.villages['102688'], Stuffs(0, 100, 0, 0))
    #a.villages['150634'].sendStuff(a.villages['102688'], 0, 100, 0, 0) #sendStuff(self,x,y,legno,argilla,ferro,grano)
    