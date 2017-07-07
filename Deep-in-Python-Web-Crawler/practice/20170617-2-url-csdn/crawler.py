"""
1.确定要爬取的入口链接
2.根据需求构建好链接提取的正则表达式
3.模拟成浏览器并爬取对应网页
4.根据步骤2中的正则表达式提取出该网页中包含的链接
5.过滤掉重复链接
6.后续操作，比如输出或者保存这些链接
"""

import re
import urllib.request

def getlink(url):
    #模拟成浏览器
    headers=("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    #将opener安装为全局
    urllib.request.install_opener(opener)
    file = urllib.request.urlopen(url)
    data = str(file.read())
    #根据需求构建好链接正则表达式
    pat = '(https?://[^\s)";]+\.(\w|\/)*)'
    link = re.compile(pat).findall(data)
    #去除重复元素
    link = list(set(link))
    return link

#要爬取的网页链接
url = "http://blog.csdn.net/"
#获取对应网页包含的链接地址
linklist = getlink(url)
#通过for循环分别遍历输出获取的链接
for link in linklist:
    print(link[0])

