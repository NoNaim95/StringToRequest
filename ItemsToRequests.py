import requests
import bs4
import base64

def parseFile(file):
    s = ""
    with open(file,"r")as file:
        s = file.readlines()
        s = "".join(s)
    soup = bs4.BeautifulSoup(s,"xml")
    arr = []
    arr.append([ base64.b64decode(el.text).decode("utf-8") for el in soup.findAll('request') ])
    return arr[0]



def httptorequest(req):
    request = requests.Request(
            method=getMethod(req),
            url = getUrl(req),
            headers=getHeaders(req),
            data=getContent(req)
            )
    return request

def httptorequests(reqarr):
    requestobjects = []
    for req in reqarr:
        requestobjects.append(httptorequest(req))
    return requestobjects


def getMethod(req):
    return req.split(' ')[0]


def getUrl(req):
    host = getHeader(req,"Host")
    path = req.split(' ')[1]
    return host+path


def getHeaders(req,blacklist=[]):
    dic = {}
    req.rstrip()
    req.replace('\r','')
    headers = req[req.find('\n')+1:-3].split('\n')
    for header in headers:
        key = header.split(": ")[0]
        value = header.split(": ")[1]
        if not key in blacklist:
            dic[key] = value
    return dic


def getHeader(req,key):
    return getHeaders(req)[key]


def getContent(req):
    if getMethod == "POST":return req.split('\n')[-1]
    else:return


#httptoreq(parseFile("/tmp/items"))

reqs = parseFile("/tmp/items")
for req in httptorequests(reqs):
    print(req.headers["User-Agent"])
    print("\n\n")
