import  urllib2,httplib
from StringIO import StringIO
import gzip

USER_AGENT="Mozilla/5.0 (Windows; U; Windows NT 6.0; ja; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14"
ACCEPT="text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5"
ACCEPT_LANGUAGE="ja,en-us;q=0.7,en;q=0.3"
ACCEPT_ENCODING="gzip,deflate"
ACCEPT_CHARSET="Shift_JIS,utf-8;q=0.7,*;q=0.7"
KEEP_ALIVE="300"
CONNECTION = "keep-alive"
REFERER = "http://www.google.it"

class ReDirHandler(urllib2.HTTPRedirectHandler):
    AUTOREDIRECTION=False
    def http_error_301(self, req, fp, code, msg, headers):
        if AUTOREDIRECTION ==False:
            return urllib2.HTTPError(req,"200","OK",headers,fp )
        return urllib2.HTTPRedirectHandler.http_error_301(
                    self, req, fp, code, msg, headers)
    def http_error_302(self, req, fp, code, msg, headers):
        if AUTOREDIRECTION ==False:
            return urllib2.HTTPError(req,"200","OK",headers,fp )
        return urllib2.HTTPRedirectHandler.http_error_302(
                    self, req, fp, code, msg, headers)


class Browser(object):
    def __init__(self,url="",agent=USER_AGENT,accept=ACCEPT,accept_lang=ACCEPT_LANGUAGE,accept_enc=ACCEPT_ENCODING,accept_charset=ACCEPT_CHARSET, keep_alive=KEEP_ALIVE, con=CONNECTION,referer=REFERER):
        self.url=url
        self.cookie = ''
        self.headers = { "User-Agent": agent, "Accept": accept , "Accept-Language" : accept_lang , "Accept-Encoding" : accept_enc , "Accept-Charset" : accept_charset , "Keep-Alive": keep_alive , "Connection": con,'Referer':referer}
        self.etag=None
        self.lastmodified=None
        self.referer = REFERER
    def go(self,u=None,data=None,referer=REFERER):
        "Opens a URL"
        if u == None:
            u = self.url
        self.url = u
        httplib.HTTPConnection.debuglevel=1
        if self.referer:
            self.headers['Referer'] = self.referer
        if self.etag:   
            self.headers['If-None-Match'] = self.etag                                                                 
        if self.lastmodified:                                                            
            self.headers['If-Modified-Since'] = self.lastmodified
        if self.cookie:
            self.headers['Cookie'] = self.cookie
        self.request=urllib2.Request(self.url,data,self.headers)
        for i in self.headers:
           if len(self.headers[i]) > 0:
               self.request.add_header(i,self.headers[i])
        op=urllib2.build_opener(ReDirHandler())
        self.response = op.open(self.request)
        self.referer = self.response.url
    def content(self):
        "Get the response content"
        s = self.response.read()
        if hasattr(self.response, 'headers'):
            self.lastmodified = self.response.headers.get('Last-Modified')
            self.etag =  self.response.headers.get('ETag')
            if self.response.headers.get('content-encoding', '') == 'gzip':
                # data came back gzip-compressed, decompress it          
                s = gzip.GzipFile(fileobj=(StringIO(s))).read()
            if self.response.headers.get('set-cookie'): #we set the cookie
                cooki = self.response.headers.get('Set-Cookie')
                self.cookie = cooki
        return s
