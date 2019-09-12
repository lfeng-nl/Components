## 1.基础及及架构

### 1.MySQL server

- 客户端进程向服务端进程发送一段文本(SQL语句), 服务器进程处理后再向客户端进程发送一段文本(处理结果); 
- 服务端处理可以分为三部分:
  - 连接管理: MySQL服务器会为每一个连接进来的客户端分配一个线程;
  - 解析优化: 包括语法解析(编译), 查询优化(外连接转换为内连接、表达式简化、子查询转为连接);
  - 存储引擎: 对数据的存储和提取操作的封装;

![MySQL](image/mysql.jpg)

### 2.常用的存储引擎

- `InnoDB`: 具备外键, 支持事务和部分事务回滚(Savepoints), 支持分布式事务(XA)
- `MyISAM`: 占用空间小, 处理速度快, 但不支持事务完整性和并发;
- `Memory`: 存储于内存中, 默认使用哈希索引, 速度快.

### 3.服务端启动配置

- 默认会读取响应目录下的`my.cnf`文件;
- `mysqld_save`: 会间接调用`mysqld`, 在启动后监控`mysqld`的运行情况;
- 使用`--defaults-file`指定配置文件;

### 4.字符编码

- 使用`show charset`查看支持的字符编码;
- 常用字符编码:
  - `utf8bm4`: 正宗`utf-8`编码, 

### 5.数据类型

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

- 创建: `CREATE DATABASE 数据库名;`

- 查看：`SHOW {DATABASES|SCHEMAS} ` ；

- 修改：`ALTER {DATABASE|SCHEMAS} [数据库名] [DEFAULT] CHARACTER SET [=] charset_name;`

- 删除：`DROP {DATABASE|SCHEMA} [IF EXISTS] 数据库名;`


- 使用数据库：`USE 数据库名;`

    - `SELECT DATABASE();`: 当前使用数据库;
    - `SELECT NOW(), USER(), VERSION();`: 时间, 用户, 版本;

### 2.表定义操作

> PRIMARY KEY: 唯一约束, NOT NULL约束, 主键必须包含且唯一, 自动创建唯一索引;
>
> UNIQUE KEY: 唯一约束, 自动创建唯一索引;
>
> FOREIGN KEY:  规范数据引用完整性约束, 自动建立索引
>
> **以上三种KEY, 都有约束和索引双层含义 ** 

- 创建：`CREATE TABLE 表名 (字段名1 属性, 字段名2 属性, ...);`
  - 设置主键: `PRIMARY KEY`;
  - 唯一约束: `UNIQUE`;
  - 设置外键: `CONSTRAINT 外键别名 FOREIGN KEY (字段1, 字段2) REFERENCES 表明(字段名1, 字段名2)`;
  - 设置非空: `NOT NULL`;
  - 设置自增: `AUTO_INCREMENT`,  自增类必须建立索引;
  - 默认值: `DEFAULT 默认值`;
- 查看：`SHOW TABLES;`
  - 查看名为`tb_name`的数据表的详细结构：`SHOW COLUMNS FROM 表名;` | `DESCRIBE 表名;`或者`EXPLAIN 表名;`
  - 查看建表详细信息: `SHOW CREATE TABLE 表名;`
- 修改数据表内容：`ALTER TABLE 表名 ...`
  - 重命名: `... RENAME 新表名`
  - 修改字段:
    - 修改字段数据类型和索引: `... MODIFY 属性名 数据类型 约束 类型 [FIRST|AFTER 字段] ;`
    - 修改字段名称: `... CHANGE 旧字段名 新字段名 属性;`
  - 添加字段:
    - 添加：`... ADD 字段名 属性 [FIRST|AFTER col_name]`
    - 添加多列：`... ADD (字段名1 属性, 字段名2 属性);`
  - 删除字段：
    - `... DROP col_name;`
  - 删除约束:
    - 删除主键约束：`... DROP PRIMARY KEY;`
    - 删除外键约束: `... DROP FOREIGN KEY 外键别名;`, 未指定外键别名会自动生成,  请查看建表信息`SHOW CREATE TABLE 表名`
  - `DROP`和`ADD`可以混用，用`,`隔开即可；
  - 修改表的存储引擎: `... ENGINE=存储引擎名`

- 删除: `DROP TABLE 表名`

## 3.数据增删改查

### 1.数据增删改

