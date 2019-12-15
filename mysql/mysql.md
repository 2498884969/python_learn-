## 1. 安装

```shell
# docker 安装
https://blog.csdn.net/weixin_40461281/article/details/92610876

docker run -p 3306:3306 --name mysql 
-v /root/mysql/conf:/etc/mysql/conf.d
-v /root/mysql/logs:/logs 
-v /root/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -d mysql:5.7

# 客户端设置
[client]
port = 3306
# 默认情况下，socket文件应为/usr/local/mysql/mysql.socket,所以可以ln -s xx  /tmp/mysql.sock
socket = /tmp/mysql.sock 
# 服务端设置
[mysqld]

##########################################################################################################
# 基础信息
#Mysql服务的唯一编号 每个mysql服务Id需唯一
server-id = 1
#服务端口号 默认3306
port = 3306
# 启动mysql服务进程的用户
# user = mysql

##########################################################################################################
# 安装目录相关
# mysql安装根目录
basedir = /usr/local/mysql-5.7.21
# mysql数据文件所在位置
datadir = /usr/local/mysql-5.7.21/data
# 临时目录 比如load data infile会用到,一般都是使用/tmp
tmpdir  = /tmp
# 设置socke文件地址
socket  = /tmp/mysql.sock


##########################################################################################################
# 事务隔离级别，默认为可重复读（REPEATABLE-READ）。（此级别下可能参数很多间隙锁，影响性能，但是修改又影响主从复制及灾难恢复，建议还是修改代码逻辑吧）
# 隔离级别可选项目：READ-UNCOMMITTED  READ-COMMITTED  REPEATABLE-READ  SERIALIZABLE
# transaction_isolation = READ-COMMITTED
transaction_isolation = REPEATABLE-READ

##########################################################################################################
# 数据库引擎与字符集相关设置

# mysql 5.1 之后，默认引擎就是InnoDB了
default_storage_engine = InnoDB
# 内存临时表默认引擎，默认InnoDB
default_tmp_storage_engine = InnoDB
# mysql 5.7新增特性，磁盘临时表默认引擎，默认InnoDB
internal_tmp_disk_storage_engine = InnoDB
#数据库默认字符集,主流字符集支持一些特殊表情符号（特殊表情符占用4个字节）
character-set-server = utf8
#数据库字符集对应一些排序等规则，注意要和character-set-server对应
collation-server = utf8_general_ci
# 设置client连接mysql时的字符集,防止乱码
init_connect='SET NAMES utf8'
# 是否对sql语句大小写敏感，默认值为0，1表示不敏感
lower_case_table_names = 1


##########################################################################################################
# 数据库连接相关设置
# 最大连接数，可设最大值16384，一般考虑根据同时在线人数设置一个比较综合的数字，鉴于该数值增大并不太消耗系统资源，建议直接设10000
# 如果在访问时经常出现Too Many Connections的错误提示，则需要增大该参数值
max_connections = 10000

# 默认值100，最大错误连接数，如果有超出该参数值个数的中断错误连接，则该主机将被禁止连接。如需对该主机进行解禁，执行：FLUSH HOST
# 考虑高并发场景下的容错，建议加大。
max_connect_errors = 10000

# MySQL打开的文件描述符限制，默认最小1024;
# 当open_files_limit没有被配置的时候，比较max_connections*5和ulimit -n的值，哪个大用哪个，
# 当open_file_limit被配置的时候，比较open_files_limit和max_connections*5的值，哪个大用哪个。
open_files_limit = 65535

# 注意：仍然可能出现报错信息Can't create a new thread；此时观察系统cat /proc/mysql进程号/limits，观察进程ulimit限制情况
# 过小的话，考虑修改系统配置表，/etc/security/limits.conf和/etc/security/limits.d/90-nproc.conf

# MySQL默认的wait_timeout  值为8个小时, interactive_timeout参数需要同时配置才能生效
# MySQL连接闲置超过一定时间后(单位：秒，此处为1800秒)将会被强行关闭
# interactive_timeout = 1800 
# wait_timeout = 1800 
# 在MySQL暂时停止响应新请求之前的短时间内多少个请求可以被存在堆栈中 
# 官方建议back_log = 50 + (max_connections / 5),封顶数为900
back_log = 900

##########################################################################################################
# 数据库数据交换设置
# 该参数限制服务器端，接受的数据包大小，如果有BLOB子段，建议增大此值，避免写入或者更新出错。有BLOB子段，建议改为1024M
max_allowed_packet = 1024M

##########################################################################################################
# 内存，cache与buffer设置


# 内存临时表的最大值,默认16M，此处设置成128M，排序的时候会用到
tmp_table_size = 64M
# 用户创建的内存表的大小，默认16M，往往和tmp_table_size一起设置，限制用户临师表大小。
# 超限的话，MySQL就会自动地把它转化为基于磁盘的MyISAM表，存储在指定的tmpdir目录下，增大IO压力，建议内存大，增大该数值。
max_heap_table_size = 64M
# 表示这个mysql版本是否支持查询缓存。ps：SHOW STATUS LIKE 'qcache%'，与缓存相关的状态变量。
# have_query_cache
# 这个系统变量控制着查询缓存工能的开启的关闭，0时表示关闭，1时表示打开，2表示只要select 中明确指定SQL_CACHE才缓存，一般都不需要使用缓存查询。
# 看业务场景决定是否使用缓存，不使用，下面就不用配置了。
query_cache_type = 0 
# 默认值1M，优点是查询缓冲可以极大的提高服务器速度, 如果你有大量的相同的查询并且很少修改表。
# 缺点：在你表经常变化的情况下或者如果你的查询原文每次都不同,查询缓冲也许引起性能下降而不是性能提升。
query_cache_size = 64M 
# 只有小于此设定值的结果才会被缓冲，保护查询缓冲,防止一个极大的结果集将其他所有的查询结果都覆盖。
query_cache_limit = 2M

# 每个被缓存的结果集要占用的最小内存,默认值4kb，一般不怎么调整。
# 如果Qcache_free_blocks值过大，可能是query_cache_min_res_unit值过大，应该调小些
# query_cache_min_res_unit的估计值：(query_cache_size - Qcache_free_memory) / Qcache_queries_in_cache
query_cache_min_res_unit = 4kb

# 在一个事务中binlog为了记录SQL状态所持有的cache大小
# 如果你经常使用大的,多声明的事务,你可以增加此值来获取更大的性能.
# 所有从事务来的状态都将被缓冲在binlog缓冲中然后在提交后一次性写入到binlog中
# 如果事务比此值大, 会使用磁盘上的临时文件来替代.
# 此缓冲在每个连接的事务第一次更新状态时被创建
binlog_cache_size = 1M



#*** MyISAM 相关选项
# 指定索引缓冲区的大小, 为MYISAM数据表开启供线程共享的索引缓存,对INNODB引擎无效。相当影响MyISAM的性能。
# 不要将其设置大于你可用内存的30%,因为一部分内存同样被OS用来缓冲行数据
# 甚至在你并不使用MyISAM 表的情况下, 你也需要仍旧设置起 8-64M 内存由于它同样会被内部临时磁盘表使用.
# 默认值 8M，建议值：对于内存在4GB左右的服务器该参数可设置为256M或384M。注意：该参数值设置的过大反而会是服务器整体效率降低！
key_buffer_size = 64M

# 为每个扫描MyISAM的线程分配参数设置的内存大小缓冲区。 
# 默认值128kb，建议值：16G内存建议1M，4G：128kb或者256kb吧
# 注意，该缓冲区是每个连接独占的，所以总缓冲区大小为 128kb*连接数；极端情况128kb*maxconnectiosns，会超级大，所以要考虑日常平均连接数。
# 一般不需要太关心该数值，稍微增大就可以了，
read_buffer_size = 262144 

# 支持任何存储引擎
# MySQL的随机读缓冲区大小，适当增大，可以提高性能。
# 默认值256kb；建议值：得参考连接数，16G内存，有人推荐8M
# 注意，该缓冲区是每个连接独占的，所以总缓冲区大小为128kb*连接数；极端情况128kb*maxconnectiosns，会超级大，所以要考虑日常平均连接数。
read_rnd_buffer_size = 1M

# order by或group by时用到 
# 支持所有引擎，innodb和myisam有自己的innodb_sort_buffer_size和myisam_sort_buffer_size设置
# 默认值256kb；建议值：得参考连接数，16G内存，有人推荐8M.
# 注意，该缓冲区是每个连接独占的，所以总缓冲区大小为 1M*连接数；极端情况1M*maxconnectiosns，会超级大。所以要考虑日常平均连接数。
sort_buffer_size = 1M

# 此缓冲被使用来优化全联合(full JOINs 不带索引的联合)
# 类似的联合在极大多数情况下有非常糟糕的性能表现,但是将此值设大能够减轻性能影响.
# 通过 “Select_full_join” 状态变量查看全联合的数量
# 注意，该缓冲区是每个连接独占的，所以总缓冲区大小为 1M*连接数；极端情况1M*maxconnectiosns，会超级大。所以要考虑日常平均连接数。
# 默认值256kb;建议值：16G内存，设置8M.
join_buffer_size = 1M

# 缓存linux文件描述符信息，加快数据文件打开速度
# 它影响myisam表的打开关闭，但是不影响innodb表的打开关闭。
# 默认值2000，建议值：根据状态变量Opened_tables去设定
table_open_cache = 2000

# 缓存表定义的相关信息，加快读取表信息速度
# 默认值1400，最大值2000，建议值：基本不改。
table_definition_cache = 1400
# 该参数是myssql 5.6后引入的，目的是提高并发。
# 默认值1，建议值：cpu核数，并且<=16
table_open_cache_instances = 2

# 当客户端断开之后，服务器处理此客户的线程将会缓存起来以响应下一个客户而不是销毁。可重用，减小了系统开销。
# 默认值为9，建议值：两种取值方式，方式一，根据物理内存，1G  —> 8；2G  —> 16； 3G  —> 32； >3G  —> 64；
# 方式二，根据show status like  'threads%'，查看Threads_connected值。
thread_cache_size = 16

# 默认值256k,建议值：16/32G内存，512kb，其他一般不改变，如果报错：Thread stack overrun，就增大看看,
# 注意，每个线程分配内存空间，所以总内存空间。。。你懂得。
thread_stack = 512k


##########################################################################################################
# 日志文件相关设置，一般只开启三种日志，错误日志，慢查询日志，二进制日志。普通查询日志不开启。

# 普通查询日志，默认值off，不开启
general_log = 0
# 普通查询日志存放地址
general_log_file = /usr/local/mysql-5.7.21/log/mysql-general.log
# 全局动态变量，默认3，范围：1～3
# 表示错误日志记录的信息，1：只记录error信息；2：记录error和warnings信息；3：记录error、warnings和普通的notes信息。
log_error_verbosity = 2
# 错误日志文件地址
log_error = /usr/local/mysql-5.7.21/log/mysql-error.log


# 开启慢查询
slow_query_log = 1

# 开启慢查询时间，此处为1秒，达到此值才记录数据
long_query_time = 0.5

# 检索行数达到此数值，才记录慢查询日志中
#min_examined_row_limit = 100

# mysql 5.6.5新增，用来表示每分钟允许记录到slow log的且未使用索引的SQL语句次数，默认值为0，不限制。
log_throttle_queries_not_using_indexes = 0

# 慢查询日志文件地址
#slow_query_log_file = /usr/local/mysql-5.7.21/log/mysql-slow.log

# 开启记录没有使用索引查询语句
log-queries-not-using-indexes = 1


# 开启二进制日志
log_bin = mysql-bin.log
# mysql清除过期日志的时间，默认值0，不自动清理，而是使用滚动循环的方式。
expire_logs_days = 0
# 如果二进制日志写入的内容超出给定值，日志就会发生滚动。你不能将该变量设置为大于1GB或小于4096字节。 默认值是1GB。
max_binlog_size = 1000M
# binlog的格式也有三种：STATEMENT，ROW，MIXED。mysql 5.7.7后，默认值从 MIXED 改为 ROW
# 关于binlog日志格式问题，请查阅网络资料
binlog_format = row
# 默认值N=1，使binlog在每N次binlog写入后与硬盘同步，ps：1最慢
# sync_binlog = 1 

##########################################################################################################
# innodb选项

# 说明：该参数可以提升扩展性和刷脏页性能。
# 默认值1，建议值：4-8；并且必须小于innodb_buffer_pool_instances
innodb_page_cleaners = 4

# 说明：一般8k和16k中选择，8k的话，cpu消耗小些，selcet效率高一点，一般不用改
# 默认值：16k；建议值：不改，
innodb_page_size = 16384

# 说明：InnoDB使用一个缓冲池来保存索引和原始数据, 不像MyISAM.这里你设置越大,你在存取表里面数据时所需要的磁盘I/O越少.
# 在一个独立使用的数据库服务器上,你可以设置这个变量到服务器物理内存大小的60%-80%
# 注意别设置的过大，会导致system的swap空间被占用，导致操作系统变慢，从而减低sql查询的效率
# 默认值：128M，建议值：物理内存的60%-80%
innodb_buffer_pool_size = 512M

# 说明:只有当设置 innodb_buffer_pool_size 值大于1G时才有意义，小于1G，instances默认为1，大于1G，instances默认为8
# 但是网络上有评价，最佳性能，每个实例至少1G大小。
# 默认值：1或8，建议值：innodb_buffer_pool_size/innodb_buffer_pool_instances >= 1G
innodb_buffer_pool_instances = 1

# 说明：mysql 5.7 新特性，defines the chunk size for online InnoDB buffer pool resizing operations.
# 实际缓冲区大小必须为innodb_buffer_pool_chunk_size*innodb_buffer_pool_instances*倍数，取略大于innodb_buffer_pool_size
# 默认值128M，建议值：默认值就好，乱改反而容易出问题，它会影响实际buffer pool大小。
innodb_buffer_pool_chunk_size = 128M 

# 在启动时把热数据加载到内存。默认值为on，不修改
innodb_buffer_pool_load_at_startup = 1
# 在关闭时把热数据dump到本地磁盘。默认值为on，不修改
innodb_buffer_pool_dump_at_shutdown = 1

# 说明：影响Innodb缓冲区的刷新算法，建议从小到大配置，直到zero free pages；innodb_lru_scan_depth * innodb_buffer_pool_instances defines the amount of work performed by the page cleaner thread each second.
# 默认值1024，建议值: 未知
innodb_lru_scan_depth = 1024

# 说明：事务等待获取资源等待的最长时间，单位为秒，看具体业务情况，一般默认值就好
# 默认值：50，建议值：看业务。
innodb_lock_wait_timeout = 60

# 说明：设置了Mysql后台任务（例如页刷新和merge dadta from buffer pool）每秒io操作的上限。
# 默认值：200，建议值：方法一，单盘sata设100，sas10，raid10设200，ssd设2000，fushion-io设50000；方法二，通过测试工具获得磁盘io性能后，设置IOPS数值/2。
innodb_io_capacity = 2000
# 说明：该参数是所有缓冲区线程io操作的总上限。
# 默认值：innodb_io_capacity的两倍。建议值：例如用iometer测试后的iops数值就好
innodb_io_capacity_max = 4000

# 说明：控制着innodb数据文件及redo log的打开、刷写模式，三种模式：fdatasync(默认)，O_DSYNC，O_DIRECT
# fdatasync：数据文件，buffer pool->os buffer->磁盘；日志文件，buffer pool->os buffer->磁盘；
# O_DSYNC：  数据文件，buffer pool->os buffer->磁盘；日志文件，buffer pool->磁盘；
# O_DIRECT： 数据文件，buffer pool->磁盘；           日志文件，buffer pool->os buffer->磁盘；
# 默认值为空，建议值：使用SAN或者raid，建议用O_DIRECT，不懂测试的话，默认生产上使用O_DIRECT
innodb_flush_method = O_DIRECT


# 说明：mysql5.7之后默认开启，意思是，每张表一个独立表空间。
# 默认值1，开启
innodb_file_per_table = 1

# 说明：The path where InnoDB creates undo tablespaces.通常等于undo log文件的存放目录。
# 默认值./;自行设置
innodb_undo_directory = /usr/local/mysql-5.7.21/log
# 说明：The number of undo tablespaces used by InnoDB.等于undo log文件数量。5.7.21后开始弃用
# 默认值为0，建议默认值就好，不用调整了。
innodb_undo_tablespaces = 0
# 说明：定义undo使用的回滚段数量。5.7.19后弃用
# 默认值128，建议不动，以后弃用了。
innodb_undo_logs = 128
# 说明：5.7.5后开始使用，在线收缩undo log使用的空间。
# 默认值：关闭，建议值：开启
innodb_undo_log_truncate = 1
# 说明：结合innodb_undo_log_truncate，实现undo空间收缩功能
# 默认值：1G，建议值，不改。
innodb_max_undo_log_size = 1G

# 说明：重作日志文件的存放目录
innodb_log_group_home_dir = /usr/local/mysql-5.7.21/log
# 说明：日志文件的大小
# 默认值:48M,建议值：根据你系统的磁盘空间和日志增长情况调整大小
innodb_log_file_size = 128M
# 说明：日志组中的文件数量，mysql以循环方式写入日志
# 默认值2，建议值：根据你系统的磁盘空间和日志增长情况调整大小
innodb_log_files_in_group = 3
# 此参数确定些日志文件所用的内存大小，以M为单位。缓冲区更大能提高性能，但意外的故障将会丢失数据。MySQL开发人员建议设置为1－8M之间
innodb_log_buffer_size = 16M



# 说明：可以控制log从系统buffer刷入磁盘文件的刷新频率，增大可减轻系统负荷
# 默认值是1；建议值不改。系统性能一般够用。
innodb_flush_log_at_timeout = 1
# 说明：参数可设为0，1，2；
# 参数0：表示每秒将log buffer内容刷新到系统buffer中，再调用系统flush操作写入磁盘文件。
# 参数1：表示每次事物提交，将log buffer内容刷新到系统buffer中，再调用系统flush操作写入磁盘文件。
# 参数2：表示每次事物提交，将log buffer内容刷新到系统buffer中，隔1秒后再调用系统flush操作写入磁盘文件。
innodb_flush_log_at_trx_commit = 1


# 说明：限制Innodb能打开的表的数据，如果库里的表特别多的情况，请增加这个。
# 值默认是2000，建议值：参考数据库表总数再进行调整，一般够用不用调整。
innodb_open_files = 8192

# innodb处理io读写的后台并发线程数量，根据cpu核来确认，取值范围：1-64
# 默认值：4，建议值：与逻辑cpu数量的一半保持一致。
innodb_read_io_threads = 4
innodb_write_io_threads = 4
# 默认设置为 0,表示不限制并发数，这里推荐设置为0，更好去发挥CPU多核处理能力，提高并发量
innodb_thread_concurrency = 0
# 默认值为4，建议不变。InnoDB中的清除操作是一类定期回收无用数据的操作。mysql 5.5之后，支持多线程清除操作。
innodb_purge_threads = 4 

# 说明：mysql缓冲区分为new blocks和old blocks；此参数表示old blocks占比；
# 默认值：37，建议值，一般不动
innodb_old_blocks_pct = 37
# 说明：新数据被载入缓冲池，进入old pages链区，当1秒后再次访问，则提升进入new pages链区。
# 默认值：1000
innodb_old_blocks_time=1000
# 说明：开启异步io，可以提高并发性，默认开启。
# 默认值为1，建议不动
innodb_use_native_aio = 1

# 说明：默认为空，使用data目录，一般不改。
innodb_data_home_dir=/usr/local/mysql-5.7.21/data
# 说明：Defines the name, size, and attributes of InnoDB system tablespace data files.
# 默认值，不指定，默认为ibdata1:12M:autoextend
innodb_data_file_path = ibdata1:12M:autoextend


# 说明:设置了InnoDB存储引擎用来存放数据字典信息以及一些内部数据结构的内存空间大小,除非你的数据对象及其多，否则一般默认不改。
# innodb_additional_mem_pool_size = 16M


# 说明：The crash recovery mode。只有紧急情况需要恢复数据的时候，才改为大于1-6之间数值，含义查下官网。
# 默认值为0；
#innodb_force_recovery = 0

##########################################################################################################
# 其他。。。。
# 参考http://www.kuqin.com/database/20120815/328905.html
# skip-external-locking

# 禁止MySQL对外部连接进行DNS解析，使用这一选项可以消除MySQL进行DNS解析的时间。
# 缺点：所有远程主机连接授权都要使用IP地址方式，因为只认得ip地址了。
# skip_name_resolve = 0

# 默认值为off,timestamp列会自动更新为当前时间，设置为on|1，timestamp列的值就要显式更新
explicit_defaults_for_timestamp = 1




[mysqldump]
# quick选项强制 mysqldump 从服务器查询取得记录直接输出而不是取得所有记录后将它们缓存到内存中
quick
max_allowed_packet = 16M

[mysql]
# mysql命令行工具不使用自动补全功能，建议还是改为
# no-auto-rehash
auto-rehash
socket = /tmp/mysql.sock
```

