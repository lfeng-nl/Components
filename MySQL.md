# MySQL

## 1.基本操作

- MySQL语句规范;
  - 关键字与函数名称全部大写；
  - 数据库名称、表名称、字段名称全部小写；
  - SQL语句必须以分号结尾；
  - 但实际上，SQL并不区分大小写，只是认为约定，方便区分；
- 数据库默认端口：3306；

### 1.数据库操作

- 创建数据库

  ```sql
  CREATE {DATABASE|SCHEMA} db_name [DEFAULT] CHARACTER SET [=] charset_name
  # [ ]内为可选项，{ }内为必选项；
  # CHARACTER SET:字符编码格式；例如：CHARACTER = utf8；
  ```

- 查看当前服务器下的数据库：`SHOW {DATABASES|SCHEMAS} ` ；

- 修改数据库：`ALTER {DATABASE|SCHEMAS} [db_name] [DEFAULT] CHARACTER SET [=] charset_name;`

- 删除数据库：`DROP {DATABASE|SCHEMA} [IF EXISTS] db_name;`


- 打开数据库：`USE database_name;`

### 2.表定义操作

- 创建数据表：`CREATE TABLE table_name(colume_name data_type,...);`
- 查看表列表：`SHOW TABLES;`
- 查看名为`tb_name`的数据表的详细结构：`SHOW COLUMNS FROM tb_name;` 或者 `DESCRIBE tab_name;`
- 修改数据表内容：`ALTER TABLE tb_name ...`

  - 添加：`... ADD [COLUNMS] col_name column_define [FIRST|AFTER col_name]`
  - 添加多列：`... ADD [COLUMNS](col_name column_define,...);`
  - 删除列：`... DROP [COLUMNS] col_name;`
  - `DROP`和`ADD`可以混用，用`,`隔开即可；
  - 添加主键约束：`... ADD [CONSTRAINT [symble]] PRIMARY KEY (col_name);`
  - 删除主键约束：`... DROP PRIMARY KEY;`
  - 添加唯一约束：`... ADD [CONSTRAINT [symble]] UNIQUE (col_name, col_name2);`
  - 删除唯一约束：`... DROP {INDEX|KEY} index_name;`
  - 添加外键约束：`... ADD [CONSTRAINT [symble]] FOREIGN KEY (col_name) REFERENCES tb_name(col_name);`
  - 修改默认约束：`... ALTER col_name {SET DEFAULT lit|DROP DEFAULT};`
  - 添加非空约束：`... MODIFY col_name col_define NOT NULL;`
  - 删除非空约束：`... MODIFY col_name col_define NULL` 注意:==列定义是否需要修改==
  - 修改列定义：`... MODIFY  col_name col_define [FIRST|AFTER col_namex];`**定义需要写上**，可以修改定义、位置
  - 修改列（名称，定义，位置）：`... CHANGE old_col_name new_col_name col_define [FIRST|AFTER col_name]`
  - ==`MODIFY` 和 `CHANGE` 的区别在于，`CHANGE` 允许修改列名称；==
  - 修改表的名称：`... RENAME [TO|AS] new_tab_name;` 

### 3.表记录操作

- 向数据表中写入记录`INSERT` ：
  - `INSERT [INTO] tbl_name [(col_name)] {VALUES|VALUE}({expr|DEFAULT},...),(...);`
  - `INSERT [INTO] tbl_name SET col1_name={expr|DEFAULT},col2_name={expr|DEFAULT}，...;` 与第一种的区别：此种方式可以使用子查询； 
  - `INSERT [INTO] tbl_name [(col_name, ...)] SELECT ...;` 可将查询结果插入到指定数据表中；
- 从文件中加载数据`LOAD DATA INFILE`：
  - `LOAT DATA INFILE '文件路径' INTO TABLE tab_name [LINES TERMINATED BY '\r\n'];`
- 更新记录`UPDATE` ：
  - `UPDATE [LOW_PRIORITY] [IGNORE] table_reference SET col_name1={expr1|DEFAULT},...[WHERE where_condition]`
- 删除记录`DELETE` ：
  - `DELETE FROM tbl_name [WHERE where_condition];` 

### 4.表查找操作

> 查询表达式：每个表达式表示想查找的一列，必须有至少一个；多列之间以英文逗号分隔；

```sql
SELECT select_expr [,select_expr ...]
[
  FROM table_references
  [WHERE where_condition]
  [GROUP BY {col_name|position}]
  [HAVING where_condition]
  [ORDER BY {col_name|expr|position} [ASC|DESC],...]
  [LIMIT {offset, row_count} | {row_count OFFSET offset}]
]
```

