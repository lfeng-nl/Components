# Docker

## 整体架构

![架构](./image/docker-engine.png)

- docker daemon: 实现镜像, 容器, 网络, 卷等模块,
- docker CLI:  通过RESTful API与docker daemon通信.
- registry: 镜像仓库.

## 核心组成

### 镜像 Image

> 从根本上解决了打包的难题

### 容器 Container

> 容器的本质是进程.

![container](./image/container.png)

### 网络 Network

> bridge, host, overlay

- bridge: ![bridge](./image/bridge_1.jpg)
- host: 和主机共享网络栈.
- overlay: 集群环境下使用.
    - 依靠`key-value`存储服务.
    - 集群中每台机器的hostname唯一.

### 数据卷 Volume

## Dockerfile

> 定制镜像, 

### 1.构建

- 构建上下文: 执行`docker build`时给定的路径. 
- `docker build [operation] path`
    - `-t name:tag`: 镜像名字和tag.
    - 

### 2.指令

> **1.exec格式指令, 需要使用双引号**
>
> **2.容器就是为了主进程存在, 主进程退出, 容器就会退出, 所以, 容器中的进程需要前台执行**

- `FROM`: 指定基础镜像.必备指令, 且是第一条指令.
- `RUN`: 执行命令(启动一个容器, 执行命令, 然后提交存储层文件变更).
    - *shell*格式: `RUN echo '<h1>Hello, Docker!<h1>' > /usr/share/nginx/html/index.html`
    - *exec*格式: `RUN ["可执行文件", "参数1", "参数2"]`
    - 多条`RUN`指令应串联执行, 减少镜像层级.

- `COPY`: 复制文件到镜像.
    - *shell*格式: `COPY [--chown=<user>:<group>] <原路径1> <原路径2> ... <目标路径>`
    - *exec*格式: `COPY [--chown=[user]:[group]] ["原路径1", "目标路径"]`

- `CMD`: 指定默认的容器主进程的启动命令.
    - *shell*格式: `CMD <命令>`
    - *exec*格式: `CMD ["可执行文件", "参数1", "参数2"]`
- `ENTRYPOINT`: 入口点, 和`CMD`目的一致, 但是需要通过`docker run --entrypoint`指定.
- `ENV`: 设置环境变量.
    - `ENV <key> <value>`
    - `ENV <key>=<value> <key2>=<value2>`
    - 定义的环境变量,在Dockerfile以及后续的容器中可以使用.
- `ARG`: 只可以在Dockerfile阶段使用的变量.
- `VOLUME`: 定义匿名卷
    - **容器运行时, 应该尽量保持容器存储层不发生写操作**. 为了防止运行时用户忘记将动态文件保持目录挂载为卷, 可以在dockerfile中事先指定某些目录为匿名卷.
    - `VOLUME ["路径1", "路径2"]`
    - `VOLUME <路径>`
- `EXPOSE`: 声明运行时容器提供服务的端口.
- `WORKDIR`: 指定工作目录. 如不存在则创建. 
- `USER`: 指定用户.
- `LABEL`: 添加一些元数据信息. 
    - `LABEL maintainer="lfengnl@163.com"`