## 2.学习

### 05.  深入浅出索引（下）

```shell

```

### 16. `order by` 是怎么工作的

```shell
# 创建表
CREATE TABLE `t` (
  `id` int(11) NOT NULL,
  `city` varchar(16) NOT NULL,
  `name` varchar(16) NOT NULL,
  `age` int(11) NOT NULL,
  `addr` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `city` (`city`)
) ENGINE=InnoDB;


explain select city,name,age from t where city='杭州' order by name limit 1000  ;


# use index 和 use index condition的区别
https://blog.csdn.net/h106140873/article/details/80999990
```

### 3. python 与mysql

```shell
# 根据表得到orm sqlalchemy
https://blog.csdn.net/github_26672553/article/details/78549078
# session
https://blog.csdn.net/qq_43355223/article/details/86678516
# faker 使用 
https://blog.csdn.net/JR_willbeBetter/article/details/89438116
# random随机选取
https://blog.csdn.net/kl28978113/article/details/79485037
# sqlahemy 增删改查

# 数据库插入中文报错
https://www.cnblogs.com/u-vitamin/p/10608441.html
# 修改配置文件
https://blog.csdn.net/eagle89/article/details/82148751
```

### 10 MYSQL为什么会选错索引

```shell
https://www.cnblogs.com/a-phper/p/10313888.html

# delimiter 练习
https://blog.csdn.net/yuxin6866/article/details/52722913
# mysql触发器
https://www.cnblogs.com/fps2tao/p/10400936.html
# mysql 事件
https://www.cnblogs.com/wt645631686/p/9208245.html

表 t
id int p
a int nd
b int dn
k a
k b

delimiter ;;
  create procedure idata()
  begin
    declare i int;
    set i=1;
    while(1<=10000) do
      insert into t values (i,i,i);
      set i=i+1;
    end while
  end;;
delimiter ;
```

