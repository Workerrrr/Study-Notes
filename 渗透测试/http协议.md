### HTTP协议简介

#### 一、什么是HTTP协议

HTTP(HyperText Transfer Protocol), 超文本传输协议, 它是在web服务器和客户端直接进行数据传输的规则, 它是一个**无状态**的**应用层**协议

*ISO七层网络模型背了吗?*

HTTPS(HyperText Transfer Protocol over SecureSocket Layer), 是以安全为目标的HTTP通道, 在HTTP基础上通过传输加密和身份认证保证了传输过程的安全性

#### 二、HTTP协议工作原理

在用户访问 https://www.baidu.com/index.html 时, 浏览器(客户端)和Web服务器执行了以下操作:

> - 浏览器分析超链接中的URL
> - 浏览器向DNS服务器请求解析 www.baidu.com 的IP地址
> - DNS服务器将解析出的IP地址(假设) 220.181.38.148 返回浏览器
> - 浏览器与Web服务器建立TCP连接(80或443端口)
> - 浏览器请求文档: GET /index.html
> - Web服务器响应请求, 将文档 index.html 发送给浏览器
> - 释放TCP连接
> - 浏览器显示 index.html 中的内容

![text](img/1.png)

#### 三、持久性与非持久性连接

- **非持久性连接**

浏览器每请求一个Web文档, 就建立一个新的连接, 当文档传输完毕后, 连接就立即释放

HTTP0.9, HTTP1.0 采用此连接方式

非持久性连接对于请求的Web网页内包含多个文档对象(如图像、视频等), 由于每个文档都要创建新的连接, 所以效率底下

- **持久性连接**

在一个连接中, 可以进行多次文档请求和响应, 服务器在发送完响应后, 不会立即释放连接, 连接的保持时间由双方协商

HTTP1.1 版本之后均采用此连接方式



### HTTP报文分析

要获取HTTP报文, 需要使用到抓包工具, 常用的抓包工具有`Burp Suite`、`Wireshark`、`Fiddler`等, 我使用的是国产工具`Yakit`

