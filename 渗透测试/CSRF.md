## CSRF

CSRF，跨站请求伪造

### 漏洞成因

- 主要成因：浏览器Cookie不过期，不关闭浏览器或退出登录状态都会默认为已登录状态
- 次要成因：对请求合法性验证不严格

### 漏洞定义

来看下面一个案例

> 1、小明访问www.bank.com，登录后存入100元
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

续：https://www.freebuf.com/articles/web/341591.html