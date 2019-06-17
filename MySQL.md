## 1.基础及及架构

### 1.MySQL server

- 客户端进程向服务端进程发送一段文本(SQL语句), 服务器进程处理后再向客户端进程发送一段文本(处理结果); 
- 服务端处理可以分为三部分:
  - 连接管理: MySQL服务器会为每一个连接进来的客户端分配一个线程;
  - 解析优化: 包括语法解析(编译), 查询优化(外连接转换为内连接、表达式简化、子查询转为连接);
  - 存储引擎: 对数据的存储和提取操作的封装

![MySQL](image/mysql.jpg)

### 2.常用的存储引擎

- `InnoDB`: 具备外键, 支持事务和部分事务回滚(Savepoints), 支持分布式事务(XA)
- `MyISAM`: 占用空间小, 处理速度快, 但不支持事务完整性和并发;
- `Memory`: 存储于内存中, 默认使用哈希索引, 速度快.

### 3.系统变量和状态变量

> 系统变量: 配置MySQL服务器的运行环境, 可以通过**配置文件**, **启动选项**, 或运行时进行配置;
>
> 状态变量: 监控MySQL服务器的运行状态;

- 查看系统变量: `show variables;` 或者`show variables like 'log%';`
  - 优先显示会话级别变量, 不存在则显示全局变量;
  - 可以使用`show global variables;`指定显示全局变量;
- 通过`set [GLOBAL|SESSION] variable_name = value`;
  - 例如`SET GLOBAL sort_buffer_size=value; 或 SET @@global.sort_buffer_size=value;`
- 重要变量:
  - `max_connections`: 最大连接数;
  - `auto_increment_increment`: 自增增量;
  - `auto_increment_offset`: 起始自增点;
- 查看状态变量: `show status`或者`show status like 'Threads%';`

### 4.服务端启动配置

- 默认会读取响应目录下的`my.cnf`文件;
- `mysqld_save`: 会间接调用`mysqld`, 在启动后监控`mysqld`的运行情况;
- 使用`--defaults-file`指定配置文件;

### 5.字符编码

- 使用`show charset`查看支持的字符编码;
- 常用字符编码:
  - `utf8bm4`: 正宗`utf-8`编码, 

### 6.数据类型

- 存储数据最小的数据类型通常更好, 但要确保没有低估需要存储的值的范围;
- 简单更好; 简单数据类型通常需要更少的CPU周期;
- 尽量避免NULL, MySQL难以优化包含NULL的列;

- 常用数据类型: `INT, FLOAT, DOUBLE, DATA, TIME, CHAR, VARCHAR, TEXT...`
    - `VARCHAR`: 可变长字符串, 适用于列的最大长度比平均长度大很多, 列的更新很少的数据; 频繁更新会导致碎片化;
    - `CHAR`: 定长, 对于经常变更的数据也不容易产生碎片; 存储空间上比`VARCHAR`更有效率;
    - `BLOB`: 存储的是二进制数据, 没有排序规则或字符集;
    - `TEXT`: 存储的是字符


## 2.库和表操作

> 帮助使用：
>
> - 按层次看帮助：`mysql>? contents` 会按分类列出项，然后可以再选择感兴趣的方向
>
> - 直接快速查询：`mysql>? show`

### 1.数据库操作

- 创建: `CREATE DATABASE db_name;`

- 查看：`SHOW {DATABASES|SCHEMAS} ` ；

- 修改：`ALTER {DATABASE|SCHEMAS} [db_name] [DEFAULT] CHARACTER SET [=] charset_name;`

- 删除：`DROP {DATABASE|SCHEMA} [IF EXISTS] db_name;`


- 使用数据库：`USE database_name;`

### 2.表定义操作

- 创建：`CREATE TABLE table_name(colume_name data_type,...);`
  - 设置主键: `PRIMARY KEY`;
  - 设置非空: `NOT NULL`;
  - 唯一约束: `UNIQUE`;
  - 设置外键: `FOREIGN KEY (f_key_name) REFERENCES tab_name(colume_name)`;
  - 设置自增: `AUTO_INCREMENT`;
    - 默认值: `DEFAULT 默认值`;
