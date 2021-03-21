import requests
import bs4
import base64

def parseBurpFile(file,cdata="request"):
    s = ""
    with open(file,"r")as file:
        s = file.readlines()
        s = "".join(s)
    soup = bs4.BeautifulSoup(s,"xml")
    arr = []
    arr.append([ base64.b64decode(el.text).decode("utf-8") for el in soup.findAll(cdata) ])
    if cdata == "request":
        return arr[0]
    else:
        return arr


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

def httptoresponse(resp):
    if not resp == '\r' and not resp == '':
        response = requests.Response()
        response.status_code=getStatus(resp)
        response.headers=getHeaders(resp)
        response._content=getContent(resp)
        return response
    return

def httptoresponses(resparr):
    responseobjects = []
    for resp in resparr:
        responseobjects.append(httptoresponse(resp))
    return responseobjects



def filetorequests(file):
    return httptorequests(parseBurpFile(file))

def filetorequest(file,index=0):
    return httptorequest(parseBurpFile(file)[index])

def filetoresponse(file):
    return httptoresponse(parseBurpFile(file,"response"))

def filetoresponses(file,index=0):
    return httptoresponses(parseBurpFile(file,"response")[index])

def getStatus(resp):
    return resp.split(" ")[1]

def getMethod(req):
    return req.split(' ')[0].replace('\r','')


def getUrl(req):
    host = getHeader(req,"Host")
    path = req.split(' ')[1]
    return "http://"+host+path


def getHeaders(req,blacklist=["Upgrade-Insecure-Request"]):
    dic = {}
    req.rstrip()
    req.replace('\r','')
    headers = req[req.find('\n')+1:-(req[::-1].find('\n')+1)].split('\n')
    for header in headers:
        if ": " in header:
            key = header.split(": ")[0]
            value = header.split(": ")[1].replace('\r','')
            if not key in blacklist:
                dic[key] = value
    return dic


def getHeader(req,key):
    return getHeaders(req)[key]


def getContent(req):
    if getMethod(req) == "POST":return req.split('\n')[-1]
    else:return
