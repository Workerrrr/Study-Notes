### Linux基本常识

#### 一、Linux简介

Linux系统诞生于1991年, 由芬兰大学生林纳斯·托瓦兹(Linus Torvalds)开创, 开源后和众多志同道合的爱好者通过开发完成

Linux是一套开源的, 免费的多用户, 多任务, 支持多线程和多CPU的操作系统

Linux有着众多的发行家族和发行版, 例如`Debian`家族下有`Ubuntu`、`Linux Mint`, `Fedora`家族下有`CentOS`、`Oracle Linux`, `SUSE`家族下有`openSUSE`等等

#### 二、Linux目录结构

Linux系统的重要概念是一切皆`文件`, 无论硬件、软件都通过`文件`形式进行访问

Linux的文件系统与Windows不同, 是以根目录`\`为起点, 展开一个层次化的目录结构, 以下是一些主要的根目录下的子目录(二级目录)及用途

- `/bin`
存放着最基本的命令二进制文件，这些命令是系统启动和运行所必需的

- `/root`
系统管理员（超级用户）的主目录, 它包含例如`/root/Desktop`等文件夹

- `/boot`
包含启动Linux时使用的核心文件，如内核文件和启动引导程序

- `/etc`
系统配置文件存放目录，这里包含了系统的大部分配置文件

- `/dev`
设备文件的存放地，Linux中的设备如硬盘、USB等都以文件形式存在于此

- `/var`
存放经常变化的文件，如日志文件

- `/lib`
存放系统最基本的动态链接共享库，类似于Windows中的DLL文件

- `/usr`
用户的很多应用程序和文件都放在这个目录下, 它包含了许多子目录，如`/usr/bin`、`/usr/sbin`、`/usr/local`等

- `/home`
用户的主目录，通常以用户的账户名命名

- `/media`
可移动媒体设备的挂载点，如U盘、CD-ROM等


在Linux中, 还有几个特殊目录符号需要牢记

- `~(波浪号)`
代表当前登录用户的主目录, 例如`/home/username`

- `/(斜杠)`
代表根目录, 是所有目录的起点

- `.(点号)`
代表当前目录

- `..(两个点)`
代表上一级目录

### Linux常用命令

在学习Linux命令之前, 当然需要一个Linux系统环境, 这里讲解使用Windows自带工具`WSL(Windows Subsystem for Linux)`搭建Linux环境

官方教程网站:[https://learn.microsoft.com/zh-cn/windows/wsl/install](https://learn.microsoft.com/zh-cn/windows/wsl/install "Microsoft Learn")

本笔记使用`Ubuntu 24.04.1 LTS`

现在, 让我们进入Linux

#### 一、文件处理

- `ls` 显示当前目录下所有文件
```
ls	显示当前目录下所有文件
ls <path>	显示指定目录下的文件
ls -l	列表形式显示文件
ls -a	显示所有文件(包括隐藏文件夹)
ls -h	以字节形式显示文件大小
```

每个选项都可以组合使用

- `mkdir` 创建目录
```
mkdir <path_name>	创建目录
mkdir -p	递归创建子目录
```

如果想要创建类似于`1/2/3`的目录结构, 则需要使用`-p`选项
```
mkdir 1/2/3 -p
```

可以是使用`find`命令查看是否创建成功

- `cd` 切换目录
```
cd <path>	切换目录
cd ..	返回上级目录
```

`cd`命令可以使用绝对和相对路径

可以使用`pwd`命令查看现在所处的目录位置

- `touch` 创建文件
```
touch <file_name>	创建文件
```

- 打开文件
```
cat <file_name>		正序显示所有文件内容
tac <file_name>		倒序显示所有文件内容

more <file_name>	显示文件部分内容
less <file_name>	显示文件部分内容