- 插入:
  - `INSERT [INTO] 表名 VALUES (值1, 值2...),((值1, 值2...))` ：给所有字段插入一组或多组值;
  - `INSERT [INTO] 表名 (字段1, 字段2) VALUES (值1, 值2...),((值1, 值2...));`: 给字段字段插入一组或多住值;
  - `INSERT [INTO] 表名 SET 字段1=值1,字段2=值2，...;` 每次只能插入一组信息；与第一种的区别：此种方式可以使用子查询； 
  - `INSERT [INTO] 表名 (字段1, 字段2...)] SELECT ...;` 可将查询结果插入到指定数据表中；
- 从文件中加载数据`LOAD DATA INFILE`：
  - `LOAT DATA INFILE '文件路径' INTO TABLE tab_name [LINES TERMINATED BY '\r\n'];`
- 更新：
  - `UPDATE 表名 SET 字段1=值1, 字段2=值2,...WHERE 条件;`
- 删除：
  - `DELETE FROM 表名 WHERE 条件;` 

### 2.表查找操作

- 基本查询:

  ```mysql
  SELECT [DISTINCT] 属性1, ...FROM 表名
  [
    [WHERE 条件1]
    [GROUP BY 属性1 [HAVING 条件2]]
    [ORDER BY 属性2 [ASC|DESC],...]
  ]
  ```

- `WHERE`子句: 

  - 大小比较: `=, <, <=, >, >=, !=`
  -  集合`IN|NOT IN`:  `... WHERE id IN (1, 5, 10) ;`
  - 范围`[NOT] BETWEEN AND`:  `... WHERE id BETWEEN 1 and 10;`
  - 匹配字符`[NOT] LIKE`: `... WHERE name LIKE 'l%';`
    -  `%`: 任意长度字符串, 长度可以为0;
    - `_`: 匹配单个字符;
  - 空值`IS [NOT] NULL`
  - 多个条件`AND, OR`: `WHERE id=1 OR name='test';`

- 去重`DISTINCT `:  `SELECT DISTINCT name FROM product;`

- 排序`ORDER BY 字段 [ASC|DESC]`: 安照指定字段的升序或降序排序; 

- 别名`... 字段 AS 字段别名 FROM ...;`

- 分组 `GROUP BY` ：
  - 通常伴随着对另外一些列进行聚合运算, 如`sum, avg, max, min`等;  `SELECT 字段2, max(字段1) from 表名 GROUP BY 字段2;` 
  - 加条件限制`HAVING` : `...HAVING SUM(xxx)>100`, 注意, `WHERE`用于表和视图, `HAVING`用于分组;

- 限制返回数量`LIMIT` ：
  - `... LIMIT 数量` : 仅返回指定数量的查询结果； 
  - `... LIMIT 初始位置 数量` : 返回从指定位置开始的指定数量结果;

- 聚合(集合)函数：`COUNT(),SUM(),AVG(),MAX(),MIN();`

### 3.连接查询和子查询


#### 1.连接查询

> 连接查询: 将两个或两个以上的表按某个条件连接, 从中查询数据;

- 连接：`SELECT * FROM 表1 [连接形式] 表2 ON 表1.字段1=表2.字段2 WHERE 条件;`  
  - 一般用`ON`关键字来设定连接条件，用`WHERE`关键字进行结果及记录的过滤。
- 连接类型：内连接、左外连接、右外连接；
  - 内连接`JOIN`: 仅显示符合连接条件的记录，即交集部分；
  - 左外连接`LEFT JOIN`:从左表那里返回所有的行 ;
  - 右外连接 `RIGHT JOIN`:从右表那里返回所有的行;


- 内连接的两种写法:

  ```sql
  # 写法1
  SELECT a.字段1, b.字段2 
  FROM 表1 AS a, 表2 AS b 
  WHERE 表1.字段1=表2.字段3;
   
  #写法2
  SELECT a.字段1, b.字段2 
  FROM 表1 AS a JOIN 表2 AS b 
  ON 表1.字段1=表2.字段3
  WHERE 条件;
  
  ```

- 多表连接：

  ```SQL
   SELECT A.xxx, b.xxx 
   FROM A
   JOIN (B, C)
   ON A.xx = B.xx AND|&& B.xx=C.xx
   WHERE =...
  ```
#### 2.子查询

> 出现在其他SQL语句(增删改查)内的`SELECT`子句，用小括号包围；内层查询语句为外层查询语句提供查询条件. 

- 带`IN`关键字子查询:
  - `... WHERE 字段1 IN (SELECT 字段2 FROM 表名);`
