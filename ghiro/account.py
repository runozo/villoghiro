"This is the account object. I t record the player datas and the villages datas"
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
