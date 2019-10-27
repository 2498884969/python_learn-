## 1. mysql

### 1.1 B-Tree

- `B-Tree` 的特点(如下为3阶B树)
- **阶数：**树中所有孩子结点个数的最大值称为该树的阶

![](./pic/1.mysql/3阶B树.png)

1. 根节点至少包括两个孩子

2. 树中的每个节点最多包含有m个孩子(m>=2)，m为树的阶数，也就是说极端情况下为二叉树

3. 除根节点和叶子节点外，其它每个节点至少含有ceil(m/2)个节点，ceil为向上取整

4. 所有叶子节点都位于同一层

5. 假设每个非终端节点中包含有n个关键字信息，其中

   a. `k_i(i=1...n)` 为关键字，且关键字按顺序升序排序`k_(i-1)<k_i`

   b. 关键字的个数n必须满足：`[ceil(m/2)-1] <=n<=m-1`

   c. 非叶子节点的指针`P[1],P[2]...P[M]`，其中`P[1]`指向关键字小于`K[1]`的子树，`P[M]`指向关键字大于`K[M-1]`的子树，其它关键字指向`(k_[i-1],k[i])`的子树

### 1.2B+-Tree

![](./pic/1.mysql/B+树.png)

**B+树是B树的变体，其基本定义与B树相同除了：**

1. 非叶子节点的指针数与节点的关键字的个数相同
2. 非叶子节点的子树指针P[i]，指向关键字值[k[i],k[i+1])的子树
3. 非叶子节点仅用来作为索引数据都保存在叶子节点里面
4. 所有叶子节点均有一个链指针指向下一个叶子节点（适合用来做范围统计）

**结论：B+树更适合用来作为索引**

1. `B+` 树的磁盘读写代价更低（由于B+树非叶子节点仅仅用来存储索引，这样可以在使用的时候将索引和数据分别存储于不同的盘区，由于索引数据量较少可以一次性读取所有索引的数据，再进行定位数据）

2. `B+`树的查询效率更加稳定

   由于内部结点并不是最终指向文件内容的结点，而只是叶子结点中关键字的索引。所以任何关键字的查找必须走一条从根结点到叶子结点的路。所有关键字查询的路径长度相同，导致每一个数据的查询效率相当。

3. B+树更有利于对于数据库的扫描和范围查询

   B树在提高了磁盘IO性能的同时并没有解决元素遍历的效率低下的问题，而B+树只需要遍历叶子节点就可以解决对全部关键字信息的扫描，所以对于数据库中频繁使用的range query，B+树有着更高的性能。

### 1.3 索引模块

- 密集索引文件中的每个搜索码值都对应一个索引值
- 稀疏索引文件只为索引码的某些值建立索引项

![](./pic/1.mysql/密集索引和稀疏索引的区别.png)

密集索引的定义：叶子节点保存的不只是键值，还保存了位于同一行记录里的其他列的信息，由于密集索引决定了表的物理排列顺序，一个表只有一个物理排列顺序，所以一个表只能创建一个密集索引

稀疏索引：叶子节点仅保存了键位信息以及该行数据的地址，有的稀疏索引只保存了键位信息机器主键

`myIsam`存储引擎，不管是主键索引，唯一键索引还是普通索引都是稀疏索引

`innodb`存储引擎：有且只有一个密集索引。密集索引的选取规则如下：

- 若主键被定义，则主键作为密集索引
- 如果没有主键被定义，该表的第一个唯一非空索引则作为密集索引
- 若不满足以上条件，innodb内部会生成一个隐藏主键（密集索引）
- 非主键索引存储相关键位和其对应的主键值，包含两次查找（1.通过辅助索引找到主键索引；2.通过主键索引找到具体数据）

PS:myIsam的索引和数据存放在不同文件中(`.MYI,.MYD`)，而`innodb`的存放在同意文件中(`.idb`)

![](./pic/1.mysql/索引查找过程.png)

### 1.4 事务（`trasaction`）

- 事务是数据库并发控制的基本单位
- 事务可以看做是一系列SQL语句的集合
- 事务要么全部执行成功，要么全部执行失败（回滚）

事务隔离级别：https://www.cnblogs.com/shihaiming/p/11044740.html

```shell
原子性（Atomicity）：事务开始后所有操作，要么全部做完，要么全部不做，不可能停滞在中间环节。事务执行过程中出错，会回滚到事务开始前的状态，所有的操作就像没有发生一样。也就是说事务是一个不可分割的整体，就像化学中学过的原子，是物质构成的基本单位。

一致性（Consistency）：事务开始前和结束后，数据库的完整性约束没有被破坏 。比如A向B转账，不可能A扣了钱，B却没收到。

隔离性（Isolation）：同一时间，只允许一个事务请求同一数据，不同的事务之间彼此没有任何干扰。比如A正在从一张银行卡中取钱，在A取钱的过程结束前，B不能向这张卡转账。

持久性（Durability）：事务完成后，事务对数据库的所有更新将被保存到数据库，不能回滚。（redo_log）
```