- 带比较运算符的子查询, `=, !=, >, >=, <, <=`:
  - `... WHERE 字段1 >= (SELECT 字段1 FROM 表名 WHERE 条件);`
- 带`EXISTS`关键字子查询:
  - 如果内层查询到结果, 返回为`true`, 反之为`yes`;
- 带`ANY`关键字子查询:
  - 只要满足内层查询语句返回结果中的任何一个;
  - `.... WHERE 字段1 >= ANY (SELECT 字段2 FROM 表名);`
- 带`ALL`关键字子查询:
  - 需要满足内层查询的所有结果;
  - `... WHERE 字段1 >= ALL (SELECT 字段2 FROM 表名);`

- *子查询的性能问题*
  - 子查询通常不会像我们认为的那样, 由内到外执行, 性能上会有很大的问题;
  - 尽量避免使用子查询;

### 4.合并查询结果

- `UNION`: 合并查询结果, 相同记录消除; `SELECT 语句1 UNION SELECT 语句2;`
- `UNION ALL`: 合并查询结果, 不消除相同记录;  `SELECT 语句1 UNION ALL SELECT 语句2;`

## 4.索引

> 索引: 存储引擎**对索引的数据**维护一种数据结构, 达到快速查找的目的. 索引能够显著提高查询效率, 但是创建和维护索引需要消耗时间;
>
> 大多数MySQL索引(PRIMARY KEY, UNIQUE, INDEX, FULLTEXT) 存储在B树, 空间数据类型的索引使用R树.
>
> 参考: **<<高性能MySQL>> 第五章**

### 1.索引类型

- B-Tree索引: 使用B-Tree(B+Tree)数据结构来存储数据;

    - 比较`=, > , <,`或是不以通配符匹配开头字符的`LIKE`语句;

- 哈希索引: 基于哈希表, 只有精确匹配的查询才有效; 只有`Memory`引擎支持;

    - 适用于`=`或`!=`运算符()精确匹配)
    - 只有整个键可用于搜索(哈希值不同);

- 单列索引:

    - 索引前缀: 只用指定字段的指定前缀长度(**最长 1000个字节**)作为索引, `CREATE TABLE xxx( xxx, INDEX(col(10)))`,;
    - 全文索引: 查找的是文本中的关键词, 而不是直接比较索引中的值, `MyISAM`和`InnoDB`支持;
    - 空间索引: 基于R-Tree, `MyISAM`支持, 可以用于地理数据存储;

- 多列索引:

    - 也称为复合索引, 最多包含16列;

    - `INDEX name (last_name, first_name)`;

    - 如果表具有多列索引, 则优化程序可以使用索引的任何最左前缀来查找行;

        - 最左前缀:  例如有个三列索引`(col1, col2, col3)`, 则可索引`(col1), (col1, col2), (col1, col2, col3)`

        - ```sql
            // 使用 (col1)
            SELECT * FROM tbl_name WHERE col1=val1;
            // 使用 (col1)
            // 使用 (col1, col2)
            SELECT * FROM tbl_name WHERE col1=val1 AND col2=val2;
            // 以下无法使用索引
            SELECT * FROM tbl_name WHERE col2=val2;
            SELECT * FROM tbl_name WHERE col2=val2 AND col3=val3;
            ```

- 索引使用: 优化器会根据实际情况决定是否使用索引, 即使索引存在, 也有可能不使用;

    - 

### 2.索引概述

- 优点:
    - 减少了服务器需要扫描的数据量;
    - 避免排序和临时表;
    - 将随机I/O变为顺序I/O;
- 查看索引信息：`SHOW {INDEX|KEYS} FORM tab_name;`
- 添加索引：`UNIQUE`: 唯一性索引, `FULLTEXT`: 全文索引, `SPATIAL`: 空间索引;
  - 建表时创建索引:
    - `CREATE TABLE 表名 (字段 ...) [UNIQUE|FULLTEXT|SPATIAL] INDEX|KEY [索引名] (字段1, 字段2... [(长度)] [ASC|DESC]);`
    - `ASC`升序排列, 默认;
    - `DESC`: 降序排序, 调高倒序查询速度;
  - 对已存在的表建立
      - `ALTER TABLE 表名 ADD [UNIQUE|FULLTEXT|SPATIAL] INDEX 索引名 表名(字段 [(长度)]);` 
      - `CREATE [UNIQUE|FULLTEXT|SPATIAL] INDEX 索引名 ON 表名(字段名 [(长度)]);`

- 删除索引:
  - `DROP INDEX 索引名 ON 表名;`

### 3.高效的索引策略