head <file_name>	显示文件头几行内容
tail <file_name>	显示文件尾几行内容
```

其中`cat`命令可以使用选项`-n`显示行号, `head`和`tail`命令可以使用选项`-数字`指定行数

- `cp` 复制文件
```
cp <old> <new>	复制文件或目录
cp <name> <path>	复制文件或目录到指定目录
cp -r <path>	递归复制其子目录内的所有内容
```

- `mv` 剪切文件
```
mv <name> <path>	剪切文件或目录到指定目录
```

`mv`命令还可以完成重命名操作
```
mv 1.py 2.py	将文件 1.py 改名为 2.py
```

- `rm` 删除文件
```
rm <file_name>	删除文件
rm -f <file_name>	强制删除文件
rm -r <path>	递归删除目录以及其下所有文件
```

`rm`命令**非常危险**, 请一定确定好文件或目录正确

*`rm -rf /*`删库跑路*

- `vim` 文本编辑器
```
vim <name>	用文本编辑器打开文件
```

`vim`是用文本编辑器打开文件, 如果文件不存在, 则直接创建

在命令模式下使用"hjkl"控制光标"左下上右"移动, 也可以使用方向键

在命令模式下, 按下`i`进入编辑模式, 再按下`Esc`返回命令模式

在命令模式下, 按下`:`进入ex命令, 输入`w`保存, `q`退出, `/<key>`查找关键字, `n`向下查找关键字, `N`向上查找关键字

- `find` 文件查找
```
find <path> <condition>	按条件在范围内进行查找
```

查找范围默认为当前目录

以下是各种条件
```
find -name <file_name>	按照文件名查找文件

find -amin <n>		查找在过去 n 分钟内被读取过的文件
find -anewer <file>	查找比文件 file 更晚读取过的文件
find -atime <n>		查找在过去 n 天内被读取过的文件

find -cmin <n>		查找在过去 n 分钟内被修改过的文件
find -cnewer <file>	查找比文件 file 更晚修改过的文件
find -ctime <n>		查找在过去 n 天内被修改过的文件

find -type f	按文件进行查找
find -type d	按目录进行查找
find -type l	按链接进行查找
```

#### 二、权限管理

在此之前, 我们需要先了解Linux的权限机制

Linux文件权限针对三类对象进行定义

分别是 owner属主 缩写为`u`, group属组 缩写为`g`, other其他 缩写为`o`

每个文件又针对每类访问者定义了三种主要权限

`r`: Read 读取, `w`: Write 写入, `x`: eXecute 执行

而针对文件和目录, `rwx`又有着不同的作用与含义
```
对于文件
r: 读取文件内容
w: 修改文件内容
x: 执行权限对除二进制程序以为的文件没有什么意义

对于目录
r: 查看目录下的文件列表
w: 删除和创建目录下的文件
x: 可以cd进目录, 能查看目录下文件的详细属性, 能访问目录下的文件内容(基础权限)
```

linux系统内的文件权限由一串字符表示, 使用命令`ls -l`即可在文件前方看到其权限信息
```
eiousee@Workerrrr-Laptop:~$ ls -l
total 0
-rw-r--r-- 1 eiousee eiousee   32 Mar 25 19:01 1.txt
drwxr-xr-x 1 eiousee eiousee 4096 Mar 25 20:00 test2
```

前面的`-rw-r--r--`和`drwxr-xr-x`就是文件权限的字符表示

第一个字符表示文件类型, `-`为文件, `d`为目录

其后每**3**个字符为一组, 分别表示该文件的**属主**、**属组**、**其他**的访问权限

`drwxr-xr-x`表示, 该文件是目录, 属主的权限是`rwx`, 属组的权限是`r-x`, 其他的权限是`r-x`

在linux内可能还会以文件名称颜色来区分文件类型

**`root`用户可以无视权限操作**

- `chmod` 更改文件权限
```
chmod +<n> <name>	为所有人增加指定文件或目录的<n>权限
chmod -<n> <name>	为所有人删除指定文件或目录的<n>权限

chmod -R <n>+<m> <name>	为指定访问者<n>增加指定文件或目录的<m>权限
chmod -R <n>-<m> <name>	为指定访问者<n>删除指定文件或目录的<m>权限
```

文件权限也可以使用数字表示, 每个访问者用一个三位二进制数表示, 比如`rwx`则为`111`, 在使用时转换为十进制数`7`, 所以对于权限`rwxr--r--`则可以表示为`744`, `-wxr-xrw-`则可以表示为`356`

#### 三、压缩解压

- 压缩和解压文件
```
该命令只能操作文件, 不能操作目录, 且压缩后不保留原文件
gzip <name>	压缩文件为gz格式
gzip -d <name>	解压gz文件

zip需要额外安装
zip <output_name> <name>	压缩目录下的所有文件为zip格式
zip -r <output_name> <name>	递归压缩目录下的所有文件为zip格式
unzip <name>	解压zip文件

tar -zcf <output_name> <name>	压缩目录下的所有文件为tar.gz格式
tar -zxvf <name>	解压tar.gz文件
```

#### 四、网络命令

- `ping` 测试网络连通性

- `ifconfig` 查看当前网络配置信息

- `nestat` 显示网络相关配置
```
netstat -tlun	查看本机监听的所有端口
netstat -rn	查看本机路由表
netstat -anp	列出所有端口信息
netstat -anpt	查看TCP端口信息
```

#### 五、进程命令

- `ps` 查看系统进程
```
ps aux	列出全部进程
ps aux | grep <name>	查找<name>相关的所有进程
ps -u <name>	查找用户<>的进程
```

- `crontab` 计划任务
```
crontab -l	列出系统的计划任务
crontab -e	进入编辑模式
crontab -u <name> -e	编辑用户<name>的计划任务
```

#### 六、其他命令
```
uname -a	查看当前系统内核信息

whoami	查看当前登录用户
id	查看当前用户信息
last	查看用户登录记录
lastlog	查看所有用户最后一次登录信息

useradd <name>	添加用户<name>
userdel	<name>	删除用户<name>
passwd <name>	设置用户<name>的密码

history	查看历史操作命令
```