- 事务并发控制可能产生的问题

```shell
- 幻读（phantom read）:一个事务第二次查出现第一次没有的结果				
- 不可重复读(nonrepeatable read)：一个事务重复两次读得到的结果不一致
- 脏读(dirty read):一个事务读到另外一个事务没有提交的修改
- 修改丢失(lost update)：并发写入造成其中一些修改丢失
```

- 四种事务的隔离级别

```shell
- 读未提交(read uncommited) 脏读 不可重复读 幻读
- 读已提交(read committed)  不可重复读 幻读
- 可重复读(reapeatable read) 可以通过next-key锁来避免幻读
- 序列化读(serialisale read)
```

- 如何解决高并发场景下的插入重复

```shell
- 使用数据库的唯一索引
- 使用异步队列写入
- 使用redis等实现分布式锁
```

- 乐观锁和悲观锁

```shell
- 悲观锁是先获取锁再进行操作。一锁二查三更新select for update
- 乐观锁先修改，更新的时候发现数据已经变了就回滚(check and set) 时间戳或版本号
- 选择的时候需要根据响应速度、冲突频率、重试代价来判断使用哪一种		
```

- `InnoDB vs MyISAM`

```shell
MyISAM不支持事务 InnoDB 支持事务 
MyISAM不支持外键 InnoDB 支持外键 
MyISAM只支持表锁 InnoDB 支持表锁和行锁
MyISAM只支持全文索引 InnoDB 不支持全文索引
```



###  1.5相关面试题

1. `MYSQL`与`IO`的关系：<http://www.sohu.com/a/280609547_818692>

### 1.6MYSQL索引原理

- 为什么需要索引？

```shell
如何定位并优化慢查询SQL？

	1.根据慢查询日志定位出慢查询SQL（show_query_log_ile）
	2.使用explain等工具分析sql
	3.修改sql尽量使得sql通过索引进行查询,调整业务代码或者sql语句使得SQL语句尽量使用索引

最左匹配原则：
	1. 在使用联合索引的情况下，mysql会一直向右匹配知道遇到范围查询（>、<、between、like）就停止匹配，比如
	a=3 and b=4 and c>5 and d=6 如果建立(a、b、c、d)顺序的索引，d是用不到索引的，如果建立(a、b、d、c)的索 	引，则都可以用到
	
	可以认为(a、b、c、d)产生了四个索引(a), (a、b)， (a、b、c), (a、b、c、d)
	
	2. =和in可以乱序，比如a=1 and b=2 and c=3 建立(a,b,c)索引可以任意顺序，mysql的查询优化器会帮你优化成索	  引可以识别的形式。
	
-- 1.建表
CREATE TABLE t_a(
`a` INT UNSIGNED not null auto_increment,
`b` int not null,
`c` int not null,
`d` int not null,
PRIMARY KEY(`a`) 
);
-- 2. 创建唯一索引
ALTER table t_a add UNIQUE(`b`); 
-- 3.添加联合索引
alter table t_a add key(`a`, `b`, `c`, `d`); 

-- 4.插入数据
INSERT INTO t_a (a,b,c,d) VALUES (2,3,4,5); 
INSERT INTO t_a (a,b,c,d) VALUES (3, 4, 5, 6);
INSERT INTO t_a (a,b,c,d) VALUES (4,5,6,7); 
INSERT INTO t_a (a,b,c,d) VALUES (5, 6, 7, 8); 
-- 5.查询仅使用了主键索引并没有使用复合索引
explain select * from t_a where a=3 and b=4 and c>4 and d=6\G;
***************************[ 1. row ]***************************
id            | 1
select_type   | SIMPLE
table         | t_a
partitions    | <null>
type          | const
possible_keys | PRIMARY,b,a
key           | PRIMARY
key_len       | 4
ref           | const
rows          | 1
filtered      | 100.0
Extra         | <null>
	
	
id            | 1
select_type   | SIMPLE
table         | t_b
partitions    | <null>
type          | index
possible_keys | <null>    空
key           | a		不为空
key_len       | 20
ref           | <null>
rows          | 1
filtered      | 100.0
Extra         | Using where; Using index	
    这种情况一般发生在覆盖索引条件下
    possible_keys为null 说明用不上索引的树形查找
    但如果二级索引包含了所有要查找的数据，二级索引往往比聚集索引小，所以mysql可能会选择顺序遍历这个二级索引直接返回
    所以就出现了你的这个情况
	
最左匹配原则的成因：

索引是建立的越多越好吗：
    1.数据量小的表不需要建立索引，建立会增加额外的索引开销
    2.数据变更需要维护索引，因此更多的索引意味着更多的维护成本
    3.更多的索引也需要更多的空间
    
建表的时候需要根据查询需求来创建索引：
- 经常作为查询条件的字段
- 经常作为表连接的字段
- 经常出现在order by, group by之后的字段

创建索引需要注意什么？
- 非空字段not null,Mysql很难对于空值进行查询优化
- 区分度高，离散度大，作为索引的字段尽量不要有大量相同值(值相同只能进行遍历搜索)
- 索引的长度不要太长

索引什么时候失效？

模糊匹配、类型隐转、模糊搜索
- 以%开头的like语句，模糊搜索
- 出现类型隐式转换
- 没有满足最左前缀
- or中含有没有索引的字段

聚集索引 非聚集索引 辅助索引

内连接 外连接 全连接

1. 为什么mysql数据库的主键使用自增的整数比较好?
2. 使用uuid可以吗？为什么？
3. 如果是分布式系统我们怎么生成数据库的自增id?
```