### 19 `mysql`只查找一行也很慢

```mysql
-- 1.MySQL 5.7中如何定位DDL被阻塞的问题 
https://www.cnblogs.com/ivictor/p/9460147.html
-- 2. flash 的作用
https://www.cnblogs.com/shc336/p/9796018.html
```

## 3.名词

```shell
collation	英[kəˈleɪʃn] 校对整理
同一条记录在系统中可以存在多个版本，就是数据库的多版本并发控制（MVCC）
```

## 4. 额外



### 4.1与锁相关的表

```shell
# mysql查看当前数据库锁请求
https://blog.csdn.net/asdfsadfasdfsa/article/details/84634669
# 查询事务的详细信息
https://www.cnblogs.com/gaogao67/p/10790520.html
```

`information_shcema`下的三张表（通过这三张表可以更新监控当前事物并且分析存在的锁问题）

- `innodb_trx` （打印`innodb`内核中的当前活跃事务）
-  `innodb_locks` （ 打印当前状态产生的`innodb`锁 仅在有锁等待时打印）

- `innodb_lock_waits`（打印当前状态产生的`innodb`锁等待 仅在有锁等待时打印，感觉没多大用）



| 字段名                | 说明                                                         |
| --------------------- | ------------------------------------------------------------ |
| trx_id                | 事务ID                                                       |
| trx_state             | 当前事务的状态(runing和lock_wait两种状态)                    |
| trx_started           | 事务开始的时间                                               |
| trx_requested_lock_id | 处于等待状态务的锁ID,trx_state为running，则值为NULL          |
| trx_wait_started      | 事务等待的开始时间                                           |
| trx_weight            | 事务的权重，在innodb中，发生死锁的时候优先回滚权重较小的事务 |
| trx_mysql_thread_id   | mysql中的线程ID即show processlist的结果                      |
| trx_query             | 事务运行的SQL                                                |

