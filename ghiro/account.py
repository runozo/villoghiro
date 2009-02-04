class Account:
    def __init__(self,mainurl, username, password):
        self.mainurl = mainurl
        self.username = username
        self.password = password
        self.cookie = ''
        self.cookiename = "cookie_%s_%s" % (username, mainurl[7:9])
        self.logger = None
        self.loggedin = False
        self.villages = {}
        #attr_writer 
        self.cancelImageName = '' #the name of the image which is used to cancel a job. (looks like a red X)
        self.nightmode = False #set TRUE if the bot should build during the night
        self.mainurl = mainurl
        # self.logname = "%s-&s" % (username,url.host.to_s[0..url.host.to_s.index(".")-1])
class Village:
    def __init__(self, name,dorfId,stockStuff={},prodStuff={},destDorfId=None,browser=None,parser=None):
        self.dorfId = dorfId
        self.name = name
        self.dorfId = dorfId
        self.stock = stockStuff
        self.production = prodStuff
        self.scrocco = destDorfId
        self.marketId = ''
        self.browser = browser
        self.parser = parser
        self.x = None
        self.y = None
class Stuffs:
    def __init__(self,legno,argilla,ferro,grano):
        self.legno = legno
        self.argilla = argilla
        self.ferro = ferro
        self.grano = grano
