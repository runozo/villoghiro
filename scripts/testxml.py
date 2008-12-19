import libxml2dom

from theparser import TheParser

def info(object, spacing=10, collapse=1):
    """Print methods and doc strings.
    
    Takes module, class, list, dictionary, or string."""
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print "\n".join(["%s %s" %
                      (method.ljust(spacing),
                       processFunc(str(getattr(object, method).__doc__)))
                     for method in methodList])
s = ''
try:
    f = open("./dorf2_145926", "r")
    try:
        s=f.read()
    finally:
        f.close()
except IOError, e:
    print 'Errore: ',e.reason 
    exit()
else:
    p = TheParser()
    print p.getMarketId(s)
    #print info(libxml2dom.Document)
    #print p.getFirstInfos(s)
#    p.parse(s)
#    ns = p.doc.getElementsByTagName("a")
#    for n in ns:
#        #print info(libxml2dom.Node_textContent)
#        s = n.getAttribute('href')
#        if s.find("?newdid=")!=-1:
#            s = s[len("?newdid="):]
#            print s,n.textContent
    