- `innodb_locks` 

|      |      |
| ---- | ---- |
|      |      |
|      |      |
|      |      |
|      |      |
|      |      |
|      |      |
|      |      |
|      |      |
|      |      |

### 4.2Mysql 添加 create_time, update_time自动更新

```shell
https://www.jianshu.com/p/490947d61719
```

### 4.3 触发器before和after

```shell
https://www.cnblogs.com/zuochuang/p/7263848.html
```

### 4.4  mysql避免幻读原理

```shell
# 两种情况 快照读(mvcc) 当前读(next-key)
https://www.cnblogs.com/fanguangdexiaoyuer/p/10759746.html
```





## 5.循环

```mysql
1. 给表格添加索引
alter table `table_name` add index `index_name`(`column_name`);
2. 慢查询
show variables like `slow_query_log`;
	slow_query_log: off/on 0/1
	slow_query_log_file:
	long_query_time:	
3. 存储过程
delimiter ;;
create procedure idata()
begin
  declare i int
  set i=i+1
  while(i<10000)do
    insert into table_name values(i,i,i);
    set i=i+1;
  end while;
end;;
delimiter;
4. case when使用详解
select name, gender( case gender
	when 1 then '男'
	when 2 then 'nv'
    else '未知'
end) as '性别' from test_user;
5. 查看表创建的详细信息
show create table `table_name`;
6. 给表添加索引
alter table `table_name`
	add index `index_name`(`column_name`);
7. 慢查询相关
show variables like 'slow_query_log';
			slow_query_log: off/on 0/1;
			long_query_time:
			slow_query_log_file:
8. 存储过程
delimiter ;;
create procedure idata()
begin
  declare i int;
  set i=0;
  while(i<=100000)do
    insert into t1 values(i,i);
    i=i+1;
  end while;
end;;
delimiter;
9. case和when
select id, name, gender (case gender
	when 1 then '男'
  when 0 then '女'
  else '未知'
) as '性别' from test_user;
10. 查看表的信息
show variables like t_a;
11. 创建事件
create event event_now
on schedule
at now()
do insert into event_list values('event_now', now());
12. 删除事件
drop event if exists event_second;
13. 开启关闭事件
alter event `event_name` disable/enable;
14. 
show events;
15. 查看行锁
select * from sys.innodb_lock_waits\G；
```