- 查看：`SHOW TABLES;`
- 查看名为`tb_name`的数据表的详细结构：`SHOW COLUMNS FROM tb_name;` | `DESCRIBE tab_name;`或者`EXPLAIN tab_name;`
- 修改数据表内容：`ALTER TABLE 表名 ...`
- 重命名: `... RENAME 新表名`
  - 修改字段:
    - 修改字段数据类型和索引: `... MODIFY 属性名 数据类型 约束 类型 [FIRST|AFTER xxx] ;`
    - 修改字段名称: `... CHANGE 旧字段名 新字段名 属性;`
  - 添加字段:
    - 添加：`... ADD 字段名 属性 [FIRST|AFTER col_name]`
    - 添加多列：`... ADD (字段名1 属性, 字段名2 属性);`
  - 删除字段：
    - `... DROP col_name;`
  - 删除约束:
    - 删除主键约束：`... DROP PRIMARY KEY;`
  - `DROP`和`ADD`可以混用，用`,`隔开即可；
  - 修改表的存储引擎: `... ENGINE=存储引擎名`

- 删除: `DROP TABLE tab_name`

## 3.数据增删改查

### 1.表记录操作

- 向数据表中写入记录`INSERT` ：
  - `INSERT [INTO] tbl_name [(col_name)] {VALUES|VALUE}({expr|DEFAULT},...),(...);`
  - `INSERT [INTO] tbl_name SET col1_name={expr|DEFAULT},col2_name={expr|DEFAULT}，...;` 每次只能插入一组信息；与第一种的区别：此种方式可以使用子查询； 
  - `INSERT [INTO] tbl_name [(col_name, ...)] SELECT ...;` 可将查询结果插入到指定数据表中；
- 从文件中加载数据`LOAD DATA INFILE`：
  - `LOAT DATA INFILE '文件路径' INTO TABLE tab_name [LINES TERMINATED BY '\r\n'];`
- 更新记录`UPDATE` ：
  - `UPDATE [LOW_PRIORITY] [IGNORE] table_reference SET col_name1={expr1|DEFAULT},...[WHERE where_condition]`
- 删除记录`DELETE` ：
  - `DELETE FROM tbl_name [WHERE where_condition];` 

### 2.表查找操作

> 查询表达式：每个表达式表示想查找的一列，必须有至少一个；多列之间以英文逗号分隔；

```sql
SELECT [distinct] select_expr [,select_expr ...]
[
  FROM table_references
  [WHERE where_condition]
  [GROUP BY {col_name|position}]
  [HAVING where_condition]
  [ORDER BY {col_name|expr|position} [ASC|DESC],...]
  [LIMIT {offset, row_count} | {row_count OFFSET offset}]
]
```

- `[distinct]`: 表示去掉重复, 默认不去除;
- 记录的查找：`SELECT col1_name，col2_name... FROM tbl_name WHERE 限制;` 显示列将按请求顺序显示 ，可以同时查询多张表的内容；
- 还可以对显示类名进行==别名==操作：`SELECT col_name AS new_col_name FROM tab_name;`
- 把一列中相同的项合并：`SELECT DISTINCT col_name FROM tab_name;` 可以用`GROUP BY`实现；
- `UNION [ALL]` : 将两个查询结果合并为一个，`UNION` 会合并相同项，`UNION ALL` 全部显示，速度要快很多；
- `WHERE`后跟限制条件，提高查询精度；
  - 限制条件可以用比较符号，也可用`AND OR`连接多个限制： `age>18 AND age<35`, MySQL 在处理OR操作之前, 优先处理AND操作符号;
  - `IN` 和 `NOT IN`：`WHERE age NOT IN(26, 27);  WHERE age IN(18);` 括号中为枚举,而不是范围;
  - `IS NULL` 和 `IS NOT NULL` :
  - 模式匹配：关键词`LIKE`和通配符一起使用，==`_` :匹配一位，`%` :不定长通配==；例：`WHERE age LIKE ’2_‘`
  - 也可以使用`NOT LIKE`反向匹配；
  - 正则表达式：利用关键词`REGEXP ...` , 
