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
- 修改数据表内容：`ALTER TABLE tb_name ...`

  - 添加：`... ADD [COLUNMS] col_name column_define [FIRST|AFTER col_name]`
  - 添加多列：`... ADD [COLUMNS](col_name column_define,...);`
  - 删除列：`... DROP [COLUMNS] col_name;`
  - `DROP`和`ADD`可以混用，用`,`隔开即可；
  - 添加主键约束：`... ADD [CONSTRAINT [symble]] PRIMARY KEY (col_name);`
  - 删除主键约束：`... DROP PRIMARY KEY;`
  - 添加唯一约束：`... ADD [CONSTRAINT [symble]] UNIQUE (col_name, col_name2);`
  - 删除唯一约束：`... DROP {INDEX|KEY} index_name;`
  - 添加外键约束：`... ADD [CONSTRAINT [symble]] FOREIGN KEY (col_name) REFERENCES tb_name(col_name)`
  - 修改默认约束：`... ALTER col_name {SET DEFAULT lit|DROP DEFAULT}`
  - 修改列定义（定义，位置）：`... MODIFY  col_name col_define [FIRST|AFTER col_namex];`**定义需要写上**
  - 修改列（名称，定义，位置）：`... CHANGE old_col_name new_col_name col_define [FIRST|AFTER col_name]`
  - 修改表的名称：`... RENAME [TO|AS] new_tab_name;` 或者 `RENAME tab_name TO new_tab_name;`
- 查看名为`tb_name`的数据表的详细结构：`SHOW COLUMNS FROM tb_name;`

### 3.表记录操作

- 向数据表中写入记录`INSERT` ：
  - `INSERT [INTO] tbl_name [(col_name)] {VALUES|VALUE}({expr|DEFAULT},...),(...);`
  - `INSERT [INTO] tbl_name SET col1_name={expr|DEFAULT},col2_name={expr|DEFAULT}，...;` 与第一种的区别：此种方式可以使用子查询； 
  - `INSERT [INTO] tbl_name [(col_name, ...)] SELECT ...;` 可将查询结果插入到指定数据表中；
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

- 记录的查找：`SELECT col1_name，col2_name... FROM tbl_name WHERE 限制;` 显示列将按请求顺序显示 ；
- 还可以对显示类名进行==别名==操作：`SELECT col_name AS new_col_name FROM tab_name;`
- `WHERE`后跟限制条件，提高查询精度；
  - 限制条件可以用比较符号，也可用`AND OR`连接多个限制： `age>18 AND age<35`
  - IN 和 NOT IN：`WHERE age NOT IN(26, 27);WHERE age IN(18);`
  - 通配符：关键词`LIKE`和通配符一起使用，`_` :匹配一位，`%` :不定长通配；例：`WHERE age LIKE ’2_‘`
- 查询结果分组`GRPUP BY`：`[GROUP BY {col_name|position} [HAVING where_condition], ...];` `HAVING `跟分组条件，即只对某一部分记录做分组；
- 查询结果排序`ORDER BY` ：默认升序(`ASC`)，降序(`DESC`)，例：`ORDER BY {col_name|position} [ASC|DESC] ，{col_name|positin} [ASC|DESC];` 可以设置多条规则，当前条满足后，对其中相等的再次排序；
- 限制查询结果返回的数量`LIMIT` ：
  - `LIMIT {[offset,] row_cout` 即从第`offset`条开始（0开始）返回`row_count`条结果； 
  -  `LIMIT row_count OFFSET offset}`  同上；
- 内置函数和计算：`COUNT(),SUM(),AVG(),MAX(),MIN();`

### 5.子查询和连接

- 子查询：例`SELECT age_avg FROM tb_name WHERE class IN(SELECT class FROM tb2_name WHERE name='Tom');` 查询名字为`Tom`所在`class`的 `age_avg`，但这两个字段不在同一张表中，可以用子查询；

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

### 

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
  | BIT       |         | 保存位字段的值，                                 |

- 时间类型：

  | 数据类型      | 描述                    |
  | --------- | --------------------- |
  | DATE      | ‘0000-00-00’          |
  | TIME      | ‘00:00:00’            |
  | DATETIME  | ‘0000-00-00 00:00:00' |
  | TIMESTAMP | '0000-00-00 00:00:00' |
  | YEAR      | 0000                  |

## 3.约束

- NOT NULL：非空约束，NULL值可以为空，NOT NULL值必须非空；
- PRIMARY KEY：主键约束，每张表中只允许一个主键，主键记录保证唯一，主键自动为NOT NULL；
- UNIQUE KEY：唯一约束，保证记录唯一，==可以为NULL==，可以存在多个唯一约束；
- DEFAULT：默认约束，如果插入记录时，没有明确为字段赋值，则自动赋予默认值；
- AUTO_INCREMENT：自增；
- FOREIGN KEY：外键约束，必须参考另一个表的主键，被外键约束的列，取值必须在它参考的列中有对应值；
  - 外键约束的参照：
- 表级约束和列级约束：对一个数据列建立的约束成为列级约束；对多个数据列建立的约束称为表级约束；

## 4.运算符和函数

### a.字符函数