- 索引不能是表达式的一部分: 如`...WHERE actor_id + 1=5;`

- 前缀索引和索引选择性:

    - 对很长的字符列建立索引会使得索引变得大且慢,  通常可以索引开始的部分字符;
    - 同理, 部分情况(如前缀相同)也可以对后缀建立索引;
    - **对后缀建立索引可以采用倒序存储的方式; 结合触发器使用;**

- 多列索引

    - >多个列上建立独立索引, 在查询多个索引条件时往往得不到很好的性能(依赖数据库优化, 或者根本没有使用索引)

    - 当出现服务器需要对多个索引做相交操作时, 通常需要一个**包含所有相关列的多列索引**;

    - 当服务器需要对多个索引做联合操作时(条件有多个OR), 通常需要耗费大量的CPU和内存;

- 选择合适的**索引列顺序**


## 5.特殊主题

### 1.视图

> 视图又称虚拟表, 是由一个表或多个表导出的虚拟表; 

- 作用: 
  - 简化操作
  - 增加数据安全性, 方便设置权限
  - 提高表的逻辑独立性
  - **甚至可以将所有查询做为视图存储, 所有查询仅查询视图;**
- 创建
  - `CREATE|REPLACE [ALGORITHM={UNDEFINED|MERGE|TEMPTABLE}] VIEW 视图名[{column_list}] AS SELECT语句;`
- 查看
  - `DESCRIBE 视图名;`
- 删除
  - `DROP VIEW 视图名;`

### 2.触发器

> 触发器是由`INSERT, UPDATE, DELETE`等事件来触发某种特定操作.

- 创建:
  - `CREATE TRIGGER 触发器名 BEFORE|AFTER 触发事件 ON 表名 FOR EACH ROW BEGIN 执行语句 END;`
    - 触发事件: `INSERT, UPDATE, DELETE`
    - 使用`DELIMITER &&`修改分隔符为`&&`, 结束时修改`DELIMITER ;`

- 查看:
  - `SHOW TRIGGERS;`
  - 所有的触发器都存储在information_schema.triggers表中
- 删除:
  - `DROP TRIGGER 触发器名;`

### 3.存储过程

> 存储过程: 类似于脚本, 保存了多条MySQL语句的集合;

- 优缺点:
  - 优点: 效率高, 简化操作, 安全性好;
  - 缺点: 更新迭代麻烦, 不利于分库分表, 业务扩展后无法使用, 跟组件或ORM库无法兼容;
  
- 创建存储过程

  ```mysql
  CREATE PROCEDURE 存储过程名称(输入输出参数列表)
  BEGIN
  	sql代码
  END
  ```

- 调用存储过程: `CALL 存储过程名称;`

- 查看:
  -  `SHOW PROCEDURE STATUS LIKE '存储过程名匹配';`
  - `SHOW CREATE PROCEDURE 存储过程名;`

- 删除
  
  - `DROP PROCEDURE 存储过程名;`

### 4.cursor 游标

> 游标: 存储在MySQL服务器上的数据库查询, 是语句检索出的结果集.  MySQL游标只能用于存储过程(和函数)

- ```sql
  -- 存储过程(或函数)内
  BEGIN
  	-- 声明变量 o 
  	DECLARE o INT;
  	-- 声明游标 ordernumbers
  	DECLARE 游标名 CURSOR
  	FOR
  	SELECT order_num FROM orders;
  	-- 打开游标
  	OPEN 游标名;
  	-- 获取值
  	FETCH 游标名 INTO o;
  	-- 关闭游标
  	CLOSE 游标名;
  END;
  ```
### 5.事务

> 用来维护数据库的完整性, 保证成批MySQL要么完全执行, 要么完全不执行;
>
> 事务特性: 原子性, 一致性, 隔离性, 持久性;

- 原理: InnoDB具有自动提交特性, 普通MySQL执行语句后, 当前的数据提交操作均可被其他客户端可见, 而事务是暂时关闭"自动提交"机制, 需要commit提交持久化数据;
- 术语
    - 事务(transaction): 一组SQL语句;
    - 回退(rollback): 撤销指定SQL语句的过程;
    - 提交(commit): 将未存储的SQL语句结果写入数据表;
    - 保留点(savepoint): 事务处理中临时占位符, 可以对它发布回退;
- 控制事务:
    - `START TRANSACTION;`: 标识事务开始;
    - `ROLLBACK;` 回退事务;
    - `COMMIT`: 提交;
