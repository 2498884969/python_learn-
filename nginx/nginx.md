## 一、环境安装

```shell
# 关闭防火墙selinux
# selinux
getenforce # 获取seLinux状态
setenforce 0
# 
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux # 永久关闭，需要重启
# 永久关闭防火墙
systemctl stop firewalld.service
systemctl disable firewalld.service
# 安装必要的安装包
yum -y install gcc gcc-c++ autoconf prce prce-devel make automake
yum -y install wget httpd-tools vim
# 初始化目录
cd /opt && mkdir app download logs work backup
# 源代码url
https://git.imooc.com/coding-121/coding-121
```

### 1.2 源码安装

```shell
tar -xzvf nginx-release-1.12.1.tar.gz

./auto/configure --prefix=/root/nginx/share --sbin-path=/root/nginx/sbin --modules-path=/root/nginx/modules

rpm -ql pcre  # 查看pcre安装目录


错误1：./configure: error: the invalid value in --with-ld-opt="-Wl,-z,relro -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -Wl,-E"

解决方法：yum -y install redhat-rpm-config.noarch

错误2：./configure: error: the HTTP image filter module requires the GD library.

解决方法： yum -y install gd-devel

错误3：./configure: error: perl module ExtUtils::Embed is required

解决方法： yum -y install perl-devel perl-ExtUtils-Embed
```





## 二、基础

### 2.2 http基础

```shell
curl -v http://www.imooc.com/ > /dev/null
# 将输出内容重定向到空设备当中仅仅输出头部信息
```

### 2.3 CPU亲和

```shell
cpu亲和是一种把cpu核心和Nginx工作进程绑定方式,把每个worker进程固定在一个cpu上执行,减少切换cpu的cahce miss(cpu高速缓存),获得更好的性能
```

### 2.4 sendfile

```shell
# 零拷贝的传输模式
请求一个文件要经过操作系统的内核空间->用户空间最终到达socket,socket再response给用户
```

![](./send_file.png)

nginx：

![](C:\Users\Administrator\Desktop\python_learn-\nginx\nginx_send_file.png)

### 2.5 快速安装

```shell
yum install nginx
```

### 2.6 配置文件和编译参数

```shell
rpm -ql nginx 列出配置文件的目录
nginx -V 查看编译信息
```



1. 安装目录

| 路径                     | 类型     | 作用                                     |
| ------------------------ | -------- | ---------------------------------------- |
| /etc/logrotate.d/nginx   | 配置文件 | nginx日志轮转，用于logrorate日志切割     |
| /etc/nginx/mime.types    | 配置文件 | 设置http协议的Content-Type与扩展名的关系 |
| /usr/lib64/nginx/modules |          | 模块                                     |
| /var/log/nginx           |          | 日志目录                                 |

2. 编译参数

```
--prefix=/usr/share/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --http-client-body-temp-path=/var/lib/nginx/tmp/client_body --http-proxy-temp-path=/var/lib/nginx/tmp/proxy --http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi --http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi --http-scgi-temp-path=/var/lib/nginx/tmp/scgi --pid-path=/run/nginx.pid --lock-path=/run/lock/subsys/nginx --user=nginx --group=nginx --with-file-aio --with-ipv6 --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-stream_ssl_preread_module --with-http_addition_module --with-http_xslt_module=dynamic --with-http_image_filter_module=dynamic --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_slice_module --with-http_stub_status_module --with-http_perl_module=dynamic --with-http_auth_request_module --with-mail=dynamic --with-mail_ssl_module --with-pcre --with-pcre-jit --with-stream=dynamic --with-stream_ssl_module --with-google_perftools_module --with-debug --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -m64 -mtune=generic' --with-ld-opt='-Wl,-z,relro -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -Wl,-E'

# with 代表nginx启用的模块
--prefix=/usr/share/nginx 
--sbin-path=/usr/sbin/nginx 
--modules-path=/usr/lib64/nginx/modules 
--conf-path=/etc/nginx/nginx.conf 
--error-log-path=/var/log/nginx/error.log 
--http-log-path=/var/log/nginx/access.log 
--http-client-body-temp-path=/var/lib/nginx/tmp/client_body 
--http-proxy-temp-path=/var/lib/nginx/tmp/proxy 
--http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi 
--http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi 
--http-scgi-temp-path=/var/lib/nginx/tmp/scgi 
--pid-path=/run/nginx.pid 
--lock-path=/run/lock/subsys/nginx
```



| 编译选项                                                     | 作用 |
| ------------------------------------------------------------ | ---- |
| --prefix=/usr/share/nginx |  安装的目的目录或者路径  |
| --user=nginx --group=nginx | 设置nginx启动的用户和用户组 |
|                                                              |      |