- 查询结果分组`GROUP BY`：`[GROUP BY {col_name|position} [HAVING where_condition], ...];` `；
  - `GROUP BY` 通常伴随着对领外一些列进行聚合运算, 如sum, avg,max, min等;
  - `HAVING` ，`WHERE` 关键字无法和聚合函数一起使用, 所以引入`HAVING`; 例如:`...HAVING SUM(xxx)>100`
- 查询结果排序`ORDER BY` ：默认升序(`ASC`)，降序(`DESC`)，例：`ORDER BY {col_name|position} [ASC|DESC] ，{col_name|positin} [ASC|DESC];` 可以设置多条规则，当前条满足后，对其中相等的再次排序；
- 限制查询结果返回的数量`LIMIT` ：
  - `LIMIT {[offset,] row_cout` 即从第`offset`条开始（0开始）返回`row_count`条结果； 
  - `LIMIT row_count OFFSET offset}`  同上；
- 内置函数和计算：`COUNT(),SUM(),AVG(),MAX(),MIN();`

### 3.子查询和连接

#### a.子查询

> 子查询（subquery）指出现在其他SQL语句(增删改查)内的SELECT子句，用小括号包围；子查询外层可以是：SELECT、INSERT、UPDATE、SET、或DO；

- 三种引发子查询的方式：
  - `>, <,<= ,>=` 比较运算符引起的子查询：可以用`ANY, SOME, ALL`修饰比较运算符号，符合其中的（ANY，SOME）一个，所有（ALL）；
  - `[NOT] IN`引发的子查询：`... IN(SELECT ...);`
  - `[NOT] EXISTS`引发的子查询：如果子查询返回任何行，`EXISTS`将返回TRUE；
- 将查询结果写入数据表：`INSERT [INTO] tbl_name [(col_name,..)] SELECT ...`
- 多表更新：参照另外的表更新本表的记录；`UPDATE table_references SET`
- `CREATE...SELECT`:创建数据表的同时，将查询结果写入到数据表，

#### b.连接

> 连接：需要从多个表中查询数据,

- 原先查询信息从单个表中查询，使用连接可以==将多个表合并为一张供查询的表==，从而整合多表信息；
- 语法结构：`A表 连接类型 B表 ON 连接条件 筛选条件` ：`table_reference1 {INNER JOIN| | LEFT JOIN | RIGHT JOIN} table_reference2 ON conditional_expr WHRER ...;` 一般用`ON`关键字来设定连接条件，用`WHERE`关键字进行结果及记录的过滤。
- 连接类型：内连接、左外连接、右外连接；
  - 内连接`[INNER JOIN]`: 仅显示符合连接条件的记录，即交集部分；
  - 左外连接`LEFT JOIN`:从左表那里返回所有的行, 即使右表中没有匹配的行;
  - 右外连接 `RIGHT JOIN`:从右表那里返回所有的行, 即使左表中没有匹配的行;


- 连接查询：在处理多个表时，子查询只能查询显示同一个表中的信息。如果需要多个表中信息，则需要连接（join）操作，基本思想就是把两个表当做一个新的表来操作；例如：

  ```sql
  SELECT id,name,people_num 
  FROM emplyee,department 
  WHERE emplyee.in_dpt=department.dpt_name;
   
  #等同于
  SELECT id,name,people_num 
  FROM emplyee JOIN department 
  ON emplyee.in_dpt=department.dpt_name
  WHERE ...;

  ```

- 多表连接：

  ```SQL
   SELECT A.xxx, b.xxx 
   FROM A
   JOIN (B, C)
   ON A.xx = B.xx AND/&& B.xx=C.xx
   WHERE =...
  ```

## 4.索引

> 索引: 存储引擎用于快速找到记录的一种数据结构; 存储引擎会先在索引中找到对应值, 然后根据匹配的索引记录找到对应的数据行.
>
> 参考: **<<高性能MySQL>> 第五章**

### 1.索引概述

- 索引是在存储引擎层级实现的, 通常使用B树或B+树, 此外还有哈希索引, 空间数据索引(R树):
  - 哈希索引: 基于哈希表实现, 用于精确匹配索引.
  - 空间数据索引: 可以用作地理数据存储;
  - 全文索引: 查找文本中的关键字;

-   索引本质：本质就是数据结构；数据库的基本操作就是查询，每种不同的查询的算法又依赖于数据结构；所以，数据之外，数据库还维护着满足特定查找算法的数据结构，这些数据结构以某种方式引用（指向）数据；这种数据结构，就是索引；

    ![索引](http://blog.codinglabs.org/uploads/pictures/theory-of-mysql-index/1.png)



- 目前大部分数据库系统及文件系统都采用B-Tree或B+Tree作为索引；
- 查看索引信息：`SHOW {INDEX|KEYS} FORM tab_name;`
- 对某个表的某列建立索引：
  - `ALTER TABLE tab_name ADD INDEX index_name(col_name);` 或者
  - `CREATE INDEX index_name ON tab_name(col_name);`

- 索引优点: 
  1. 减少了服务器需要扫描的数据量;
  2. 帮助服务器避免排序和临时表;
  3. 将随机I/O变为顺序I/O;

### 2.索引策略

- 索引选择性: 不重复的索引值和数据表的记录总数的比值, 选择性越高的索引, 查找时过滤掉的行越多;
- 

## 5.运算符和函数

### 1.字符函数

- `CONCAT()` :用于字符连接，可以连接多个字符串，`CONCAT('lfeng', 'hqh', 'xiaoxi');`
- `CONCTA_WS()` ：用指定分隔符(可以为字符串)连接，第一个参数为分隔符，`CONCAT_WS('---', 'lfeng', 'hou');`
- `FORMAT()`：数字格式化千分位，第二个参数指定小数点后的位数；`FORMAT(1235.12312, 2);`
- `LOWER()` :字符串转为小写；`LOWER('MySQL');`
- `UPPER()` :字符串转为大写；`LOWER('MySQL');`
- `LEFT()` ：从字符串的左测获取指定数目的字符；`LEFT('MySQL', 2);`
- `RIGHT()`：从字符串的右侧获取指定数目的字符；`RIGHT('MySQL', 3);`
- `LENGTH()`：获取字符串的长度；`LENGTH('lfeng');`
- `LTRIM()` ：删除字符串前导空格（首字母前的空格）；
- `RITIM()`  ：删除字符串后导空格（后续空格）；
- `TRIM()` ：删除前导和后导空格；
- `SUBSTRING()` :进行字符串截取；从第几位开始，截取n位，`SUBSTRING（'MySQL', 1, 2）--> 'My'`
- `REPLACE()` ：替换，将字符串中的`A`替换为`B`；`REPLACE('???My??SQL??', '??', ''); -->'?MySQL'`,
- `[NOT] LINE` ：

### 2.数值运算符与函数

- `CEIL()`：进一取整，小数位舍弃，整数+1,；
- `FLOOR()` ：舍一取整，小数位舍弃，
- `POWER()` ：幂运算，n的m次方，`POWER(2,3);`
- `ROUND()` ：四舍五入小数位，`ROUND(2.125, 2); -->2.13` ，位数可以为负，表示整数位；
- `TRUNCATE()` ：数字截断，不做四舍五入；

### 3.比较运算符与函数

- `[NOT] BETWEEN ... AND ...` ：在范围之内；
- `[NOT] IN` ：在不在其中；
- `IS [NOT] NULL` ： 是否为空；

### 4.聚合函数

只有一个返回值

- `AVG()` ：平均值；
- `COUNT()` ：计数，`COUNT(*)` ：返回被选行数；
- `MAX()` ：最大值
- `MIN()` ：最小值
- `SUM()` ：某列的总和；

### 5.加密函数

- `MD5()` ：信息摘要算法；
- `PASSWORD()` ：

### 6.日期时间函数

- `NOW()` ：当前日期和时间；
- `CURDATE()` ：当前日期；
- `CURTIME()` ：当前时间；

## 视图和触发器

## 6.存储过程和函数

### 1.存储过程

> 存储过程: 类似于脚本, 保存了多条MySQL语句的集合;

```sql
-- 创建名为 productpricing 的存储过程
CREATE PROCEDURE productpricing()
BEGIN
	SELECT Avg(prod_price) AS priceaverage
	FROM products;