- 更改默认提交行为
    - `SET autocommit=0`: 不自动提交(默认自动提交, 每执行一条SQL, 立刻生效); 标志针对每个连接;

### 6.锁

-   `MyISAM`支持表锁; `InnoDB`支持行锁;
-   `LOCK TABLES tbl_name;`
-   `UNLOCK TABLES;`

### 7.运算符和函数

#### 1.字符函数

- `CONCAT()` :用于字符连接，可以连接多个字符串，`CONCAT('lfeng', 'hqh', 'xiaoxi');`
- `CONCTA_WS()` ：用指定分隔符(可以为字符串)连接，第一个参数为分隔符，`CONCAT_WS('---', 'lfeng', 'hou');`

#### 2.数值运算符与函数

- `CEIL()`：进一取整，小数位舍弃，整数+1,；
- `FLOOR()` ：舍一取整，小数位舍弃，
- `POWER()` ：幂运算，n的m次方，`POWER(2,3);`
- `ROUND()` ：四舍五入小数位，`ROUND(2.125, 2); -->2.13` ，位数可以为负，表示整数位；
- `TRUNCATE()` ：数字截断，不做四舍五入；

#### 3.比较运算符与函数

- `[NOT] BETWEEN ... AND ...` ：在范围之内；
- `[NOT] IN` ：在不在其中；
- `IS [NOT] NULL` ： 是否为空；

#### 4.聚合函数

>  只有一个返回值

- `AVG()` ：平均值；
- `COUNT()` ：计数，`COUNT(*)` ：返回被选行数；
- `MAX()` ：最大值
- `MIN()` ：最小值
- `SUM()` ：某列的总和；

#### 5.加密函数

- `MD5()` ：信息摘要算法；
- `PASSWORD()` ：

#### 6.日期时间函数

- `NOW()` ：当前日期和时间；
- `CURDATE()` ：当前日期；
- `CURTIME()` ：当前时间；
## 6.安全

### 1.权限管理

- 授权
  - `GRANT 权限 ON 数据库.表 TO user [IDENTIFIED BY 'password']`
  - 权限可以为:`ALL, SELECT, CREATE. ALTER, ....`
  - 数据库和表可以用`*`匹配所有
- 回收权限
  - `REVOKE priv_type ON databases.table FROM user;`
- 查看权限
  - `SHOW GRANTS FOR user;`

### 2.备份恢复

> 逻辑备份: 将数据包含在一种MySQL能够解析的格式中(SQL或格式文本)
>
> 物理备份: 直接复制原始文件, 通常简单高效, 但是也有文件大(包含索引信息), 文件系统格式限制等问题;

- 文件系统快照: 

## 7.维护和调优

### 1.查看配置和状态信息

>   系统变量: 配置MySQL服务器的运行环境, 可以通过**配置文件**, **启动选项**, 或运行时进行配置;
>
>   状态变量: 监控MySQL服务器的运行状态;

-   变量:
    -   **查看**: 系统变量: `show variables;` 或者`show variables like 'log%';`
        -   优先显示会话级别变量, 不存在则显示全局变量;
        -   可以使用`show global variables;`指定显示全局变量;
    -   **设置**: 通过`set [GLOBAL|SESSION] variable_name = value`;
        -   例如`SET GLOBAL sort_buffer_size=value; 或 SET @@global.sort_buffer_size=value;`
    -   重要变量:
        -   `max_connections`: 最大连接数;
        -   `auto_increment_increment`: 自增增量;
        -   `auto_increment_offset`: 起始自增点;
-   状态:
    -   查看状态变量: `show status`或者`show status like 'Threads%';`
    -   `show processlist`: 显示那些线程正在运行;

### 2.日志

> 错误日志: 记录MySQL服务端在运行时产生的错误信息, 
>
> 查询日志: 记录所有MySQL活动;
>
> 慢查询日志: 慢查询时间阈值, 以秒为单位, 超过这个阈值就是慢查询;
>
> 二进制日志: 记录更新过数据的所有语句, 可以用这个日志做增量备份;