### 1.7锁模块

```shell
MyISAM和InnoDB关于锁方面的区别是什么：
	lock tables xxx read;		增加表级读锁
	lock tables xxx read;		增加表级写锁
	unlock tables;				释放锁
	MyISAM不支持事务 InnoDB 支持事务 
    MyISAM不支持外键 InnoDB 支持外键 
    MyISAM只支持表锁 InnoDB 支持表锁和行锁
    MyISAM只支持全文索引 InnoDB 不支持全文索引
    autocommit 事务自动提交
    
    select * from person where id=3;					快照读并未添加锁
    select * from person where id=3 lock in share mode;		为单行添加读锁
    
    innodb全表扫描（不走索引）同样会为表加上表锁
    
    IS ： 意向共享锁	表级锁
    IX ： 意向排他锁	表级锁
    
    DML(Data Manipulation Language, DML)锁：对于数据进行增删改查所加的锁
    DDL(Data Definition Language, DDL)锁：对于表结构进行变更锁加的锁
    

数据库事务的四大特性

事务隔离级别以及各级别下的并发访问问题
	- 幻读（phantom read）:一个事务第二次查出现第一次没有的结果				
    - 不可重复读(nonrepeatable read)：一个事务重复两次读得到的结果不一致
    - 脏读(dirty read):一个事务读到另外一个事务没有提交的修改
    - 修改丢失(lost update)：并发写入造成其中一些修改丢失(mysql几乎避免了这种情况的发生)
	
	# 设置事务隔离级别
	set session transaction isolation level read uncommitted
	
	# 幻读 rc级别测试
	锁表（添加共享锁之后）之后插入数据
	
	# serializable 不用显示添加锁

InnoDB可重复读级别下如何避免幻读
	当前读（对于读取的记录加锁）：
		select ... lock in share mode, select ... for update
		update, delete, insert
    快照度：不加锁的非阻塞读，select不加锁的条件是事务隔离级别低于serializable的情况下
    	RC:快照度==当前读		每次创建一个快照
    	RR:快照度！=当前读     创建快照的时机决定了快照的版本

    	 	
     Gap锁会用在非唯一索引没有命中或者不走索引的当前读中
     	- 索引没有全部命中或没有命中
     	- 非唯一索引
     	- 不走索引(会对于所有gap上锁)
     	
     主要通过next-key锁来避免幻读
     	next-key由record lock 和gap lock组成 
    	
    
RC、RR级别下的InnoDB的非阻塞读如何实现
	    
    快照读如何实现：
    	- 数据行里面的DB_TRX_ID（最后一次修改的事务编号deletion）、DB_ROLL_PTR（指向上一个版本）、DB_ROW_ID(行ID，隐藏	主键)字段
    	- undo 日志
    	- read view
```

### 1.8 关键语法

```shell
GROUP BY
	- student stu_id socre c_id course

student: name id
score: id student_id course_id score

# 查询所有同学的学号、选课数、总成绩
# 如果用group by 那么你的select语句中要么是你groupby里用到的列，
# 要么就是我们之前说的带有sum min等列函数的列， 仅对于同一张表有效
select student_id, count(course_id), sun(score) from score group by syudent_id

# 查询 所有同学 的学号、姓名、选课数、总成绩

select student_id,name, count(course_id), sun(score)  from score sc left join student st on sc.student_id=st.student_id group by student_id

from student, score where sc.student=st

having
	- 通常与group by 字句一起使用
	- where 过滤行, having过滤组
	- 出现在同一SQL中的顺序：where > group by > having
	
# 查询平均成绩大于60分的同学的学号和平均成绩

select student_id , avg(score) 
from
	score
group by score having avg(score) > 60

# 查询所有同学的学号、选课数、总成绩
# 查询平均成绩大于60分的同学的学号和平均成绩
# 取出student_id为1的学生的成绩情况
# 没有学全所有课的同学的学号、姓名

课程 count(score.course_id)<4
学号 score.student_id student.id
姓名： student.name

select student.id student.name from student, score
where student.id = score.student_id
group by student.id
having count(score.course_id) < (select count(*) from course);



```



