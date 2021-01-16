# MySQL

## 1.MySQL 基础

![MySQL](./image/mysql.png)

### 1.字符编码

> 编码 encode: 将字符映射成一个二进制数据的过程.
>
> 解码 decode: 将一个二进制数据映射到一个字符的过程.

- 使用`show charset`查看支持的字符编码;
- 常用字符编码:
  - `utf8bm4`: 正宗`utf-8`编码,

### 2.数据类型

- 存储数据最小的数据类型通常更好, 但要确保没有低估需要存储的值的范围;
- 简单更好; 简单数据类型通常需要更少的 CPU 周期;
- 尽量避免 NULL, MySQL 难以优化包含 NULL 的列;

- 常用数据类型: `INT, FLOAT, DOUBLE, DATA, TIME, CHAR, VARCHAR, TEXT...`

  - `VARCHAR`: 可变长字符串, 适用于列的最大长度比平均长度大很多, 列的更新很少的数据; 频繁更新会导致碎片化;
  - `CHAR`: 定长, 对于经常变更的数据也不容易产生碎片; 存储空间上比`VARCHAR`更有效率;
  - `BLOB`: 存储的是二进制数据, 没有排序规则或字符集;
  - `TEXT`: 存储的是字符

- 数据库设计需要考虑的点:
  - 使用`tinyint`代替枚举. 枚举的排序效率低, 扩展性不强.
  - 货币类使用`int`或`decimal`, 避免使用`float`和`double`.
  - 时间类型: 更加项目自身需求选择, `varchar, timestamp, datetime`等.
  - 文件类型: 一般 mysql 中仅存储文件名和路径, 文件内存使用`HDFS(Hadoop分布式文件系统)`存储.

### 3.MySQL 帮助文档

- `? xxx;`: 查询`xxx`的命令说明.
  - 例如: `? CREATE DATABASE;`

## 2.库和表操作

### 1.数据库操作

- 创建: `CREATE DATABASE 数据库名;`

- 查看：`SHOW {DATABASES|SCHEMAS}`

- 修改：`ALTER {DATABASE|SCHEMAS} [数据库名] [DEFAULT] CHARACTER SET [=] charset_name;`

- 删除：`DROP {DATABASE|SCHEMA} [IF EXISTS] 数据库名;`

- 使用数据库：`USE 数据库名;`

  - `SELECT DATABASE();`: 当前使用数据库;
  - `SELECT NOW(), USER(), VERSION();`: 时间, 用户, 版本;

### 2.表定义操作

> 创建表时长用的约束:
>
> PRIMARY KEY: 唯一约束, NOT NULL 约束, 主键必须包含且唯一, 自动创建唯一索引;
>
> UNIQUE KEY: 唯一约束, 自动创建唯一索引;
>
> FOREIGN KEY: 规范数据引用完整性约束, 自动建立索引
>
> **以上三种 KEY, 都有约束和索引双层含义**

