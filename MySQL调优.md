# MySQL 调优

## 1.EXPLAIN [参考](https://www.cnblogs.com/xuanzhi201111/p/4175635.html)

> 查看 SQL 语句的执行计划, 使用方式: 添加`EXPLAIN`到需要分析的语句前

- `EXPLAIN`出来的信息有 10 列，分别是:

  - `id`: SELECT 查询的标识符. 每个 SELECT 都会自动分配一个唯一的标识符.

  - `select_type`: SELECT 查询的类型.

    - (1) `SIMPLE`(简单 SELECT,不使用 UNION 或子查询等)
    - (2) `PRIMARY`(查询中若包含任何复杂的子部分,最外层的 select 被标记为 PRIMARY)
    - (3) `UNION`(UNION 中的第二个或后面的 SELECT 语句)
    - (4) `DEPENDENT UNION(UNION` 中的第二个或后面的 SELECT 语句，取决于外面的查询)
    - (5) `UNION RESULT`(UNION 的结果)
    - (6) `SUBQUERY`(子查询中的第一个 SELECT)
    - (7) `DEPENDENT SUBQUERY`(子查询中的第一个 SELECT，取决于外面的查询)
    - (8) `DERIVED`(派生表的 SELECT, FROM 子句的子查询)
    - (9) `UNCACHEABLE SUBQUERY`(一个子查询的结果不能被缓存，必须重新评估外链接的第一行)

- `table` : 查询的是哪个表;

- `partitions` : 匹配的分区

- `type` : **比较重要**, 显示连接使用了何种类型, 从最差到最好依次为:

  - **ALL**：遍历全表以找到匹配的行
  - **index**: index 类型只遍历索引树
  - **range**:只检索给定范围的行，使用一个索引来选择行
  - **ref**: 表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值
  - **eq_ref**: 类似 ref，区别就在使用的索引是唯一索引，对于每个索引键值，表中只有一条记录匹配，简单来说，就是多表连接中使用 primary key 或者 unique key 作为关联条件
  - **const**、system: 当 MySQL 对查询某部分进行优化，并转换为一个常量时，使用这些类型访问。如将主键置于 where 列表中，MySQL 就能将该查询转换为一个常量,system 是 const 类型的特例，当查询的表只有一行的情况下，使用 system
  - NULL: MySQL 在优化过程中分解语句，执行时甚至不用访问表或索引，例如从一个索引列里选取最小值可以通过单独索引查找完成。

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

## 2.内部执行原理

### 1.排序



## 2.慢查询日志

- 通过配置开启慢查询日志;
- 慢查询相关配置:

- `slow_query_log`: 是否开启, `ON/OFF`;

- `slow_query_log_file`: 日志路径;

- `log_queries_not_using_indexes`: 记录无索引查询, `ON/OFF`;

- `long_query_time`: 慢查询时间阈值;
- 通过`mysqldumpslow`工具, 分析慢查询日志, 找到具体需要优化的 sql 语句;
- 通过`EXPLAIN`语句, 分析具体执行计划, 优化 sql 语句;

## 3.使用及表结构上的优化

- 使用`EXPLAIN`查看如何执行 SELECT 语句;
- 存储过程比单条执行快速, 可以将常用操作转换为存储过程;
- 不检索不需要的数据;
- **子查询需要建立临时表, 效率低, 连接查询不需要建立临时表, 可以用连接查询替代子查询**;
- 表拆分: 当表数据量大时, 查询数据的速度会很慢; 对于某些字段使用频率很低的表, 可以进行拆分;
- 减少链表查询:
  - 增加中间表
  - 增加冗余字段



