import urllib.request, hashlib
def get(u):
    req=urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'})
    r=urllib.request.urlopen(req,timeout=30)
    return r.read(), r.headers.get('Content-Type')
for u in ['https://octodex.github.com/favicon.ico','https://github.com/favicon.ico','https://octodex.github.com/images/original.png']:
    try:
        b,ct=get(u)
        print(u, len(b), ct, hashlib.md5(b).hexdigest())
    except Exception as e:
        print(u,'ERR',e)