- 日志配置:

    ```ini
    # 错误日志 #
    log_error=/exdata1/logs/mysql/mysqld.log
    # 日志等级, 可选1,error, 2,warn, 3, note
    log_error_verbosity=3
    
    # 查询日志 #
    # 是否开启
    general_log=ON
    general_log_file=/exdata1/logs/mysql/mysql-general.log
    
    # 慢查询日志 #
    slow_query_log=ON
    slow_query_log_file=/exdata1/logs/mysql/mysql-slow.log
    # 慢查询日志阈值, 单位s
    long_query_time=1
    # 捕获所有未使用索引的SQL
    log_queries_not_using_indexes=ON
    # 限制未索引查询数量, 0无限制
    log_throttle_queries_not_using_indexes=100
    # 捕获管理类的SQL,(修改表, 创建索引,...)
    log_slow_admin_statements=ON
    #min_examined_row_limit=100000
    二进制日志
    log-bin=/x/x/x/x
    ​```    
    ```
- 二进制日志查看: `mysqlbinlog filename.number`

### 3.EXPLAIN [参考](<https://www.cnblogs.com/xuanzhi201111/p/4175635.html>)

> 查看SQL语句的执行计划, 使用方式: 添加`EXPLAIN`到需要分析的语句前

- `EXPLAIN`出来的信息有10列，分别是:

  - `id`: SELECT 查询的标识符. 每个 SELECT 都会自动分配一个唯一的标识符.

  - `select_type`: SELECT 查询的类型.

    ```
    (1) SIMPLE(简单SELECT,不使用UNION或子查询等)
    (2) PRIMARY(查询中若包含任何复杂的子部分,最外层的select被标记为PRIMARY)
    (3) UNION(UNION中的第二个或后面的SELECT语句)
    (4) DEPENDENT UNION(UNION中的第二个或后面的SELECT语句，取决于外面的查询)
    (5) UNION RESULT(UNION的结果)
    (6) SUBQUERY(子查询中的第一个SELECT)
    (7) DEPENDENT SUBQUERY(子查询中的第一个SELECT，取决于外面的查询)
    (8) DERIVED(派生表的SELECT, FROM子句的子查询)
    (9) UNCACHEABLE SUBQUERY(一个子查询的结果不能被缓存，必须重新评估外链接的第一行)
    ```

  - `table` : 查询的是哪个表;

  - `partitions` : 匹配的分区

  - `type` : **比较重要**, 显示连接使用了何种类型, 从最差到最好依次为:

    -   **ALL**：遍历全表以找到匹配的行
    -   **index**: index类型只遍历索引树
    -   **range**:只检索给定范围的行，使用一个索引来选择行
    -   **ref**: 表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值
    -   **eq_ref**: 类似ref，区别就在使用的索引是唯一索引，对于每个索引键值，表中只有一条记录匹配，简单来说，就是多表连接中使用primary key或者 unique key作为关联条件
    -   **const**、system: 当MySQL对查询某部分进行优化，并转换为一个常量时，使用这些类型访问。如将主键置于where列表中，MySQL就能将该查询转换为一个常量,system是const类型的特例，当查询的表只有一行的情况下，使用system
    -   NULL: MySQL在优化过程中分解语句，执行时甚至不用访问表或索引，例如从一个索引列里选取最小值可以通过单独索引查找完成。
  
  - `possible_keys`: 此次查询中可能选用的索引;

  - `key` : 实际查询中确切使用到的索引.

  - `key_len`: 索引长度, 精度满足, 越短越好

  - `ref` : 哪些列或常量被用于查找索引列上的值

  - `rows` : 估算的找到所需的记录所需要读取的行数

  - `filtered` : 表示此查询条件所过滤的数据的百分比

  - `Extra`: 额外的信息

      - `Using filesort`: 需要额外的步骤来对返回行排序, 需要优化;
      - `Using temporary`: 使用了临时表, 需要优化;
      - `Select tables optimized away`: 通过索引一次性定位到数据行完成整个查询;

### 4.MySQL调优

#### 1.慢查询日志

-   通过配置开启慢查询日志;
-   通过`mysqldumpslow`工具, 分析慢查询日志, 找到具体需要优化的sql语句;
-   通过`EXPLAIN`语句, 分析具体执行计划, 优化sql语句;

#### 2.索引建立

-   在where从句, group by从句, order by从句, on从句中出现的列;
-   

#### 2.使用及表结构上的优化

- 使用`EXPLAIN`查看如何执行SELECT语句;
- 一般存储过程比单条执行快速;
- 不检索不需要的数据;
- 子查询需要建立临时表, 效率低, 连接查询不需要建立临时表, 可以用连接查询替代子查询;
- 表拆分: 当表数据量大时, 查询数据的速度会很慢; 对于某些字段使用频率很低的表, 可以进行拆分;
- 增加中间表: 减少联表查询;
- 增加冗余字段: 减少联表查询;

#### 2.配置优化

### 5.应用侧调优

- 使用缓存
- 

## 9.技巧