```shell
cat /etc/passwd 可以查看所有用户的列表
w 可以查看当前活跃的用户列表
cat /etc/group 查看用户组

groups 查看当前登录用户的组内成员
groups gliethttp 查看gliethttp用户所在的组,以及组内成员
whoami 查看当前登录用户名

```

### 2.7  配置文件

```shell
##代码块中的events、http、server、location、upstream等都是块配置项##
##块配置项可以嵌套。内层块直接继承外层快，例如：server块里的任意配置都是基于http块里的已有配置的##
 
##Nginx worker进程运行的用户及用户组 
#语法：user username[groupname]    默认：user nobody nobody
#user用于设置master进程启动后，fork出的worker进程运行在那个用户和用户组下。当按照"user username;"设置时，用户组名与用户名相同。
#若用户在configure命令执行时，使用了参数--user=usergroup 和 --group=groupname,此时nginx.conf将使用参数中指定的用户和用户组。
#user  nobody;
 
##Nginx worker进程个数：其数量直接影响性能。
#每个worker进程都是单线程的进程，他们会调用各个模块以实现多种多样的功能。如果这些模块不会出现阻塞式的调用，那么，有多少CPU内核就应该配置多少个进程，反之，有可能出现阻塞式调用，那么，需要配置稍多一些的worker进程。
worker_processes  1;
 
##ssl硬件加速。
#用户可以用OpneSSL提供的命令来查看是否有ssl硬件加速设备：openssl engine -t
#ssl_engine device;
 
##守护进程(daemon)。是脱离终端在后台允许的进程。它脱离终端是为了避免进程执行过程中的信息在任何终端上显示。这样一来，进程也不会被任何终端所产生的信息所打断。##
##关闭守护进程的模式，之所以提供这种模式，是为了放便跟踪调试nginx，毕竟用gdb调试进程时最繁琐的就是如何继续跟进fork出的子进程了。##
##如果用off关闭了master_proccess方式，就不会fork出worker子进程来处理请求，而是用master进程自身来处理请求
#daemon off;   #查看是否以守护进程的方式运行Nginx 默认是on 
#master_process off; #是否以master/worker方式工作 默认是on
 
##error日志的设置#
#语法： error_log /path/file level;
#默认： error_log / log/error.log error;
#当path/file 的值为 /dev/null时，这样就不会输出任何日志了，这也是关闭error日志的唯一手段；
#leve的取值范围是debug、info、notice、warn、error、crit、alert、emerg从左至右级别依次增大。
#当level的级别为error时，error、crit、alert、emerg级别的日志就都会输出。大于等于该级别会输出，小于该级别的不会输出。
#如果设定的日志级别是debug，则会输出所有的日志，这一数据量会很大，需要预先确保/path/file所在的磁盘有足够的磁盘空间。级别设定到debug，必须在configure时加入 --with-debug配置项。
#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;
 
##pid文件（master进程ID的pid文件存放路径）的路径
#pid        logs/nginx.pid;
 
 
events {
 #仅对指定的客户端输出debug级别的日志： 语法：debug_connection[IP|CIDR]
 #这个设置项实际上属于事件类配置，因此必须放在events{……}中才会生效。它的值可以是IP地址或者是CIRD地址。
 	#debug_connection 10.224.66.14;  #或是debug_connection 10.224.57.0/24
 #这样，仅仅以上IP地址的请求才会输出debug级别的日志，其他请求仍然沿用error_log中配置的日志级别。
 #注意：在使用debug_connection前，需确保在执行configure时已经加入了--with-debug参数，否则不会生效。
	worker_connections  1024;
}
 
##核心转储(coredump):在Linux系统中，当进程发生错误或收到信号而终止时，系统会将进程执行时的内存内容(核心映像)写入一个文件(core文件)，以作为调试只用，这就是所谓的核心转储(coredump).
 
http {
##嵌入其他配置文件 语法：include /path/file
#参数既可以是绝对路径也可以是相对路径（相对于Nginx的配置目录，即nginx.conf所在的目录）
    include       mime.types;
    default_type  application/octet-stream;
 
    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';
 
    #access_log  logs/access.log  main;
 
    sendfile        on;
    #tcp_nopush     on;
 
    #keepalive_timeout  0;
    keepalive_timeout  65;
 
    #gzip  on;
 
    server {
##listen监听的端口
#语法：listen address:port [ default(deprecated in 0.8.21) | default_server | [ backlog=num | rcvbuf=size | sndbuf=size | accept_filter=filter | deferred | bind | ssl ] ]
#default_server: 如果没有设置这个参数，那么将会以在nginx.conf中找到的第一个server块作为默认server块
	listen       8080;
 
#主机名称：其后可以跟多个主机名称，开始处理一个HTTP请求时，nginx会取出header头中的Host，与每个server中的server_name进行匹配，以此决定到底由那一个server来处理这个请求。有可能一个Host与多个server块中的server_name都匹配，这时会根据匹配优先级来选择实际处理的server块。server_name与Host的匹配优先级见文末。
	 server_name  localhost;
 
        #charset koi8-r;
 
        #access_log  logs/host.access.log  main;
 
        #location / {
        #    root   html;
        #    index  index.html index.htm;
        #}
 
##location 语法： location [=|~|~*|^~] /uri/ { ... }
# location的使用实例见文末。
#注意：location时有顺序的，当一个请求有可能匹配多个location时，实际上这个请求会被第一个location处理。
	location / {
	proxy_pass http://192.168.1.60;
        }
 
        #error_page  404              /404.html;
 
        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
 
}
```

