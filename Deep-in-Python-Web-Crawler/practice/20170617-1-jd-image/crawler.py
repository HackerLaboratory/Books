import re
import urllib.request

def craw(url, page):
    #下载url对应的HTML页面
    html1 = urllib.request.urlopen(url).read()
    html1 = str(html1)
    #第一层过滤，留下来图片链接信息
    pat1 = '<div id="plist".+? <div class="page clearfix">'
    result1 = re.compile(pat1).findall(html1)
    result1 = result1[0]
    #第二层过滤，获取图片真实链接
    pat2 = '<img width="220" height="220" data-img="1" data-lazy-img="//(.+?\.jpg)">'
    imagelist = re.compile(pat2).findall(result1)
    x = 1
    for imageurl in imagelist:
        #必须先在本地创建好对应的目录，否则保存文件时报错
        imagename = "./image/" + str(page) + str(x) + ".jpg"
        imageurl = "http://" + imageurl
        try:
            urllib.request.urlretrieve(imageurl, filename=imagename)
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                x += 1
            if hasa (e, "reason"):
                x += 1
        x += 1

# 测试程序，只爬取第一页
for i in range(1, 2):
    url = "http://list.jd.com/list.html?cat=9987,653,655&page=" + str(i)
    craw(url, i)
