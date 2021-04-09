# Loki

## 是什么?

- 日志聚合系统. 
- 仅索引日志标签, 不索引日志内容, 不提供分析, 报表. 大大减轻了存储成本.
- Loki-based logging stack:
  - promtail: 客户端, 负责收集日志并发送Loki.
  - Loki: 负责日志存储和处理查询.
  - grafan: 日志的查询和显示.

![Loki](https://aleiwu.com/img/loki/loki-arch.png)

- 

### 组件

- Distributor: 接受来自客户端的日志写入请求, 无状态, 可扩展.
  - 通过日志标签 和 tenant ID 哈希, 选择发送的Ingester.
  - 通过gRPC和ingesters通信
- Ingester: 接收`Distributor`下发的日志流.
  - 负责将日志写入后端存储(DynamoDB, Amazon S3, Cassandra ... )
  - 日志按时间戳(纳秒)进行排序.
- Querier: 负责日志查询
- Chunk Store: 支持交互式查询和持续写入.

### 客户端

> 向Loki发送日志, 支持: Promtail, Docker Driver, Fluentd, Logstash

- Promtail:
  - 通过Pod 的元信息确定Pod的日志文件位置. 同时为日志(日志流)打上特定的`target label`. 通过`label`, 就可以快速查询一个或一组特定的`stream`.
  - 服务发现: 同Node, 通过`label`确定日志路径.

## 怎么用?

### 1.安装



## 原理?

参考:

[云原生下的日志新玩法: Grafana Loki 源码分析](https://aleiwu.com/post/grafana-loki/)

[Loki: Prometheus-inspired, open source logging for cloud natives](https://grafana.com/blog/2018/12/12/loki-prometheus-inspired-open-source-logging-for-cloud-natives/)

[promtail config](https://grafana.com/docs/loki/latest/clients/promtail/configuration/)

[Loki调研](http://wiki.baidu.com/pages/viewpage.action?pageId=972975329)

[Helm 部署 Loki 日志聚合](https://www.akiraka.net/kubernetes/849.html)