- 记录的查找：`SELECT col1_name，col2_name... FROM tbl_name WHERE 限制;` 显示列将按请求顺序显示 ，可以同时查询多张表的内容；
- 还可以对显示类名进行==别名==操作：`SELECT col_name AS new_col_name FROM tab_name;`
- 把一列中相同的项合并：`SELECT DISTINCT col_name FROM tab_name;` 可以用`GROUP BY`实现；
- `UNION [ALL]` : 将两个查询结果合并为一个，`UNION` 会合并相同项，`UNION ALL` 全部显示，速度要快很多；
- `WHERE`后跟限制条件，提高查询精度；
  - 限制条件可以用比较符号，也可用`AND OR`连接多个限制： `age>18 AND age<35`
  - `IN` 和 `NOT IN`：`WHERE age NOT IN(26, 27);  WHERE age IN(18);`
  - `IS NULL` 和 `IS NOT NULL` :
  - 模式匹配：关键词`LIKE`和通配符一起使用，==`_` :匹配一位，`%` :不定长通配==；例：`WHERE age LIKE ’2_‘`
  - 正则表达式：利用关键词`REGEXP ...` , 
- 查询结果分组`GROUP BY`：`[GROUP BY {col_name|position} [HAVING where_condition], ...];` `HAVING `跟分组条件，即只对某一部分记录做分组；
- 查询结果排序`ORDER BY` ：默认升序(`ASC`)，降序(`DESC`)，例：`ORDER BY {col_name|position} [ASC|DESC] ，{col_name|positin} [ASC|DESC];` 可以设置多条规则，当前条满足后，对其中相等的再次排序；
- 限制查询结果返回的数量`LIMIT` ：
  - `LIMIT {[offset,] row_cout` 即从第`offset`条开始（0开始）返回`row_count`条结果； 
  - `LIMIT row_count OFFSET offset}`  同上；
- 内置函数和计算：`COUNT(),SUM(),AVG(),MAX(),MIN();`

### 5.子查询和连接

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

> 连接：在SELECT语句、多表更新、多表删除语句中支持`JOIN`操作：

- 语法结构：`A表 连接类型 B表 ON 连接条件` ：`table_reference1 {INNER JOIN| | LEFT JOIN | RIGHT JOIN} table_reference2 ON conditional_expr;` 一般用`ON`关键字来设定连接条件，用`WHERE`关键字进行结果及记录的过滤。
- 连接类型：内连接、左外连接、右外连接；
  - 内连接`INNER JOIN`: 仅显示符合连接条件的记录，即交集部分；
  - 左外连接`LEFT JOIN`:显示左表的全部记录及右表符合连接记录条件的记录；
  - 右外连接 `RIGHT JOIN`:显示右表的全部记录及左表符合连接记录条件的记录；


- 连接查询：在处理多个表时，子查询只能查询显示同一个表中的信息。如果需要多个表中信息，则需要连接（join）操作，基本思想就是把两个表当做一个新的表来操作；例如：

  ```sql
  SELECT id,name,people_num 
  FROM emplyee,department 
  WHERE emplyee.in_dpt=department.dpt_name;
   
  #等同于
  SELECT id,name,people_num 
  FROM emplyee JOIN department 
  ON emplyee.in_dpt=department.dpt_name;
  ```

## 2.数据类型

- Text类型：

  | 数据类型          | 描述                                       |
  | ------------- | ---------------------------------------- |
  | CHAR(size)    | 最多保存size个字符，默认 255；末尾空格去除；               |
  | VARCHAR(size) | 可变长度，size为最大允许的长度，保存时**只保存需要的字符**；       |
  | TEXT          | 字符大对象，有四种，TINY.., MEDIUM.., LONG..;      |
  | BLOB          | 二进制大对象，有TINY..MEDIUM..,LONG..四种；         |
  | ENUM          | 枚举类型，`ENUM('S', 'M', 'L', 'XL', 'XLL')` ； |
  | SET           | 可以有规定范围内的零个或多个值，规定范围由创建时给定；例如`name SET('f','s');` 则可赋值为`name='f',name='s',name='f,s'`等， |

- number类型：`UNSIGNED`后缀，==可以加`(size)`表示显示宽度，与实际能存放数据大小无关！==

  | 数据类型      | 存储      | 描述                                       |
  | --------- | ------- | ---------------------------------------- |
  | ==整数==    | ==---== | ==---==                                  |
  | TINYINT   | 1       | `-128~127,0~255`                         |
  | SMALLINT  | 2       | `-32768～32767,0~65535`                   |
  | MEDIUMINT | 3       | `-8388608~8388607,0~1677215`             |
  | INT       | 4       | `-2147483648~2147483647,0~4294967295`    |
  | BIGINT    | 8       |                                          |
  | ==定点数==   | ==---== | ==---==                                  |
  | DECIMAL   |         | `DECIMAL(M,D)` ；M总位数(小数+整数)；D表示小数位；**不允许超出范围;** |
  | NUMERIC   |         | 在MySQL中，与DECIMAL视为同一类型；                  |
  | ==浮点数==   | ==---== | ==---==                                  |
  | FLOAT     | 4       | `FLOAT(M,D)` ;显示宽度，M总位数，D小数位数；实际值与存储值可能不全相同 |
  | DOUBLE    | 8       |                                          |
  | ==BIT==   | ==---== | ==---==                                  |
  | BIT       |         | 保存位字段的值，SET b = b'01110111'              |