## 2.WEB安全

### 2.1 SQL注入

**SQL注入与防范**

- 通过构造特殊的输入参数传入web应用，直接导致后端执行了恶意`SQL`

- 通常由于程序员未对于输入进行过滤，直接动态拼接SQL产生

- 可以使用开源工具`sqlmap`， `SQLninja` 检测

**案例**

```sql
-- 创建表
CREATE TABLE `USER` (
`id` int NOT NULL AUTO_INCREMENT,
`name` VARCHAR(45) NULL,
`email` VARCHAR(45) NULL,
`password` VARCHAR(45) NULL,
PRIMARY KEY(`id`)
);

-- 插入数据
INSERT INTO user(name,email,password) values(
'lisi', 'lisi@gmail.com',md5('lisi123')
);
```

- python代码

```python
import MySQLdb

db = MySQLdb.connect(host="127.0.0.1", user='root', passwd='123456', db='demo')
cur = db.cursor()
name = input("Enter Name: ")
print('您输入的用户name是{name}'.format(name=name))
password = input('Enter password: ')
print('您输入的密码是：{password}'.format(password=password))
# 直接拼接SQL
# sql = "select * from user where name = '" + name + "' and password = md5('" + password + "')"
sql = "select * from user where name = '{name}' and password = md5('{password}')".\
    format(name=name, password=password)
print(sql)
cur.execute(sql)
for row in cur.fetchall():
    print(row)

```

- 直接拼接SQL的输出结果

```shell
Enter Name: lisi ' -- '
您输入的用户name是lisi ' -- '
Enter password: 123
您输入的密码是：123
select * from user where name = 'lisi ' -- '' and password = md5('123')
(1, 'lisi', 'lisi@gmail.com', 'c3cb6d12c40908943b64bc0681af47db')
```

- 采用字符替换的输出结果

```python
您输入的用户name是lisi ' -- '
Enter password: 123
您输入的密码是：123
select * from user where name = 'lisi ' -- '' and password = md5('123')
(1, 'lisi', 'lisi@gmail.com', 'c3cb6d12c40908943b64bc0681af47db')

```

**如何防范SQL注入**

**web安全一大原则：永远不要相信用户的输入**

- 对于输入参数做好类型检查，过滤和转义特殊字符
- 不要直接拼接SQL，使用ORM可以大大降低SQL注入风险
- 数据库底层：做好权限管理配置；不要明文存储敏感信息（密码）

### 2.2 XSS攻击

**XSS（Cross Site Scripting）跨站脚本攻击**

- 恶意用户将未进行转义的代码植入到提供给其他用户使用的页面中，未经转义的恶意代码输出到其他用户的浏览器被执行
- 用户浏览页面的时候嵌入页面的脚本(js)会被执行，对于用户进行攻击
- 主要分为两类：反射型（非持久型）、存储型（持久型）

**XSS危害**

- 盗用用户的cookie，获取敏感信息
- 利用私人账号执行一些违法操作，比如盗取个人或者商业资料，执行一些隐私操作
- 甚至可以在一些访问量很大的网站上实现DDoS攻击

**XSS防范**

- 过滤。对于`<script> <img> <a>` 等进行过滤
- 转义。对常见符号`(&、<、>)` 进行转义(`python3 html.escape`)
- 后端设置`httpOnly`禁止浏览器访问和操作`Document.cookie`

```python
a = html.escape('<script>')
a # '&lt;script&gt;'
```

### 2.3 什么是CSRF?

**CSRF:Cross-site request forgery（跨站请求伪造）**

- 利用网站对于已认证用户的权限去执行为授权命令的一种恶意攻击
- 攻击者会盗用你的登录信息，以你的身份发起请求
- web身份认证机制只能识别一个请求是否来自某个用户的浏览器，但无法保证请求时用户自己或批准发送的

![](C:\Users\Administrator\Desktop\python_learn-\面试\pic\2.web安全\csrf.PNG)

**CSRF产生条件**

- 受害者已经登录到目标网站并且没有退出（保持登录状态）
- 受害者访问了攻击者发布的链接或者表单
- 二者缺一不可

**如何防范CSRF**

- 不要在get请求里面有任何数据修改的操作
- 令牌同步(`Synchronized token pattern`， 简称`STP`)：在用户请求的表单里面嵌入一个隐藏的`csrf_token`，服务端验证其是否与`cookie`中的一致（基于同源策略其他网站是无法获取`cookie`中的`csrf_token`） 黑客是拿不到你cookie中的scrftoken值得，前提是网站本身没有XSS漏洞
- 如果是js提交需要先从`cookie`获取`csrf_token`作为`X-CSRFToken`请求头提交
- 其他：检查来源`HTTP Referer`(容易被伪造)；验证码方式（安全但是繁琐）

原理参考：`http://webpy.org/cookbook/csrf`



