## CSRF

CSRF，跨站请求伪造

### 漏洞成因

- 主要成因：浏览器Cookie不过期，不关闭浏览器或退出登录状态都会默认为已登录状态
- 次要成因：对请求合法性验证不严格

### 漏洞定义

来看下面一个案例

> 1、小明访问银行网站www.bank.com，登录后存入100元
>
> 2、小明存钱后，未关闭网站的情况下，浏览其它网站，发现了一个网站有100元的RTX4090显卡，于是打开该网站
>
> 3、小明打开网站后，发现只有4090的散热器，大失所望，遂离开网站
>
> 4、小明再次返回www.bank.com时，发现刚刚存的100元竟不翼而飞

这个过程如何实现呢？

假设小明点击的网站有以下代码

```html
<html>
  <body>
  <script>history.pushState('', '', '/')</script>
    <form action="http://www.bank.com" method="POST">
      <input type="hidden" name="money" value="100" />
      <input type="hidden" name="submit" value="submit" />
    </form>
  </body>
</html>
```

当用户访问该页面时，自动提交了一个表单，内容是将100元转出，而表面什么都没有

攻击者利用小明进入自己的恶意网站时携带的银行网站的Cookie，让小明自己在不经意间向银行网站提交了一份转账申请，而使用的是小明自己的合法Cookie，于是银行判断是小明本人，执行转账操作

整个过程攻击者都没有主动操作，仅依靠小明自己的操作就可以完成攻击

### CSRF分类

#### GET 类型

仅仅需要一个HTTP请求，就能构造一次简单的CSRF

假设某银行网站转账通过GET请求来完成

```text
http://www.bank.com/transfer.php?uid=1001&money=100
```

用户`uid`为`1001`的账户转账`100`元，转给谁不用在意

某恶意网站的HTML包含以下代码

```html
<img src=http://www.bank.com/transfer.php?uid=1001&money=100>
```

看起来是一张图片文件，但是资源地址却是银行网站的转账地址

如果你先登录银行网站，在没有退出登录的情况下访问恶意网站，此时会出现以下情况

你的浏览器中还保存有银行网站的合法Cookie，打开恶意网站，浏览器会自动通过GET请求第三方资源，这与你自己手动打开对应资源的地址是一致的；对于上述代码，也就相当于你手动打开转账链接进行转账

银行网站并不会察觉到你的请求异常，因为该请求携带的是你浏览器保存的合法Cookie，于是银行执行转账操作，你的钱就不翼而飞了

#### POST 类型

POST相比GET更加麻烦一点，但不多

GET请求是浏览器自动执行，而POST请求则需用户主动提交

这难不倒我们，假设某恶意网站有以下代码

```html
<form action="http://www.bank.com/transfer.php" method=POST>
<input type="text" name="uid" value="1001">
<input type="text" name="money" value="100">
</form>
<script> document.forms[0].submit() </script>	// 自动提交表单
```

当用户访问恶意网站后，表单会自动提交，相当于模拟用户完成了一次POST操作

同样，也可以使用`hidden`隐藏表单数据，比如

```html
<input type="hidden" name="uid" value="1001">
<input type="hidden" name="money" value="100">
<input type="submit" name="submit" value="点击参与抽奖">
```

页面只会显示一个“点击参与抽奖”的按钮，点击就会提交数据

*不要相信天生掉馅饼*

#### CSRF利用

