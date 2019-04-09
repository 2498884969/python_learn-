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

### 1.1 B+-Tree

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

### 3. 索引模块

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

## 2.WEB安全

### 1. SQL注入

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

### 2.XSS攻击

**XSS（Cross Site Scripting）跨站脚本攻击**

- 恶意用户将未进行转义的代码植入到提供给其他用户使用的页面中，未经转义的恶意代码输出到其他用户的浏览器被执行
- 用户浏览页面的时候嵌入页面的脚本(js)会被执行，对于用户进行攻击
- 主要分为两类：反射型（非持久型）、存储型（持久型）

**XSS危害**

- 盗用用户的cookie，获取敏感信息
- 利用私人账号执行一些违法操作，比如盗取个人或者商业资料，执行一些隐私操作
- 甚至可以在一些访问量很大的网站上实现DDoS攻击

**XSS防范**