## 3.redis

### 3.1 什么是缓存？为什么要使用缓存？

- 缓解关系型数据库（常见的是`Mysql`）并发访问的压力：热点数据
- 减少响应时间：内存IO速度比磁盘快
- 提升吞吐量：Redis等内存数据库单机就可以支撑很大的并发

### 3.2 `Redis`和`Memcached`主要差别?

![](./pic/3.redis/redis和memcache的差异.PNG)

```shell
memcache:
	- 支持简单数据类型
	- 不支持数据持久化存储
	- 不支持主从
	- 不支持分片
```





### 3.3 请简述redis常用数据类型和使用场景？

- `String(字符串)`：用来实现简单的KV键值存储，比如计数器，最大512M
- `List(双向队列)`：可以用来存储用户的关注或者粉丝列表
- `Hash`（哈希表）：用来存储彼此相关信息的键值对
- `Set`（集合）：存储不重复元素，比如用户的关注者
- `Sorted Set`（有序集合）：实时信息排行榜，通过`score`值进行排序

### 3.4 `Redis`内置实现

- `String`：整数或者`sds(Simple Dynamic String)` 简单动态字符串

- `List`：`ziplist`或者`double linked list`

  PS：`ziplist`是通过一个连续内块实现`list`结构，其中每个`entry`节点头部保存前后节点长度信息，实现双向链表功能

- `Hash`：`ziplist` 和`hashtable`

- `Set`：`intset`或者`hashtable`

- `SortedSet`(zSet)：`skiplist跳跃表`

**skiplist实现**

这张跳表的图优点问题没有包含向下的箭头

![](./pic/3.redis/跳跃表.PNG)

### 3.5什么是redis事务？

**和Mysql的事务有什么不同？**

- 将多个请求打包，一次性、按顺序执行多个命令的机制
- `Redis`通过`MULTI`，`EXEC`,`WATCH`,`DISCARD` 等命令实现事务
- `Python redis-py pipeline=conn.pipeline(transaction=True)`

### 3.6使用的缓存模式？
- `Cache Aside：`同时更新缓存和数据库，首先去缓存中获取数据，缓存中没有再去数据库里面拿数据，然后将数据更新到缓存。
  - 问题：数据一致性问题
  - 先更新数据库后更新缓存，并发写操作的时候可能导致缓存读取的是脏数据
  - 一般先更新数据库，等到数据读取的时候再去更新缓存
- `Read/Write Through`：先更新缓存，缓存负责同步更新数据库
- `Write Behind Caching：`先更新缓存缓存定期异步更新数据库

### 3.7如何解决缓存穿透问题？

**大量查询不到的数据的请求落到后端数据库，数据库压力增大**

- 由于大量缓存查不到就去数据库取，数据库也没有要查的数据
  - 很多无脑爬虫通过自增`id`的方式爬取网站，网站查不到相关的`id`数据
  - 解决：对于没查到返回为None的数据也缓存
  - 插入时删除缓存，或者为为None的缓存设置超时时间
  
  ```shell
  缓存穿透是指缓存和数据库中     都没有的数据，而用户不断发起请求，如发起为id为“-1”的数据或id为特别大不存在的数据。这时的用户很可能是攻击者，攻击会导致数据库压力过大。
  
  解决方案：
  
  接口层增加校验，如用户鉴权校验，id做基础校验，id<=0的直接拦截；
  从缓存取不到的数据，在数据库中也没有取到，这时也可以将key-value对写为key-null，缓存有效时间可以设置短点，如30秒（设置太长会导致正常情况也没法使用）。这样可以防止攻击用户反复用同一个id暴力攻击
  ```

### 3.8 如何解决缓存击穿问题？

**某些非常热点的数据`key`过期，大量请求打到后端数据库**

- **热点**数据`key`失效导致大量请求大道后端数据库增加数据库压力
- 分布式锁：获取锁的线程从数据库拉数据更新缓存，其他线程等待
- 异步后台更新：后台任务对过期的`key`自动刷新

```shell
缓存击穿是指   缓存中没有但数据库中有的数据   （一般是缓存时间到期），这时由于并发用户特别多，同时读缓存没读到数据，又同时去数据库去取数据，引起数据库压力瞬间增大，造成过大压力

解决方案：

设置热点数据永远不过期。
分布式锁：获取锁的线程从数据库拉数据更新缓存，其他线程等待
```



### 3.9 如何解决缓存雪崩问题？

**缓存（缓存服务器挂了）不可用或者大量缓存`key`同时失效，大量请求直接打到数据库**

- 多级缓存：不同级别的`key`设置不同的超时时间
- 随机超时：`key`的超时时间随机设置，防止同时超时
- 架构层：提升系统可用性。监控、报警完善

### 3.10 缓存主要应用架构

### 3.11 为什么redis这么快？

