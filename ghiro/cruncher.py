from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import re
import urllib
import libxml2dom
# TODO: intenazionalize here
class Cruncher:
    ARGILLA = "Argilla"
    LEGNO = "Legno"
    FERRO = "Ferro"
    GRANO = "Grano"
    MARKET = "Mercato"
    def __init__(self):
        self.browser = Browser()
    def login(self,url,username,password):
        "Do the login, returns true if succeded"
        response= self.browser.open(url)
        assert self.browser.viewing_html()
        soup = BeautifulSoup(response.read())
        inputs =  soup.findAll(lambda tag: tag.has_key('class') and tag['class'] == 'fm fm110')
        print inputs[0]['name']
        self.browser.select_form(name = "snd")
        self.browser[inputs[0]['name']] = username
        self.browser[inputs[1]['name']] = password
        response = self.browser.submit()  # submit current form
        print response.geturl()
        print response.info().keys()
        #.find('Set-Cookie:')
        print response
        #if self.browser.CookieJar():
        #    return True
        return False
    def iscookieok(self, s=''):
        if s: self.parse(s)
        "Check if cookie is accepted"
        divs = self.doc.getElementsByTagName("div")
        f = False
        for div in divs: 
            f = div.getAttribute("class")=='dname'
        return f
    def getFirstInfos(self,s=''):
        "Returns first infos needed to generate the account like dorfids"
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
        "Returns first infos needed to generate the account"
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
#            print info(libxml2dom.Node_textContent)
#            s = n.getAttribute('href')
#            if s.find("?newdid=")!=-1:
#                s = s[len("?newdid="):]
#                info[s] = n.textContent
        #print stock
        #print prod
        info['stock'] = stock
        info['production'] = prod
        return info
    def getMarketId(self,s=''):
        "Returns the market id"
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