### 2.8 nginx日志类型

```shell
log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';	
		
’HTTP_X_FORWARDED_FOR’，’HTTP_CLIENT_IP’ 为了能在大型网络中，获取到最原始用户IP，或者代理IP地址。对HTTp协议进行扩展。定义了实体头。
HTTP_X_FORWARDED_FOR = clientip,proxy1,proxy2  所有IP用”,”分割。 HTTP_CLIENT_IP 在高级匿名代理中，这个代表了代理服务器IP。既然是http协议扩展一个实体头，并且这个值对于传入端是信任的，信任传入方按照规则格式输入的。
		
192.168.1.8 - - [27/Oct/2019:09:16:50 +0800] "GET /img/header-background.png HTTP/1.1"
200 82896 "http://192.168.1.59/"
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36" "-"
```

**参数详解：**

| 参数                    | 说明                                         | 示例                                                         |
| ----------------------- | -------------------------------------------- | ------------------------------------------------------------ |
| $remote_addr            | 客户端地址                                   | 219.227.111.255                                              |
| $remote_user            | 客户端用户名称                               | -                                                            |
| $time_local             | 访问时间和时区                               | 18/Jul/2014:17:00:01 +0800                                   |
| $request                | 请求的URI和HTTP协议                          | “GET /article-10000.html HTTP/1.1”                           |
| $http_host              | 请求地址，即浏览器中你输入的地址（IP或域名） | www.ha97.com<br/>198.98.120.87                               |
| $status                 | HTTP请求状态                                 | 200                                                          |
| $upstream_status        | upstream状态                                 | 200                                                          |
| $body_bytes_sent        | 发送给客户端文件内容大小                     | 1547                                                         |
| $http_referer           | url跳转来源                                  | https://www.google.com/                                      |
| $http_user_agent        | 用户终端浏览器等信息                         | “Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; GTB7.0; .NET4.0C; |
| $ssl_protocol           | SSL协议版本                                  | TLSv1                                                        |
| $ssl_cipher             | 交换数据中的算法                             | RC4-SHA                                                      |
| $upstream_addr          | 后台upstream的地址，即真正提供服务的主机地址 | 10.36.10.80:80                                               |
| $request_time           | 整个请求的总时间                             | 0.165                                                        |
| $upstream_response_time | 请求过程中，upstream响应时间                 | 0.002                                                        |
| $http_x_forwarded_for   |                                              |                                                              |

相关命令：

```shell
# 检查配置文件语法
nginx -t -c /etc/nginx/nginx.conf
# 重载配置文件
nginx -s reload -c /etc/nginx/nginx.conf
```

### 2.9 stub_status

```shell
参考： https://blog.csdn.net/zhanghuiqi205/article/details/89417217

server {
        listen       2016;
        server_name  localhost;

        location /hello {
                echo hello world;
        }

        location /test {
                echo $remote_addr;
                echo $args;
        }

        location /proxy_brefore_after {
                echo_before_body before;
                proxy_pass http://127.0.0.1:2016/test;
                echo_after_body after;
        }

        location /if {
                set $res miss;
                if ($arg_val1 ~* '^a') {
                        set $res hit;
                        echo $res;
                }
                echo $res;

        }
        location /nginx_status {
                stub_status;
        }

}

```

结果：

```shell
[root@localhost conf.d]# curl http://127.0.0.1:2016/nginx_status
Active connections: 1
server accepts handled requests
 23 23 21
Reading: 0 Writing: 1 Waiting: 0
```

### 2.10 random_index