```shell
1. 完全基于内存，绝大部分请求时纯粹的内存操作，执行效率高
2. 数据结构简单，对数据操作也简单(存储结构类似于hashmap)
3. 采用单线程，避免的锁请求和上下文切换
4. 使用了多路IO复用模型，非阻塞IO
```

### 3.12 从海量`key`里查询出某一固定前缀的`key`

```shell
keys pattern: 查找所有符合给定pattern的key
- keys指令会一次性返回所有匹配的key
- 键的数量过大会使服务卡顿

scan cursor [MATCH pattern] [Count count]
count 为期待返回的元素数量
- 基于游标的迭代器, 需要基于上一次的游标延续之前的迭代过程
- 以0为游标开始一次新的迭代，知道命令返回0， 完成一次遍历
- 不保证每次都返回给定数量个元素，支持模糊查询
- 一次返回的数量不可控，只能大概符合count参数
```

### 3.13 如何通过redis实现分布式锁

```shell
- 互斥性
	同时持有锁的客户端只能有一个
- 安全性
	释放锁和获得锁的必须使同一个客户端
- 死锁
	 获取锁的客端端由于某些原因导致宕机，必须通过一定的手段使得宕机后redis还可以继续释放
 - 容错
 	  一些redis节点宕机之后还可以继续获取锁
 	  
为代码段1(原子性得不到满足)：
status = redis.setnx(key, "1")
if status == 1:
	expire(key, expire_time)
	doSometing()

set key value [Ex seconds] [Px milliseconds] [NX|XX]

伪代码:
res = redis.set(lockKey, requestId（'uuid或者时间戳'）,SET_IF_NOT_EXITE, EXPIRE_TIME);
if ('OK'.equals(res))
	doSomething
	
 # 释放的时候可以判断当前锁的uuid的值是否等于之前的值从而可以节省时间
```

### 3.14 大量key同时过期的注意事项

```shell
集中过期，由于清除大量key很耗时，会出现短暂的卡顿现象
- 解决方案：在设置key的过期时间的时候，给每个key加上随机值
```

### 3.15 `copy-on-write`

```shell
如果有多个调用者要求相同的资源(如内存或磁盘上的数据存储)，他们会共同获取相同的指针指向相同的资源，直到某个调用者试图修改资源的内容的时候，系统才会真正复制一个副本给该调用者，而其他调用者者所看到的最初的资源仍然保持不变
```

### 3.16 redis 持久化

```shell
- AOF(APPEND-ONLY-FILE)持久化

	- 配置项:
		- appendonly yes
		- appendsync everysec/always/no(交给操作系统决定)
    - 注意：
    	- 以aof方式启动redis不会再去读取rdb文件
    - 日志重写
    	- 调用fork创建一个子进程
    	- 子进程把内存中的快照数据进行AOF重写（直接将存储的数据转化为redis操作指令进行写入）， 新的AOF写到一个临时文件里，不依赖原来的AOF文件
    	- 主进程持续将新的变动同时写到内存和原来的AOF里
    	- 主进程获取子进程重写AOF的完成信号，往新的AO同步增量变动
    	- 使用新的AOF文件替换旧的AOF文件
```

- RDB和AOF的优缺点

```shell
RDB优点：全量数据快照，文件小，恢复快
RDB缺点：无法保存最近一次快照之后的数据
AOF优点：可读性高，适合保存增量数据，数据不易丢失
AOF缺点：文件体积大，恢复时间长
```

RDB-AOF混合持久化方式(redis4.0之后)

```shell
- BGSAVE做镜像全量持久化，AOF做镜像增量持久化
```

### 3.17 为什么使用Pipeline?

- `Pipeline`和`Linux`的管道类似

- `Pipeline`批量执行命令，节省多次IO往返的时间

### 3.18 `Redis`的同步机制

```shell
全同步过程：
	- slave发送sync命令到Master
	- Master启动一个后台进程，将redis中的数据快照保存到文件中
	- Master将保存数据快照期间接收到的写命令缓存起来
	- Master完成写文件操作后，将该文件发送给Slave
	- 使用新的RDB文件替换掉旧的RDB文件
	- Master将这期间收集的增量命令发送给slave
	
增量同步：
	- Master接受到用户的操作指令，判断是否需要传播到slave
	- 将操作记录追加到AOF文件中
	- 将操作传播到其他的Slave: 1、对齐主从库；2、往响应缓存写入指令
	- 将缓存中的数据发送给slve
```

### 3.19 `redis sentinel`

```shell
解决主从同步Master宕机后的主从切换问题：
	- 监控：检查主从服务器是否运行正常
	- 提醒：通过api向管理员或者其他应用程序发送故障通知
	- 自动故障迁移：主从同步
	
流言协议Gossip
	- 杂乱无章中寻求一致
	- 每个节点都随机地与对方通信，最终所有节点地状态达成一致
	- 种子节点定期随机向其他节点发送节点列表以及需要传播地消息
	- 不保证信息一定会传递给所有节点，但是最终会趋于一致
```

