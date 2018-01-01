# MySQL

## 1.基本操作

- MySQL语句规范;
  - 关键字与函数名称全部大写；
  - 数据库名称、表名称、字段名称全部小写；
  - SQL语句必须以分号结尾；
  - 但实际上，SQL并不区分大小写，只是认为约定，方便区分；

- 数据库默认端口：3306；

- 创建数据库

  ```sql
  CREATE {DATABASE|SCHEMA} db_name [DEFAULT] CHARACTER SET [=] charset_name
  # [ ]内为可选项，{ }内为必选项；
  # CHARACTER SET:字符编码格式；例如：CHARACTER = utf8；
  # 
  ```

- 查看当前服务器下的数据库：

  ```sql
  SHOW {DATABASES|SCHEMAS} 
  ```

- 修改数据库：

  ```sql
  ALTER {DATABASE|SCHEMAS} [db_name] [DEFAULT] CHARACTER SET [=] charset_name;
  ```

- 删除数据库：

  ```sql
  DROP {DATABASE|SCHEMA} [IF EXISTS] db_name;
  ```

  ​

## 2.数据类型

- Text类型：

  | 数据类型       | 描述                                       |
  | ---------- | ---------------------------------------- |
  | CHAR(size) | 最多保存size个字符，默认 255；末尾空格去除；               |
  | VARCHAR    | 可变长度，保存时只保存需要的字符，另外加一个表示长度的数；            |
  | TEXT       | 字符大对象，有四种，TINY.., MEDIUM.., LONG..;      |
  | BLOB       | 二进制大对象，有TINY..MEDIUM..,LONG..四种；         |
  | ENUM       | 枚举类型，`ENUM('S', 'M', 'L', 'XL', 'XLL')` ； |
  | SET        | 可以有规定范围内的零个或多个值，规定范围由创建时给定；              |

- number类型：`UNSIGNED`后缀，==可以加`(size)`表示显示宽度，与实际能存放数据大小无关！==

  | 数据类型      | 存储      | 描述                                       |
  | --------- | ------- | ---------------------------------------- |
  | ==整数==    | ==---== | ==---==                                  |
  | TINYINT   | 1       | -128~127,0~255                           |
  | SMALLINT  | 2       | -32768～32767,0~65535                     |
  | MEDIUMINT | 3       | -8388608~8388607,0~1677215               |
  | INT       | 4       | -2147483648~2147483647,0~4294967295      |
  | BIGINT    | 8       |                                          |
  | ==定点数==   | ==---== | ==---==                                  |
  | DECIMAL   |         | DECIMAL(M,D),M总位数(小数位+整数位),D表示小数位；**不允许超出范围;** |
  | NUMERIC   |         | 在MySQL中，与DECIMAL视为同一类型；                  |
  | ==浮点数==   | ==---== | ==---==                                  |
  | FLOAT     | 4       | 用M(尾数)，B(基数)，E(指数)来表示：M×B^E;             |
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

## 3.数据表

数据表是数据库最重要的组成部分之一，是其他对象的基础。

- 打开某个数据库：`USE database_name;`
- 创建数据表：`CREATE TABLE table_name(colume_name data_type,...);`
- 查看数据表列表：`SHOW TABLES;`
- 查看名为`tb_name`的数据表的详细结构：`SHOW COLUMNS FROM tb_name;`
- 向数据表中写入记录：`INSERT [INTO] tbl_name [(col_name, ...)] VALUES(val,...);`
- 记录的查找：`SELECT expr, ... FROM tbl_name;`

## 属性

- NOT NULL：非空约束，NULL值可以为空，NOT NULL值必须非空；
- PRIMARY KEY：主键约束，每张表中只允许一个主键，主键记录保证唯一，组建自动为NOT NULL；
- UNIQUE KEY：唯一约束，保证记录唯一，==可以为NULL==，可以存在多个唯一约束；
- DEFAULT：默认约束，如果插入记录时，没有明确为字段赋值，则自动赋予默认值；
- FOREIGN KEY：外键约束，