- 创建表：`CREATE TABLE 表名 (字段名1 类型 [修饰], 字段名2 类型, ..., [索引]) [表选项];` [参考](https://dev.mysql.com/doc/refman/5.7/en/create-table.html)

  - 修饰:

    - `NOT NULL`: 非空约束
    - `DEFAULT default_value`: 默认值
    - `AUTO_INCREMENT`: 自增(设置自增, 必须对该列设置索引)
    - `UNIQUE`: 唯一约束(自动创建索引)
    - `PRIMARY KEY`: 主键
    - `COMMENT '注释信息'`: 注释

  - 索引:
    - `PRIMARY KEY (列1, 列2)`: 主键, 默认添加唯一约束, 不能设置索引名称.
    - `KEY | INDEX 索引名 (列1, 列2)`: 普通索引.
    - `FULLTEXT KEY 索引名 (列1)`: 全文索引, 用于全文搜索特殊类型的索引.
    - `UNIQUE 索引名 (列1, 列2)`: 唯一索引.

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
    - 删除外键约束: `... DROP FOREIGN KEY 外键别名;`, 未指定外键别名会自动生成, 请查看建表信息`SHOW CREATE TABLE 表名`
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
  SELECT
    [DISTINCT]
    检索列1 [, 检索列2] ...
    [FROM 表
      [PARTITION partition_list]]
    [WHERE where_condition]
    [GROUP BY {col_name | expr | position}
      [ASC | DESC], ... [WITH ROLLUP]]
    [HAVING where_condition]
    [ORDER BY {col_name | expr | position}
      [ASC | DESC], ...]
    [LIMIT {[offset,] row_count | row_count OFFSET offset}]
    [FOR UPDATE | LOCK IN SHARE MODE]
  ```

- `DISTINCT`:

  - 返回结果删除重复行.

- `WHERE`: 条件过滤

  - 大小比较: `=, <, <=, >, >=, !=`
  - 集合`IN|NOT IN`: `... WHERE id IN (1, 5, 10) ;`
  - 范围`[NOT] BETWEEN AND`: `... WHERE id BETWEEN 1 and 10;`
  - 匹配字符`[NOT] LIKE`: `... WHERE name LIKE 'l%';`
    - `%`: 任意长度字符串, 长度可以为 0;
    - `_`: 匹配单个字符;
  - 空值`IS [NOT] NULL`
  - 多个条件`AND, OR`: `WHERE id=1 OR name='test';`

- `GROUP BY`：分组

  - SELECT 子句中的列必须为分组列或聚合函数.
  - `SELECT 字段2, max(字段1) from 表名 GROUP BY 字段2;`
  - 通过`HAVING`对分组后的数据进行过滤.
  - `... GROUP BY xxx HAVING xxxx`.

- `HAVING 和 WHERE`:

  - `HAVING`
    - 条件中可以使用函数`HAVING AGV(score) > 60`
    - 用于过滤分组后的数据.
  - `WHERE`
    - 分组前对数据进行过滤.

- `ORDER BY`:排序

  - `ACS`: 升序 默认.
  - `DESC`: 降序

- `LIMIT`: 限制返回数量

  - `... LIMIT 数量` : 仅返回指定数量的查询结果；
  - `... LIMIT 初始位置 数量` : 返回从指定位置开始的指定数量结果;

- 聚合(集合)函数：`COUNT(),SUM(),AVG(),MAX(),MIN();`

### 3.连接查询和子查询

#### 1.连接查询

> 连接查询: 将两个或两个以上的表按某个条件连接, 从中查询数据.
>
> 根据连接形式不同, 分为**内连接, 左外连接, 右外连接**.

- 连接：`SELECT * FROM 表1 [连接形式] 表2 ON 表1.字段1=表2.字段2 WHERE 条件;`

  - 一般用`ON`关键字来设定连接条件，用`WHERE`关键字进行结果及记录的过滤。

- 连接类型：内连接、左外连接、右外连接；

  - 内连接`JOIN`: 仅显示符合连接条件的记录，即交集部分；
  - 左外连接`LEFT JOIN`: 左表的记录将会全部表示出来，右表记录不足的地方均为 NULL.
  - 右外连接 `RIGHT JOIN`: 右表的记录将会全部表示出来，左表记录不足的地方均为 NULL.

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

> 出现在其他 SQL 语句(增删改查)内的`SELECT`子句，用小括号包围；
>
> 内层查询语句为外层语句提供过滤条件.
>
> **子查询 1.执行过程可能并不是由内向外执行. 2.存在临时表的创建和销毁. 子查询通常存在严重的效率问题.应尽量避免使用, 或使用`EXPLAIN`分析**

- 带`IN`关键字子查询:

  - `... WHERE 字段1 IN (SELECT 字段2 FROM 表名);`

- 带`EXISTS`关键字子查询:

  - 如果内层查询到结果, 返回为`true`, 反之为`yes`;

- 带比较运算符的子查询, `=, !=, >, >=, <, <=`:
  - `... WHERE 字段1 >= (SELECT 字段1 FROM 表名 WHERE 条件);`
  - 带`ANY`关键字子查询:
    - 只要满足内层查询语句返回结果中的任何一个;
    - `.... WHERE 字段1 >= ANY (SELECT 字段2 FROM 表名);`
  - 带`ALL`关键字子查询:
    - 需要满足内层查询的所有结果;
    - `... WHERE 字段1 >= ALL (SELECT 字段2 FROM 表名);`

### 4.合并查询结果

- `UNION`: 合并查询结果, 相同记录消除; `SELECT 语句1 UNION SELECT 语句2;`
- `UNION ALL`: 合并查询结果, 不消除相同记录; `SELECT 语句1 UNION ALL SELECT 语句2;`

## 4.特殊主题

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
  - 所有的触发器都存储在 information_schema.triggers 表中
- 删除:
  - `DROP TRIGGER 触发器名;`

### 3.存储过程

> 存储过程: 类似于脚本, 保存了多条 MySQL 语句的集合;

- 优缺点:

  - 优点: 效率高, 简化操作, 安全性好;
  - 缺点: 更新迭代麻烦, 不利于分库分表, 业务扩展后无法使用, 跟组件或 ORM 库无法兼容;

- 创建存储过程

  ```sql
  -- 修改定界符
  delimiter ;;
  
  -- 创建存储过程
  create procedure idata()
  begin
    declare i int;
    set i=1;
    while(i<=100000)do
      insert into t values(i, i, i);
      set i=i+1;
    end while;
  end;;
  
  -- 还原定界符
  delimiter ;
  
  -- 调用存储过程
  call idata();
  ```

- 调用存储过程: `CALL 存储过程名称;`

- 查看:

  - `SHOW PROCEDURE STATUS LIKE '存储过程名匹配';`
  - `SHOW CREATE PROCEDURE 存储过程名;`

- 删除

  - `DROP PROCEDURE 存储过程名;`

### 4.运算符和函数

> `SELECT DATABASE();`: 当前使用数据库;
>
> `SELECT NOW(), USER(), VERSION();`: 时间, 用户, 版本;

#### 1.字符函数

- `CONCAT()` :用于字符连接，可以连接多个字符串，`CONCAT('lfeng', 'hqh', 'xiaoxi');`
- `CONCTA_WS()` ：用指定分隔符(可以为字符串)连接，第一个参数为分隔符，`CONCAT_WS('---', 'lfeng', 'hou');`

#### 2.数值运算符与函数

- `CEIL()`：进一取整，小数位舍弃，整数+1,；
- `FLOOR()` ：舍一取整，小数位舍弃，
- `POWER()` ：幂运算，n 的 m 次方，`POWER(2,3);`
- `ROUND()` ：四舍五入小数位，`ROUND(2.125, 2); -->2.13` ，位数可以为负，表示整数位；
- `TRUNCATE()` ：数字截断，不做四舍五入；

#### 3.比较运算符与函数

- `[NOT] BETWEEN ... AND ...` ：在范围之内；
- `[NOT] IN` ：在不在其中；
- `IS [NOT] NULL` ： 是否为空；

#### 4.聚合函数

> 只有一个返回值

- `AVG()` ：平均值；
- `COUNT()` ：计数，
    - `COUNT(*)` ：返回被选行数；
    - `COUNT(*) num`: 设置别名;
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

### 5.特殊用法

- `@`: 使用用户变量:

    - ```mysql
        select max(id), min(id) into @M, @N from t;
        set @X = floor((@M-@N+1)*rand() + @N);
        select * from t where id>= @X limit 1;
        ```

- `@@`: 使用系统变量, 