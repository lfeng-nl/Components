## 1.服务端启动和配置

- `mysqld_safe --defaults-file=xxxx --datadir=xxx --pid-file=xxx`
    - `defaults-file`: 指定配置文件.
    - `datadir`: 指定数据存放路径

- `mysqld_save` 和 `mysqld`:

    - `mysqld_save`: 脚本文件, 负责启动`mysqld`并监控 MySQL的运行.
    - `mysqld`: 二进制文件, MySQL服务执行程序.

- 系统变量: 影响服务运行的一系列变量, 由默认值和配置文件决定.

    - 系统变量信息可以通过:`SHOW [GLOBAL|SESSION] VARIABLES LIKE 'default_storage_engine'` 查询.
    - **对于大部分系统变量来说，它们的值可以在服务器程序运行过程中进行动态修改而无需停止并重启服务器**
    - 系统变量具有作用域:
        - `GLOBAL`: 全局变量, 影响服务器的整体操作.
        - `SESSION`: 会话变量, 影响客户端的连接.
    - 设置系统变量: `SET [GLOBAL|SESSION] 系统变量名=值`.

- 状态变量: 记录服务器运行状态.
    - 状态变量也有`GLOBAL, SESSION`两个作用域.
    - 查看: `SHOW [GLOBAL|SESSION] STATUS [LIKE 匹配的模式];`

## 2.常用配置

### 1.运行配置

- `interactive_timeout`: 交互式连接超时.
- `wait_timeout`: 非交互式连接超时.

### 2.日志配置

> 错误日志: 记录 MySQL 服务端在运行时产生的错误信息,
>
> 查询日志: 记录所有 MySQL 活动;
>
> 慢查询日志: 慢查询时间阈值, 以秒为单位, 超过这个阈值就是慢查询;
>
> 二进制日志: 记录更新过数据的所有语句, 可以用这个日志做增量备份;

- 日志配置:

    ````ini
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
    ````

- 二进制日志查看: `mysqlbinlog filename.number`

## 3.权限管理

- 授权
    - `GRANT 权限 ON 数据库.表 TO user [IDENTIFIED BY 'password']`
    - 权限可以为:`ALL, SELECT, CREATE. ALTER, ....`
    - 数据库和表可以用`*`匹配所有
- 回收权限
    - `REVOKE priv_type ON databases.table FROM user;`
- 查看权限
    - `SHOW GRANTS FOR user;`

## 4.备份恢复

> 逻辑备份: 将数据包含在一种 MySQL 能够解析的格式中(SQL 或格式文本)
>
> 物理备份: 直接复制原始文件, 通常简单高效, 但是也有文件大(包含索引信息), 文件系统格式限制等问题;

- 文件系统快照:

## 5.查看配置和状态信息

> 系统变量: 配置 MySQL 服务器的运行环境, 可以通过**配置文件**, **启动选项**, 或运行时进行配置;
>
> 状态变量: 监控 MySQL 服务器的运行状态;

- 变量:
    - **查看**: 系统变量: `show variables;` 或者`show variables like 'log%';`
        - 优先显示会话级别变量, 不存在则显示全局变量;
        - 可以使用`show global variables;`指定显示全局变量;
    - **设置**: 通过`set [GLOBAL|SESSION] variable_name = value`;
        - 例如`SET GLOBAL sort_buffer_size=value; 或 SET @@global.sort_buffer_size=value;`
    - 重要变量:
        - `max_connections`: 最大连接数;
        - `auto_increment_increment`: 自增增量;
        - `auto_increment_offset`: 起始自增点;
- 状态:
    - 查看状态变量: `show status`或者`show status like 'Threads%';`
    - `show processlist`: 显示那些线程正在运行;

