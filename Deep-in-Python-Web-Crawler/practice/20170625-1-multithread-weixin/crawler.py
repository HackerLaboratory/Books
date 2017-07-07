import re
import urllib.request
import time
import urllib.error
import threading
import queue

urlqueue = queue.Queue()
#模拟成浏览器
headers=("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
opener = urllib.request.build_opener()
opener.addheaders = [headers]
#将opener安装为全局
urllib.request.install_opener(opener)
#设置一个列表存储文章网址列表
listurl = []

#自定义函数，功能为使用代理服务器
def use_proxy(proxy_addr, url):
    #建立异常处理机制
    try:
        import urllib.request
        proxy = urllib.request.ProxyHandler({'http':proxy_addr})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(url).read().decode('utf-8')
        #print(data)，经常会因为频繁访问要求输入验证码，导致无法正常下载，这里print(data)就会看到原因，所以如何应对反爬虫机制还是比较有难度
        return data
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        #若为URLError异常，延时10s执行
        time.sleep(10)
    except Exception as e:
        print("exception:" + str(e))
        #若为Exception异常，延时1s执行
        time.sleep(1)

#线程1，专门获取对应网址并处理为真实网址
class geturl(threading.Thread):
    def __init__(self, key, pagestart, pageend, proxy, urlqueue):
        threading.Thread.__init__(self)
        self.pagestart = pagestart
        self.pageend = pageend
        self.proxy = proxy
        self.urlqueue = urlqueue
        self.key = key
    def run(self):
        page = self.pagestart
        #编码关键词key
        keycode = urllib.request.quote(key)
        #编码"&page"
        pagecode = urllib.request.quote("&page")
        #循环爬取各页的文章链接
        for page in range(self.pagestart, self.pageend+1):
            #分别构建各页的URL链接，每次循环构建一次
            url = "http://weixin.sogou.com/weixin?type=2&query=" + keycode + pagecode + str(page)
            #用代理服务器爬取，解决IP被封杀的问题
            data1 = use_proxy(self.proxy, url)
            #获取文章链接的正则表达式
            listurlpat = '<div class="txt-box">.*?(http://.*?)"'
            #获取每页的所有文章链接并添加到listurl中
            listurl.append(re.compile(listurlpat, re.S).findall(data1))
        print("共获取到" + str(len(listurl)) + "页")
        for i in range(0, len(listurl)):
            #等一等线程2，合理分配资源
            time.sleep(7)
            for j in range(0, len(listurl[i])):
                try:
                    url = listurl[i][j]
                    #处理成真实url
                    url = url.replace("amp;", "")
                    print("第" + str(i) + "i" + "第" + str(j) + "j次入队")
                    self.urlqueue.put(url)
                    self.urlqueue.task_done()
                except urllib.error.URLError as e:
                    if hasattr(e, "code"):
                        print(e.code)
                    if hasattr(e, "reason"):
                        print(e.reason)
                    #若为URLError异常，则延时10s执行
                    time.sleep(10)
                except Exception as e:
                    print("exception:" + str(e))
                    time.sleep(1)

#线程2，与线程1并行执行，从线程1提取的文章网址中依次爬取对应的文章信息并处理
class getcontent(threading.Thread):
    def __init__(self, urlqueue, proxy):
        threading.Thread.__init__(self)
        self.urlqueue = urlqueue
        self.proxy = proxy
    def run(self):
        #设置本地文件中的开始html编码
        html1 = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title>微信文章页面</title>
            </head>
            <body>'''
        fh = open("./result.html", "wb")
        fh.write(html1.encode("utf-8"))
        fh.close()
        #再次以追加写入的方式打开文件，以写入对应文章内容
        fh = open("./result.html", "ab")
        while(True):
            try:
                url = self.urlqueue.get()
                data = use_proxy(self.proxy, url)
                #文章标题正则表达式
                titlepat = "<title>(.*?)</title>"
                #文章内容正则表达式
                contentpat = 'id="js_content">(.*?)id="js_sg_bar"'
                #通过对应正则表达式找到标题并赋值给列表title
                title = re.compile(titlepat).findall(data)
                #获取内容
                content = re.compile(contentpat).findall(data)
                #初始化标题和内容
                thistitle = "此次没有获取到"
                thiscontent = "此次没有获取到"
                #如果标题列表不为空，说明找到标题，取列表第0个元素
                if(title != []):
                    thistitle = title[0]
                if(content != []):
                    thiscontent = content[0]
                #将标题与内容汇总给变量dataall
                dataall = "<p>标题：" + thistitle + "</p><p>内容：" + thiscontent + "</p><br>"
                #将该篇文章的标题和内容写入文件
                fh.write(dataall.encode("utf-8"))
                print("第" + str(i) + "个网页的第" + str(j) + "次处理")
            except urllib.error.URLError as e:
                if hasattr(e, "code"):
                    print(e.code)
                if hasattr(e, "reason"):
                    print(e.reason)
                #若为URLError异常，则延时10s执行
                time.sleep(10)
            except Exception as e:
                print("exception:" + str(e))
                time.sleep(1)
        fh.close()
        html2 = '''</body>
            </html>'''
        fh = open("./result.html", "ab")
        fh.write(html2.encode("utf-8"))
        fh.close()

#并行控制线程，若60s无响应，并且存url的队列为空，则判断为执行成功
class conrl(threading.Thread):
    """docstring for conrl"""
    def __init__(self, urlqueue):
        super(conrl, self).__init__()
        self.urlqueue = urlqueue
    def run(self):
        while(True):
            print("程序执行中")
            time.sleep(60)
            if(self.urlqueue.empty()):
                print("执行完毕")
                exit()

#设置关键词
key = "物联网"
#设置代理服务器，若实效，需要换成新的代理服务器，如果程序运行有问题，基本上就是代理服务器实效，在urlopen的地方卡住！
#proxy = "119.50.3.117:8118"
proxy = "58.241.58.41:808"
#可以为getlisturl()与getcontent()设置不同的代理服务器，这里没有启动该选项
proxy2 = ""
#起始页
pagestart = 1
#爬到哪页
pageend = 2
#创建线程1，并启动
t1 = geturl(key, pagestart, pageend, proxy, urlqueue)
t1.start()
#创建线程2，并启动
t2 = getcontent(urlqueue, proxy)
t2.start()
#创建线程3冰启动
t3 = conrl(urlqueue)
t3.start()