### 3.20 `redis`的集群原理

```shell
如何从海量数据中快速找到所需？

一致性哈希算法   哈希环 顺时针 数据倾斜(数据在某一节点区间内分布较多) 虚拟节点映射

取模方式不行？
增加节点 hash(key)%(N+1) 则所有原有缓存的位置基本上都会发生改变，导致缓存失效 5%4 ==> 5%5
减少节点 hash(key)%(N-1)

redis cluster的hash slot算法
crc16
crc16(key) % 16384
多写增加master节点， 多读增加slave节点
```

### 3.21 `redis`常见的数据淘汰策略

```shell
voltile-lru：从已设置过期时间的数据集（server.db[i].expires）中挑选最近最少使用的数据淘汰
volatile-ttl：从已设置过期时间的数据集（server.db[i].expires）中挑选将要过期的数据淘汰
volatile-random：从已设置过期时间的数据集（server.db[i].expires）中任意选择数据淘汰
allkeys-lru：从数据集（server.db[i].dict）中挑选最近最少使用的数据淘汰
allkeys-random：从数据集（server.db[i].dict）中任意选择数据淘汰
```

## 4. web框架和wsgi

### 4.1什么wsgi？

- `Python Web Server Gateway Interface(pep3333)`
- 描述了`Web Server（Gunicorn/uwsgi）`如何与`web`框架`(Flask/Django)`交互，`Web` 框架如何处理请求

`def application(environ, start_response)`

- application就是WSGI app一个可调用对象
- 参数
  - environ：一个包含`WSGI`环境信息的字典，由`WSGI`服务器提供，常见的`key`有`PATH_INFO,QUERY_STRING`等
  - start_reponse：生成WSGI响应的回调函数，接收两个参数`status`和`headers`
- 函数返回响应体的可迭代对象

```python
from wsgiref.simple_server import make_server


def my_app(environ, start_response):
    print(environ['QUERY_STRING'])
    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf8')]
    start_response(status, headers)
    return [b'<h1>Hello world</h1>']  # 可迭代对象


if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 8888, my_app)
    httpd.serve_forever()
```

### 4.2常用的`Python Web`框架`Django/Flask/Tornado` 对比

### 4.3Web框架的组成（淡化框架，加强基础）

## 5.python2和python3的差异

### 5.1python3改进

- print成为函数
- 编码问题，Python3不再有Unicode对象，默认str就是unicode
- 除法变化，python3除法默认返回浮点数
- 类型注解(`type hint`)。帮助IDE实现类型检查
- 优化的`super()`方便直接调用父类函数
- 高级解包操作。`a,b,*rest = range(10)`
- `Keyword only arguments`。限定关键字参数
- `Chained Exceptions`。`Python 3`重新抛出异常不会丢失栈信息
- 一切返回迭代器`range,zip,map,dict.values,etc.are all iterators`。
- 类型注解

## 6.Python内置数据结构算法

![](./pic/6.python内置数据结构和算法/python内置数据结构和算法.PNG)

### 1.LRU算法

## 7.系统设计

### 1.短网址系统设计与实现

```sql
CREATE TABLE short_url(
id bigint unsigned NOT NULL AUTO_INCREMENT,
token varchar(10),
url varchar(2048),
created_at timestamp not null default CURRENT_TIMESTAMP,
key `idx_token`(`token`)
)
```

```

- 简单实现

​```python
from string import ascii_letters, digits

from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL
from flask_redis import FlaskRedis

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
redis_store = FlaskRedis(app)

CHARS = ascii_letters + digits


def encode(num: int) -> 'str':
    if num == 0:
        return CHARS[0]
    res = []
    while num:
        num, rem = divmod(num, len(CHARS))
        res.append(CHARS[rem])
    return ''.join(reversed(res))


@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json['url']
    index = int(redis_store.incr('SHORT_CNT'))
    token = encode(index)
    sql = "INSERT INTO short_url(token, url) VALUES (%s, %s)"
    cur = mysql.connection.cursor()
    cur.execute(sql, (token, long_url))
    mysql.connection.commit()
    short_url = 'http://short.com/' + token
    return jsonify(url=short_url)


if __name__ == '__main__':
    app.run()
```



### 2.抢红包系统设计与实现

### 3.秒杀系统

### 4.评论系统

## 8. 面试中不会的问题

```shell
1.redis如何删除过期的key
	- 被动删除：当读/写一个已经过期的key时，会触发惰性删除策略，直接删除掉这个过期key
	- 主动删除：由于惰性删除策略无法保证冷数据被及时删掉，所以Redis会定期主动淘汰一批已过期的key
	- 当前已用内存超过maxmemory限定时，触发主动清理策略
	文章链接：https://blog.csdn.net/u013308490/article/details/83105470
