### Web必懂知识点

CSRF、SSRF、目录遍历、文件读取、文件下载、命令执行、XXE安全

SQL注入、文件上传、XSS跨站、文件包含、反序列化、代码执行、逻辑安全、未授权访问



## SQL注入

SQL注入是渗透测试中的重要攻击方式。SQL注入非常复杂，区分各种数据库类型、提交方法、数据类型等注入。

### SQL注入的工作原理

- 输入验证不足

  永远不要相信用户的输入，如果Web应用程序没有对用户输入进行验证，攻击者就可以在输入字段中插入SQL代码进行SQL注入攻击

- 拼接SQL语句

  应用程序后端通常将用户输入与SQL查询拼接在一起，形成完整的数据库查询语句，但是由于用户输入验证的不足，这很容易导致攻击者输入SQL代码来截取后端的SQL查询语句

- 执行恶意SQL

  如果应用程序没有对输入进行适当的清理或转义，恶意SQL代码将被数据库服务器直接执行，以此造成的后果通常是难以预料的

- 数据泄露或破坏

  攻击者可以利用SQL注入来查询、修改或删除数据库中的数据，或者执行数据库管理系统的系统命令，甚至通过权限修改以达成完全控制数据库服务器的目的

### SQL注入的学习要点

- 回显/盲注

  回显/无回显注入，延时盲注，布尔盲注

- 数据库类型

  Access，MySQL，MSSQL，Oracle，PostSQL，SQLite，Mongodb等

- 注入拓展

  加解密注入，JSON注入，LADP注入，DNSLog注入，二次注入，堆叠注入等

- 提交方法

  GET，POST，Cookie，Request，HTTP头等

- WAF绕过

  更改提交方式，大小写混合，解密解码类，注释符混用，等价函数替换。特殊符号混用，借助数据库特性，HTTP参数污染，垃圾数据溢出等

- 数据类型

  数字型，字符型，搜索型

- 查询方式

  SELECT，INSERT，DELETE，UPDATE，ORDER BY等

- 防御方案

  代码加载过滤，WAF产品部署等



### SQL注入原理

让我们模拟一个Web登录场景

```python
# 首先接收用户输入
username = input('用户名：')
password = input('密码：')

# 拼接后端查询语句
sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

# 传入mysql进行查询，并获取查询结果
# 假设已经创建了游标 cursor
cursor.execute(sql)
user = cursor.fetchone()

# 登录验证
if user is not None:
    print("登陆成功！")
else:
    print("登陆失败！")
```

这是一段简单的后台登录实现，现在模拟用户登录，假设数据库中存在用户`worker`，密码为`123456`

- 合法输入

  用户输入: `username = worker, password = 123456`

  则执行的SQL语句为: `SELECT * FROM users WHERE username='worker' AND password='123456'`

  数据库返回的数据为: `user = (1, 'worker', '123456')`

- 非法输入（SQL注入）

  用户输入: `username = 1' OR 1=1#, password = 1`

  则执行的SQL语句为: `SELECT * FROM users WHERE username='1' OR 1=1#' AND password='123456'`

  此时，条件查询的`username='1'`提前闭合，因为用户输入了一个单引号，所以后面`OR 1=1`被视为SQL命令直接参与条件判断，`1=1`恒为真，而后面的`#`是SQL注释符，后面的SQL语句`' AND password='123456'`不再参与判断，真实执行的SQL语句为: `SELECT * FROM users WHERE username='1' OR 1=1`，`WHERE`子句恒为真，等价于`SELECT * FROM users`

  数据库返回的数据为: `user = (1, 'worker', '123456')`

### 靶场搭建

这里使用`sqli-labs`作为靶场环境

### 判断注入点

SQL注入第一步，也是最重要的一步，就是寻找注入点，没有注入点你往哪儿注呢对吧

首先进行闭合测试，在参数后加上单双引号`'`或`"`，看网页中是否出现了SQL报错，类似于`You have an error in your SQL syntax...`，或网页出现明显变化，则存在注入点

### 判断注入类型

根据数据库类型和SQL语句构造的不同，SQL注入一般分为三种类型

#### 数字型

一般出现在通过数字（例如ID，序号等）进行查询，此时的SQL语句一般如下

```sql
SELECT * FROM users WHERE id = {id}	# 这里的{id}表示程序中的变量
```

此时变量`id`值为数字，就不能使用单双引号`'"`闭合，一般判断情况如下

