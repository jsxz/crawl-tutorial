# coding:utf8
import http.cookiejar,urllib.request
filename='cookie.txt'
cookie=http.cookiejar.LWPCookieJar(filename)
handler=urllib.request.HTTPCookieProcessor(cookie)
opener=urllib.request.build_opener(handler)
res=opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True,ignore_expires=True)