`Yakit`下载地址: [https://www.yaklang.com/en/](https://www.yaklang.com/en/ "Yakit 下载地址")

具体的使用方式这里不作讲解, 请自行学习

#### 一、HTTP报文结构

- HTTP请求报文

由客户端发送给Web服务器的报文称为**请求报文**

首先, 我们来看看HTTP请求报文和其结构

![alt text](img/2.png)

```
POST /cm/api/fees/pc HTTP/1.1
Host: cm.bilibili.com
Connection: keep-alive
Content-Length: 337
sec-ch-ua-platform: "Windows"
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36
Accept: application/json
sec-ch-ua: "Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"
Content-Type: application/json
sec-ch-ua-mobile: ?0
Origin: https://www.bilibili.com
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://www.bilibili.com/
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9
Cookie: buvid3=14F30C7C-851E-9E9E-6454-65C77CD3FF9702905infoc; b_nut=1742705302; b_lsid=F10DE9CAA_195C1549A7D; _uuid=53DCB1710-52F4-4BC10-4BB9-B10351EAE1079902148infoc; buvid_fp=d435c85e8d107c65b399916f9979500a; enable_web_push=DISABLE; enable_feed_channel=ENABLE; home_feed_column=5; browser_resolution=1536-738; buvid4=B8430857-2FF2-8C01-553E-913BDCDBF14D04437-025032304-832iXTx9B8FyFjbbVNhA1KQ%2B6VYJAo1D6IzO%2B9V10tGubZ%2F6%2Fy4W7RMymBxsSFri; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDI5NjQ1MDUsImlhdCI6MTc0MjcwNTI0NSwicGx0IjotMX0.69LHTxtBTdkyf_RdxhpqCspugoR5gKfBNfcvdsyuSdU; bili_ticket_expires=1742964445

{"uploads":[{"src_id":4697,"track_id":"","up_mid":"","ad_server":"bilibili","is_ad":0,"area":1,"ad_cb":"","event":"strict_show","is_visible":1,"idx":3,"mid":"","client_version":"","ts":1742705315258,"resource_id":4694,"load_ts":1742705302235,"server_type":0,"id":1667222,"event_from":"","request_id":"1742705303072q172a27a49a136q9791"}]}
```

*每条报文的内容不同, 但结构一样*

我们来仔细分析一下这条报文

- 第一行, `请求行`

`POST`就是请求方法, 后面的`/cm/api/fees/pc`就是`URL`, `HTTP/1.1`就是`版本号`

- 第二行到倒数第三行, `请求头`

`Host`、`Connection`、`Content-Length`等在每一行开头并且后面紧跟一个冒号的字符串就是`头部字段名`, 又称`首部`

冒号后的就是`值`, 或称`域值`

- 最后一行, `请求包体`

`{"uploads":[{"src_id":4697,"track_id":"...`这一长串就是请求数据

*GET方法没有请求数据*

- HTTP响应报文

Web服务器收到请求信息, 向客户端返回的就是**响应报文**

HTTP响应报文的结构

![alt text](img/3.png)

```
HTTP/1.1 200 OK
Access-Control-Allow-Credentials: true
Access-Control-Allow-Headers: Content-Type
Access-Control-Allow-Methods: POST, GET
Access-Control-Allow-Origin: https://www.baidu.com
Content-Type: application/json; charset=utf-8
Date: Sun, 23 Mar 2025 03:59:42 GMT
Set-Cookie: BAIDUID_BFESS=018CC923A04CD7D1EDC27173D2F91964:FG=1; Path=/; Domain=baidu.com; Expires=Mon, 23 Mar 2026 03:59:42 GMT; Max-Age=31536000; Secure; SameSite=None
X-Bfe-Svbbrers: MjQwODo4NDYyOjZlMzA6M2U3ZjphODBjOjM3ZGU6YjBiMTo3MTU5,1.0
Content-Length: 44

{"error":"0","logid":"11426950237717382465"}
```

跟请求报文一样, 响应报文也有明确的结构划分

- 第一行, `状态行`

`HTTP/1.1`就是`协议版本`, `200`就是`状态码`, `OK`就是`状态码描述`

- 第二行到倒数第三行, `响应头`

与请求报文一样, 响应报文中的响应头同样是由`Key: Value`结构组成的数据

- 最后一行, `响应包体`

#### 二、HTTP请求方法

HTTP请求报文中, 共有8种请求方法, 后5种是HTTP/1.1版本新增请求方法

- GET
请求指定页面信息, 返回实体主体

- POST
向指定资源提交数据进行处理请求(比如提交表单和上传文件). 数据被包含在请求体中, POST请求可能会导致新的资源的建立或已有资源的修改

- HEAD
向服务器索要与GET请求一致的响应, 但响应体不会被返回(只返回状态行和响应头). 这一方法可以在不必传输整个响应内容的情况下, 就可以获取包含在响应头中的元信息

- PUT
向指定资源位置上传其最新内容

- DELETE
请求服务器删除Request-URI(请求行中的URL)所标识的资源

- OPTIONS
返回服务器针对特定资源所支持的HTTP请求方法, 也可以利用向Web服务器发送"*"请求来测试服务器功能性

- TRACE
回显服务器收到的请求, 主要用于测试或诊断

- CONNET
HTTP/1.1协议中预留给能够将连接改为管道方式的代理服务器

#### 三、HTTP状态码

状态码(Status-Code)是响应报文状态行中包含的一串3位数字, 指明特定的请求是否被满足, 如果没有满足, 原因是什么. 状态码分为以下五类

HTTP状态码分类

- 1XX
信息性状态码(Informational), 服务器正在处理请求

- 2XX
成功状态码(Success), 请求已正常处理完毕

- 3XX
重定向状态码(Redirection), 需要进行额外操作以完成请求

- 4XX
客户端错误状态码(Client Error), 客户端原因导致服务器无法处理请求

- 5XX
服务器错误状态码(Server Error), 服务器原因导致处理请求出错

需要牢记的状态码

> 200 请求被服务器正常处理(最常见)
> 
> 301 永久重定向，资源已永久分配新URL
> 
> 302 临时重定向，资源已临时分配新URL
> 
> 401 需要通过HTTP认证，或认证失败
> 
> 403 请求资源被拒绝
> 
> 404 无法找到请求资源
> 
> 500 服务器故障或Web应用故障
> 
> 503 服务器超负荷或停机维护

HTTP状态码大全:[https://www.runoob.com/http/http-status-codes.html](https://www.runoob.com/http/http-status-codes.html "HTTP状态码大全")

#### 四、HTTP头部

HTTP请求和响应报文都有头部信息, 它们由一些头字段和值组成

**请求头**

以下是常见的请求头

- User-Agent
客户端的浏览器或平台信息(Mozilla、Chrome、Safari等)

- Accpet
用户能处理的页面类型(text/html、image/webp等)

- Accpet-Charset
用户可以接受的字符集(Unicode-1-1、UTF-8、GB2312等)

- Accpet-Encoding
用户能处理的页面编码方式(gzip、deflate、zstd等)

- Accpet-Language
用户能处理的自然语言(zh-CN、zh等)

- Host
服务器的DNS名称, 从URL提取出来, 必需

- Referer
用户从该URL代表的页面出发访问当前请求的页面

- Cookie
将以前设置的Cookie送回服务器, 可用来作为会话信息

- Date
消息被发送时的日期和时间

**响应头**

常见的响应头

- Date
消息被发送时的日期和时间

- Server
Web服务器的信息, (nginx、Microsoft IIS/6.0等)

- Content-Encoding
内容的编码方式(gzip、deflate、zstd等)

- Content-Language
内容所使用的自然语言(zh-CN、zh等)

- Content-Length
以字节计算的内容长度

- Content-Type
内容的MIME类型

- Last-Modified
页面最后被修改的时间和日期, 在页面缓存机制中意义重大

- Location
指示客户端将请求发往别处, 即重定向到另一个URL

- Set-Cookie
服务器希望客户端保存一个Cookie



### HTTP协议中的URL

#### 一、什么是URL

**URL定义**

`URL`即`Uniform Resource Location`, 中文名为`统一资源定位符`

`URL`是从互联网上获取资源位置和访问方法的一种简洁表示, 是互联网上标准资源的地址. 类似于快递地址, 互联网上每一个文件都有一个唯一的URL

**URL格式**

先来看一段完整的URL有哪些结构

```
protocol://[username:password@]hostname[:port][/path][;params][?query][#frag]
```

很长对吧? 我们来解析一下

- `protocol` 协议
常见的协议有`http`、`https`、`ftp`等

- `username:password` 用户名和密码
在某些情况下, URL需要提供用户名和密码才能访问, 并使用`@`连接后面的`host`

- `hostname` 主机地址
可以是`IP地址`或者`域名`

- `port` 端口号
这是服务器指定的服务端口, 有些URL中没有端口, 因为它们使用了`默认端口`, 比如`http`协议的默认端口是`80`

- `path` 路径
指网络资源在服务器中的指定位置

- `params` 参数
用来指定访问某个资源时的附加信息

- `query` 查询
顾名思义用来查询某类资源，如果有多个查询，则用`&`隔开

- `fragment` 片段
它是对资源描述的部分补充，可以理解为资源内部的书签, 又称为`锚点`

本笔记的URL结构划分可能与其他说法不同, 只要能够学习理解那就都是正确的

**URL协议**

这里详细介绍一下常见的URL协议

- http 超文本传输协议
- https 用安全套接字层传送的超文本传输协议
- ftp 文件传输协议
- mailto 电子邮件地址
- ldap 轻型目录访问协议
- file 本地电脑或网上分享的文件
- news Usenet新闻组
- gopher Gopher协议
- telnet 远程登录协议

#### 二、URL编码

URL只能使用**ASCII**字符集来通过互联网进行传输

URL编码使用`%`其后紧跟两位的十六进制数来替换非ASCII字符

URL不能包含空格, 通常使用`+`来代替空格

只有英文字母和数字(a~z, A~Z, 0~9), 除双引号外的特殊符号, 以及某些保留字才可以不经过转换直接用于URL

比如使用浏览器搜索中文内容, 虽然地址栏中显示了中文, 但将链接复制到文本编辑器中, 你会发现链接中并没有中文

![alt text](img/4.png)

实际上的链接

```
https://cn.bing.com/search?pglt=129&q=CTF%E6%95%99%E7%A8%8B
```

所有的中文被转换为了`%两位十六进制数`的形式

#### 三、同源策略

**同源策略(SOP)**

所谓同源, 是指域名、协议、端口三者相同
同源策略是浏览器(客户端)行为, 为了保护本地数据不被JavaScript代码获取回来的数据污染

如果没有同源策略, 那么在 A.com 加载过的js脚本, 就能在没有加载过这个脚本的 B.com 上的页面中随意执行并被读取, 可能造成页面排版混乱或数据窃取等不安全的行为

![alt text](img/5.png)