- 尝试`1 AND 1=1`报错

#### 字符型

绝大部分数据库查询参数都是字符型，在数据库中，字符类型数据需要使用单双引号括起来，因此字符型注入又分为**单引号注入**和**双引号注入**

```sql
SELECT * FROM users WHERE name = '{name}'	# 单引号
SELECT * FROM users WHERE name = "{name}"	# 双引号
```

判断情况如下

- 尝试`1 AND 1=1`和`1 AND 1=2`正常
- 尝试`1' AND '1'='1`正常
- 尝试`1' AND '1'='2`无结果

#### 搜索型

### 提交方法

网站将数据传递给数据库进行查询时，通常有以下几种提交方法

GET、POST、Cookie、REQUEST、HTTP头等

- GET

  GET 适用于较短数据的提交，GET方法将数据直接写在url中，特征是url中的`?x=123`，`x`是参数名，`123`是提交的参数值

- POST

  POST 适用长数据的提交，POST方法将数据放在报文的请求体中

- Cookie

  

### ORDER BY判断字段数

在SQL语句中，可以使用`ORDER BY <字段名>`对查询结果排序

实际上，`ORDER BY`子句中，字段名等价于其在表中的列数，假设有以下表`users`

| id   | username | password |
| ---- | -------- | -------- |
| 1    | admin    | admin    |
| 2    | worker   | 12345    |
| 3    | sheep    | 12345    |

对于查询语句

```sql
SELECT * FROM users
ORDER BY username;
```

其完全等价于

```sql
SELECT * FROM users
ORDER BY 2;
```

但`ORDER BY`子句参数为字段序号时，需要匹配被查询的字段序号，而不是原表中字段序号

所以，可以使用`ORDER BY`在不需要知道字段名的情况下判断出表中的字段数量

### MySQL注入

#### 信息收集

##### 调用系统函数查询

数据库版本: `version()`

数据库名字: `database()`

数据库用户: `user()`

操作系统: `@@version_compile_os`

#### 数据注入

MySQL数据库，版本5.0及以上为**高版本**，以下为**低版本**

**低版本**MySQL数据库的表名只能通过爆破方式获取

**高版本**MySQL数据库中存在一个名为`information_schema`的数据库，用于储存记录所有数据库名、表名、列名，所以，可以通过该数据库查询到指定数据库下的表名和列名信息

`information_schema.tables`: 记录所有表名信息

`information_schema.columns`: 记录所有列名信息

其中包含字段:

| 字段名         | 内容     |
| :------------- | :------- |
| `TABLE_NAME`   | 表名     |
| `COLUMN_NAME`  | 列名     |
| `TABLE_SCHEMA` | 数据库名 |

这里没有列举出所有的字段，详情请自行查询相关信息

`information_schema.schemata`: 包含字段`schema_name`记录所有数据库名

查询指定数据库`dvwa`的`表名`的SQL语句为: 

```sql
SELECT TABLE_NAME FROM information_schema.tables
WHERE TABLE_SCHEMA = 'dvwa';
```

#### 文件读写操作

MySQL中有文件读写的操作函数，所以攻击者也可以调用这些函数进行注入攻击

`load_file()`: 读取文件，参数值为文件路径或文件名

`into outfile`或`into dumpfile`: 写入文件，将查询结果写入指定文件内，语句末尾指明文件路径或文件名

注意，写入文件需要单独配置，默认关闭写入权限



`load_file()`函数需要指定文件的绝对路径，所以我们就必须想办法获取这些文件路径

常见的路径获取方式有: 报错显示、遗留文件、漏洞报错、平台配置文件、爆破等



PHP中有一个名为`magic_guotes_gpc`的魔术引号设置，如果该设置打开，PHP会对输入数据中的单双引号、反斜线和NULL字符自动加上反斜线进行转义

*魔术引号在PHP 5.4 版本及以上正式移除*

此设置会对我们的文件读写操作造成一定影响，要绕过该设置，可以使用hex编码



同时，PHP中也存在`addslashes()`函数，作用与魔术引号一致，绕过方法也相同

#### 注入防护

上述的魔术引号和`addslashes()`可以防御简单的SQL注入

PHP也自带一些具有防护功能的函数或自定义过滤

其它编程语言同理



#### 低版本MySQL注入要点

低版本的MySQL没有`information_schema`库，所以无法便捷获取到数据库敏感信息，基本上只能使用暴破的方式获取信息