2.描述lru算法
LRU全称是(Least Recently)Used，即最近最久未使用的意思。
LRU算法的设计原则是：如果一个数据在最近一段时间没有被访问到，那么在将来它被访问的可能性也很小。也就是说，当限定的空间已存满数据时，应当把最久没有被访问到的数据淘汰。
3.浮点数的表示



4.rabbitmq消息重复如何处理

消息重复
造成消息重复的根本原因是：网络不可达。只要通过网络交换数据，就无法避免这个问题。所以解决这个问题的办法就是绕过这个问题。那么问题就变成了：如果消费端收到两条一样的消息，应该怎样处理？

消费端处理消息的业务逻辑保持幂等性。

保证每条消息都有唯一编号且保证消息处理成功与去重表的日志同时出现。

第 1 条很好理解，只要保持幂等性，不管来多少条重复消息，最后处理的结果都一样。第 2 条原理就是利用一张日志表来记录已经处理成功的消息的 ID，如果新到的消息 ID 已经在日志表中，那么就不再处理这条消息。

第 1 条解决方案，很明显应该在消费端实现，不属于消息系统要实现的功能。第 2 条可以消息系统实现，也可以业务端实现。正常情况下出现重复消息的概率其实很小，如果由消息系统来实现的话，肯定会对消息系统的吞吐量和高可用有影响，所以最好还是由业务端自己处理消息重复的问题，这也是 RabbitMQ 不解决消息重复的问题的原因。


5.rabbitmq如何保证消息的次序
场景：比如下单操作，下单成功之后，会发布创建订单和扣减库存消息，但扣减库存消息执行会先于创建订单消息，也就说前者执行成功之后，才能执行后者。
不保证完全按照顺序消费，在 MQ 层面支持消息的顺序处理开销太大，为了极少量的需求，增加整体上的复杂度得不偿失。
所以，还是在应用层面处理比较好，或者业务逻辑进行处理。
应用层解决方式：
1. 消息实体中增加：版本号 & 状态机 & msgid & parent_msgid，通过 parent_msgid 判断消息的顺序（需要全局存储，记录消息的执行状态）。
2. “同步执行”：当一个消息执行完之后，再发布下一个消息。

6.MySQL大表在增加字段与索引的过程中如何避免表上锁
7.描述redis的AOF重写的过程
	获取数据在内存中的快照，同时开启缓存负责记录重写期间的写入操作指令，AOF重新生成完毕后，将缓存中的指令醉驾到AOF文件尾部
8.rabbitmq中的三种模式
    - Fanout
    - Direct
    - Topic
    
9.docker的几种网络模式
我们在使用docker run创建Docker容器时，可以用--net选项指定容器的网络模式，Docker有以下4种网络模式：

· host模式，使用--net=host指定。
· container模式，使用--net=container:NAME_or_ID指定。
· none模式，使用--net=none指定。
· bridge模式，使用--net=bridge指定，默认设置。

1 host模式

Docker使用的网络实际上和宿主机一样，在容器内看到的网卡ip是宿主机上的ip。

众所周知，Docker使用了Linux的Namespaces技术来进行资源隔离，如PID Namespace隔离进程，Mount Namespace隔离文件系统，Network Namespace隔离网络等。一个Network Namespace提供了一份独立的网络环境，包括网卡、路由、Iptable规则等都与其他的Network Namespace隔离。一个Docker容器一般会分配一个独立的Network Namespace。但如果启动容器的时候使用host模式，那么这个容器将不会获得一个独立的Network Namespace，而是和宿主机共用一个Network Namespace。容器将不会虚拟出自己的网卡，配置自己的IP等，而是使用宿主机的IP和端口。

2 container模式
多个容器使用共同的网络看到的ip是一样的。

在理解了host模式后，这个模式也就好理解了。这个模式指定新创建的容器和已经存在的一个容器共享一个Network Namespace，而不是和宿主机共享。新创建的容器不会创建自己的网卡，配置自己的IP，而是和一个指定的容器共享IP、端口范围等。同样，两个容器除了网络方面，其他的如文件系统、进程列表等还是隔离的。两个容器的进程可以通过lo网卡设备通信。

3 none模式

这种模式下不会配置任何网络。
这个模式和前两个不同。在这种模式下，Docker容器拥有自己的Network Namespace，但是，并不为Docker容器进行任何网络配置。也就是说，这个Docker容器没有网卡、IP、路由等信息。需要我们自己为Docker容器添加网卡、配置IP等。

4 bridge模式

bridge模式是Docker默认的网络设置，此模式会为每一个容器分配Network Namespace、设置IP等，并将一个主机上的Docker容器连接到一个虚拟网桥上。

类似于Vmware的nat网络模式。同一个宿主机上的所有容器会在同一个网段下，相互之间是可以通信的。
```



## 9.python常见的面试题

```shell
https://www.cnblogs.com/it-xiaozhi/p/9906026.html		# 很经典很详细



```














