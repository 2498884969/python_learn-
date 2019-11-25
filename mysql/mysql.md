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

## 3.名词

```shell
collation	英[kəˈleɪʃn] 校对整理
同一条记录在系统中可以存在多个版本，就是数据库的多版本并发控制（MVCC）
```



