## 1.服务端启动和配置

- `mysqld_safe --defaults-file=xxxx --datadir=xxx --pid-file=xxx`
    - `defaults-file`: 指定配置文件.
    - `datadir`: 指定数据存放路径

- `mysqld_save` 和 `mysqld`:

    - `mysqld_save`: 脚本文件, 负责启动`mysqld`并监控 mysql 的运行.
    - `mysqld`: 二进制文件, mysql 服务执行程序.

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