- 时间类型：

  | 数据类型      | 描述                    |
  | --------- | --------------------- |
  | DATE      | ‘0000-00-00’          |
  | TIME      | ‘00:00:00’            |
  | DATETIME  | ‘0000-00-00 00:00:00' |
  | TIMESTAMP | '0000-00-00 00:00:00' |
  | YEAR      | 0000                  |


- 注释方法：
  - 以`#` 字符开始到行尾；
  - 以`/*   */` 注释一段；

## 3.约束

约束是一种限制，它通过对表的行为或列的数据做出限制，来确保数据的完整性，唯一性。

| 约束类型 | 主键          | 默认值     | 唯一         | 外键          | 非空       | 检查    |
| ---- | ----------- | ------- | ---------- | ----------- | -------- | ----- |
| 关键字  | PRIMARY KEY | DEFAULT | UNIQUE KEY | FOREIGN KEY | NOT NULL | CHECK |

- NOT NULL：非空约束，NULL值可以为空，NOT NULL值必须非空；

- PRIMARY KEY：主键约束，每张表中只允许一个主键，主键记录保证唯一，主键自动为NOT NULL；

  - 还有一种特殊的主键--复合主键，主键不仅可以是表中一列，也可以是表中的两列或多列共同标示：

    ```sql
    CONSTRAINT prikey_name PRIMARY KEY(col1_name,col2_name)
    ```

- UNIQUE KEY：唯一约束，保证记录唯一，==数据可以为NULL==，可以存在多个唯一约束；

- DEFAULT：默认约束，如果插入记录时，没有明确为字段赋值，则自动赋予默认值；

- FOREIGN KEY：外键约束，必须参考另一个表的主键，被外键约束的列，取值必须在它参考的列中有对应值；
  ```sql
  CONSTRANT forkey_name FOREIGN KEY(col_name) REFERENCES tab_name(col1_name);
  ```

- 表级约束和列级约束：对一个数据列建立的约束成为列级约束；对多个数据列建立的约束称为表级约束；

- AUTO_INCREMENT：自增，指定了`AUTO_INCREMENT` 的列必须建立索引；指定了`AUTO_INCREMENT` 的列，在插入时自动生成编号，从1开始递增；

## 4.索引index

索引是用来快速地寻找那些具有特定值的记录，主要是为了检索的方便，是为了加快访问速度，按一定的规则创建的；MySQL提供多种索引：

- 查看索引信息：`SHOW {INDEX|KEYS} FORM tab_name;`
- 对某个表的某列建立索引：
  - `ALTER TABLE tab_name ADD INDEX index_name(col_name);` 或者
  - `CREATE INDEX index_name ON tab_name(col_name);`


- 普通索引：
- 唯一索引：
- 主键索引：
- 全文索引：
- 单列索引和多列索引
- 最左前缀：
- ​

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
- `COUNT()` ：计数；
- `MAX()` 
- `MIN()`
- `SUM()`

### 5.加密函数

- `MD5()` ：信息摘要算法；
- `PASSWORD()` ：

### 6.日期时间函数

- `NOW()` ：当前日期和时间；
- `CURDATE()` ：当前日期；
- `CURTIME()` ：当前时间；

## 6.自定义变量、函数和存储过程

- 自定义变量：
  - 局部变量用一个@标识，全局变量用@@；
  - 申明局部变量的语法：`DECLEAR var_name var_type`
  - 变量赋值：`SET var_name=value` ;

存储过程是SQL语句和控制语句的编译集合，以一个名称存储，并作为一个单元处理；

- `CREATE FUNCTION f1(p1 INT, p2 INT) RETURNS VARCHAR(20) RETURN ...`
- `DELIMITER`
- 复合结构体：`BEGIN ... NED`

## 7.存储引擎

存储引擎就是存储数据、查询数据的技术；

- 引擎的选用：`CREATE TABLE ... () ENGINE=engine_name`


- 并发控制：当多个连接对记录进行修改时，保证数据的一致性和完整性；
- 锁：共享锁、排他锁；也叫读锁，写锁；
- 锁颗粒：表锁，列锁；
- 事务：保证数据库的完整性；比如一个操作包含许多步骤，中间任意环节出错都应该使数据恢复至最原始的状态；
- 事务的特性：ACID，原子性，一致性，隔离性，持久性；
- 外键：保证数据一致性的策略
- 索引：对数据表中一列或多列的值进行排序的一种结构，使用索引可以快速访问数据表中的特定信息；
  - 普通索引
  - 唯一索引
  - 全文索引

## 8.优化

- SQL及索引优化：