## 6. 实验

### 1.索引失效

```mysql
# 1. 创建tradelog表
CREATE TABLE `tradelog` (
  `id` int(11) NOT NULL,
  `tradeid` varchar(32) DEFAULT NULL,
  `operator` int(11) DEFAULT NULL,
  `t_modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tradeid` (`tradeid`),
  KEY `t_modified` (`t_modified`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
# 2. 创建trade_detail表
CREATE TABLE `trade_detail` (
  `id` int(11) NOT NULL,
  `tradeid` varchar(32) DEFAULT NULL,
  `trade_step` int(11) DEFAULT NULL, /*操作步骤*/
  `step_info` varchar(32) DEFAULT NULL, /*步骤信息*/
  PRIMARY KEY (`id`),
  KEY `tradeid` (`tradeid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
# 3. 插入数据
insert into tradelog values(1, 'aaaaaaaa', 1000, now());
insert into tradelog values(2, 'aaaaaaab', 1000, now());
insert into tradelog values(3, 'aaaaaaac', 1000, now());

insert into trade_detail values(1, 'aaaaaaaa', 1, 'add');
insert into trade_detail values(2, 'aaaaaaaa', 2, 'update');
insert into trade_detail values(3, 'aaaaaaaa', 3, 'commit');
insert into trade_detail values(4, 'aaaaaaab', 1, 'add');
insert into trade_detail values(5, 'aaaaaaab', 2, 'update');
insert into trade_detail values(6, 'aaaaaaab', 3, 'update again');
insert into trade_detail values(7, 'aaaaaaab', 4, 'commit');
insert into trade_detail values(8, 'aaaaaaac', 1, 'add');
insert into trade_detail values(9, 'aaaaaaac', 2, 'update');
insert into trade_detail values(10, 'aaaaaaac', 3, 'update again');
insert into trade_detail values(11, 'aaaaaaac', 4, 'commit');

# 两张表以trade相互关联
# 测试语句1 以tradelog为驱动表
mysql> select d.* from tradelog l, trade_detail d where d.tradeid=l.tradeid and l.id=2; /*语句Q1*/
# 表tradelog使用了主键索引，扫描行数为1
# 表trade_detail没有使用索引，进行了全表扫描，扫描行数为11
# 原因为 两张表的编码不一致，在扫描过程中utf8会默认转为utf8mb4

mysql>select l.operator from tradelog l , trade_detail d where d.tradeid=l.tradeid and d.id=4;
# convert发生在右值上不会导致索引失效,驱动表为trade_detail
优化方法：
1. 修改编码
2.

mysql> select d.* from tradelog l , trade_detail d where d.tradeid=CONVERT(l.tradeid USING utf8) and l.id=2; 
```

## 7. 高可用

```mysql
-- 1. 基于gtid的主从同步
https://www.cnblogs.com/zyxnhr/p/11141234.html#_label2_2
-- 2. 只同步部分库或者表
https://blog.csdn.net/sj349781478/article/details/77731344
```




























