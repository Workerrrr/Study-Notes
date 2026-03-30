## DVWA

### Brute Force（暴力破解）

#### Low

![image-20260330145134383](C:\Users\Worker\AppData\Roaming\Typora\typora-user-images\image-20260330145134383.png)

展示一个常见的登录页面，首先尝试正常登录

输入用户名和密码都输入`1`

![image-20260330145505497](C:\Users\Worker\AppData\Roaming\Typora\typora-user-images\image-20260330145505497.png)

网页提示用户名或密码错误，观察URL，发现参数传递

![image-20260330145553735](C:\Users\Worker\AppData\Roaming\Typora\typora-user-images\image-20260330145553735.png)

说明该页面使用GET方法传参，使用Yakit抓包

