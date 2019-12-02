## 1. 安装

```shell
# docker 安装
https://blog.csdn.net/weixin_40461281/article/details/92610876
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

```shell
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
```



