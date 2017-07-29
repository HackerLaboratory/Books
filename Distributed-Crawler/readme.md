>来自课程[《分布式爬虫实战》](http://www.chinahadoop.cn/course/944)

# 爬虫的基础技术

* Python环境搭建及基础类
* HTML相关技术：HTLM、CSS、JavaScript
* HTTP协议及Python的DOM树选择器
* 宽度与深度抓取介绍及比较
* 不重复抓取策略以及BloomFilter
* 网站结构分析
* 马蜂窝网页抓取案例

### HTTP、HTML、CSS、JS

HTTPS是以安全为目标的HTTP通道，通常讲是HTTP的安全版，即HTTP下加入SSL层，HTTPS的安全基础是SSL

HTML、CSS、JavaScript我之前都了解过，也都写过简单的前端应用，所以不在这里多说了，详细可以自己再去[w3school](http://www.w3school.com.cn/)学一下

直接在浏览器的开发者工具中打开Console，根据JavaScript的语法可以进行网页元素的筛选处理

![image](./image/01.png)

DOM树最重要的作用是用来做网页数据分析及提取，我们可以充分利用TAG、CLASS、ID来找出某一类或某一个元素并提取出内容

![image](./image/02.png)

>分析、提取网页内容的时候，XPATH、正则表达式是极其高效的！

Javascript做网络请求的时候最常用的技术称为AJAX（Asynchronous JavaScript and XML），专门用来异步请求数据，要在网络爬虫中处理这些技术就相对复杂一些了！

[20170716-crawler-big-data-hash](https://github.com/HackerLaboratory/_Math/tree/master/20170716-crawler-big-data-hash)有讲到在网页量极大的情况下该如何处理！

# 登录及动态网页的抓取

* 网站结构分析及案例：马蜂网（Robots.txt、网站地图）
* 数据清洗和内容提取时主要用到的工具：XPath、正则表达式
* 动态网页
* Headless的浏览器：PhantomJS
* 浏览器的驱动：Selenium

### 网站结构

Robots.txt里面存储的是网站对于爬虫进行的限制：哪些你可以爬，哪些不要爬

获取网站URL继续进行静态页面抓取的方法有多种：

1.从首页开始下载，解析每个下载页面中的<a>标签
2.网站地图中会有该网站全站的所有URL，所以可以直接通过网站地图解析获取所有的URL并存储到数据库，然后逐个进行抓取即可
3.自己分析URL寻找出格式、规律，然后可以根据规律生成URL！寻找页面HTML、URL格式的规律是在做爬虫的时候非常重要的步骤！

静态网页可以理解为通过一个HTTP Request就能完全获取到的，而动态网页中一部分内容是通过JS动态加载的，无法直接通过HTTP Request直接获取，因为JavaScript需要自己的运行环境。在爬虫开发中对于动态网页的爬取比较进阶的部分就是要提供Javascript的运行环境以动态抓取网页

### 网页解析：XPath、正则

XPath的基础语法

表达式   |描述
---------|-----
nodename |选取此节点的所有子节点，tag或\*选择任意的tag
/        |从根节点选取，选择直接子节点，不包含更小的后代（例如孙、重孙）
//       |从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置，包含所有后代
.        |选取当前节点
..       |选取当前节点的父节点
@        |选取属性

在爬虫的解析中，经常会将正则表达式与DOM选择器结合使用。正则表达式适用于字符串特征比较明显的情况，但是同样的正则表达式可能在HTML源码中多次出现；而DOM选择器可以通过class、id精确地找到DOM块，从而缩小查找的范围

### 动态网页

动态网页的使用场景

* 单页模式：不需要外部跳转的网页，例如个人设置中心经常就是单页
* 页面交互多的场景：一部分网页上，有很多的用户交互接口，例如去哪儿的机票选择网页，用户可以反复修改查询的参数
* 内容及模块丰富的网页：有些网页内容很丰富，一次加载完对服务器压力很大，而且这种方式延时也会很差；用户往往也不会查看所有内容

动态网页带来的挑战

* 对于爬虫
    * 简单下载HTML已经不行了，必须得有一个Web容器来运行JS，由JS来实现动态加载
    * 增加了爬取的时间
    * 增加了计算机CPU、内存的资源消耗
    * 增加了爬取的不确定性
* 对于网站
    * 为了配合搜索引擎的爬取，与搜索相关的信息会采用静态方式
    * 与搜索无关的信息，例如商品的价格、评论，仍然会使用动态加载

分析动态网页的方法很简单

* 用【网页，全部】和【网页，仅HTML】两种方式保存网页
* 然后使用B compare等文本对比工具对比两种方式保存的网页内容
* 如果【网页，全部】有某个内容，而【网页，仅HTML】没有，基本可以说明这部分是动态加载的
* 比如京东上商品的价格是使用JavaScript动态加载的
    * 因为价格是可能变化的，所以不能写死在静态页面中
    * 那它既可以在后台生成HTML的时候由后台语言Java、PHP或Python查询数据库或缓存中的价格来在后台生成HTML
    * 也可以后台生成的HTML中该部分是空的，用户进行HTTP Request后，再由JavaScript进行动态加载
    * 如果是前者，对于爬虫来说直接解析HTML即可，而如果是后者就需要在爬虫环境中运行JavaScript来获取这部分内容，显然后者难度更大

### Python Web引擎

PyQt PySide是基于QT的Python Web引擎，需要图形界面的支持，需要安装大量的依赖。安装和配置复杂，尤其是安装图形系统，对于服务器来说代价很大

Selenium是一个自动化的Web测试工具，可以支持包括FireFox、Chrome、PhatomJS、IE等多种浏览器的连接和测试

PhantonJS是一个基于Webkit的Headless的Web引擎，支持JavaScript。相比于PyQT等方案，phamtoms可以部署在没有UI的服务器上

Selenium通过浏览器的驱动，支持大量的HTML及JavaScript的操作，常用的可以包括：

* page_source：获取当前的HTLM文本
* title：HTML的title
* current_url：当前网页的URL
* get_cookie() & get_cookies()：获取当前的cookie
* delete_cookie() & delete_all_cookies()：删除所有的cookie
* add_cookie()：添加一段cookie
* set_page_load_timeout()：设置网页超时
* execute_script()；同步执行一段JavaScript命令
* execute_async_script：异步执行JavaScript命令

### 提取动态数据

加载的过程中，根据网络环境的优劣，会存在一些延时，因此要多次尝试提取，提取不到不意味着数据不存在或者网络出错

动态页面的元素，所使用的id或class经常会不止一个，例如京东一件商品的“好评率”，class包括rate和percent-con两种，因此需要对两种情况都进行尝试。更通用的情况，如果一个元素不能找到而selenium并没有抱网络错误，那么有可能这个元素的class或id有了新的定义，我们需要将找不到的页面及元素信息记录在日志中，使得后续可以分析，找出新的定义并对这一类页面重新提取信息