END;
-- 调用名为 productpricing 的存储过程, 
CALL productpricing();

-- 存储过程也可使用参数

-- 删除存储过程
DROP PROCEDURE productpricing IF EXISTS;
```

### 2.cursor 游标

> 游标: 存储在MySQL服务器上的数据库查询, 是语句检索出的结果集. MySQL游标只能用于存储过程(和函数)

- ```sql
  -- 存储过程(或函数)内
  BEGIN
  	-- 声明变量 o 
  	DECLARE o INT;
  	-- 声明游标 ordernumbers
  	DECLARE ordernumbers CURSOR
  	FOR
  	SELECT order_num FROM orders;
  	-- 打开游标
  	OPEN ordernumbers;
  	-- 获取值
  	FETCH ordernumbers INTO o;
  	-- 关闭游标
  	CLOSE ordernumbers;
  END;
  ```

## 7.备份还原





## 8.安全

### 1.权限管理

- 授权
  - `GRANT priv_type ON database.table TO user [IDENTIFIED BY 'password']`
  - `priv_type`为权限, `all`所有权限;
- 回收权限
  - `REVOKE priv_type ON databases.table FROM user;`
- 查看权限
  - `SHOW GRANTS FOR user;`
- SQL注入简介：利用某些数据库的外部接口把==用户数据==插入到实际的数据库==操作语言==中，从而达到入侵数据库乃至操作系统的目的。产生主要是由于程序对用户输入的数据没有进行严格的过滤，导致非法数据库查询语句的执行；
- 


## 9.调试和维护

### 1.日志

> 错误日志: 记录MySQL服务端在运行时产生的错误信息
>
> 查询日志: 记录建立的客户端连接和执行语句;
>
> 慢查询日志: 慢查询时间阈值, 以秒为单位, 超过这个阈值就是慢查询;
>
> binlog二进制日志: 对数据库进行增删改的SQL操作, 可以用这个日志做增量备份;

- 查询日志: 

## 10.调优

