'''完整展示Python3.X的urllib模块的各种用法
'''
import urllib
import urllib.request
import urllib.parse

url = "http://coolshell.cn/"
postdata = urllib.parse.urlencode({
"s":"xumenger"
}).encode("utf-8")

req = urllib.request.Request(url, postdata)
req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

try:
    data = urllib.request.urlopen(req).read()
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.reason)
    data = e.reason
except urllib.error.URLError as e:
    print (e.reason)
    data = e.reason

fhandle = open("./result.html", "wb")
fhandle.write(data)
fhandle.close()

