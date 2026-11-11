import base64, urllib.request, sys

def murmur3_32(data, seed=0):
    data = bytearray(data)
    length = len(data)
    nblocks = length // 4
    h1 = seed
    c1 = 0xcc9e2d51
    c2 = 0x1b873593
    for i in range(nblocks):
        k1 = data[i*4] | (data[i*4+1] << 8) | (data[i*4+2] << 16) | (data[i*4+3] << 24)
        k1 = (k1 * c1) & 0xffffffff
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xffffffff
        k1 = (k1 * c2) & 0xffffffff
        h1 ^= k1
        h1 = ((h1 << 13) | (h1 >> 19)) & 0xffffffff
        h1 = (h1 * 5 + 0xe6546b64) & 0xffffffff
    tail = data[nblocks*4:]
    k1 = 0
    if len(tail) >= 3:
        k1 ^= tail[2] << 16
    if len(tail) >= 2:
        k1 ^= tail[1] << 8
    if len(tail) >= 1:
        k1 ^= tail[0]
        k1 = (k1 * c1) & 0xffffffff
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xffffffff
        k1 = (k1 * c2) & 0xffffffff
        h1 ^= k1
    h1 ^= length
    h1 ^= h1 >> 16
    h1 = (h1 * 0x85ebca6b) & 0xffffffff
    h1 ^= h1 >> 13
    h1 = (h1 * 0xc2b2ae35) & 0xffffffff
    h1 ^= h1 >> 16
    if h1 >= 2**31:
        h1 -= 2**32
    return h1

def icon_hash(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    content = urllib.request.urlopen(req, timeout=30).read()
    b64 = base64.encodebytes(content)
    return murmur3_32(b64)

for u in ['https://fofa.info/favicon.ico','https://octodex.github.com/favicon.ico','https://www.baidu.com/favicon.ico']:
    try:
        print(u, icon_hash(u))
    except Exception as e:
        print(u, 'ERR', e)
