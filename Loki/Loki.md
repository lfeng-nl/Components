# Loki

## 1.Loki是什么?

### 1.概述

- 日志聚合系统. 
- 仅索引日志标签, 不索引日志内容, 不提供分析, 报表. 大大减轻了存储成本.
- Loki-based logging stack:
  - promtail: 客户端, 负责收集日志并发送Loki.
  - Loki: 负责日志存储和处理查询.
  - grafan: 日志的查询和显示.

![Loki](https://aleiwu.com/img/loki/loki-arch.png)

### 2. Loki组件

Distributor: 接受来自客户端的日志写入请求, 无状态, 可扩展.

- 通过日志标签 和 tenant ID 哈希, 选择发送的Ingester.
- 通过gRPC和ingesters通信

Ingester: 接收`Distributor`下发的日志流.

- 负责将日志写入后端存储(DynamoDB, Amazon S3, Cassandra ... )
- 日志按时间戳(纳秒)进行排序.

Querier: 负责日志查询

### 3.客户端: Promtail

> 客户端负责收集日志并通过**loki API**推送日志信息给Loki, 支持: Promtail, Docker Driver, Fluentd, Logstash等

Promtail:

- Loki推荐的日志收集组件, 部署在需要收集日志的每台机器上.
- 主要功能: 发现目标, 给日志流绑定标签, 推送日志流到Loki

安装: `$ helm upgrade --install promtail grafana/promtail --set "loki.serviceName=loki"`

### 4.存储

日志存储分为两部分: 

- `index`: 存储日志流的标签集, 并链接到对应的`chunk`.
- `chunk`: 压缩的日志信息.

`index`支持的存储:

- Single Store(boltdb-shipper): 2.0版本推荐方式. 将`index`存储在`BoltDB`文件中, 并将文件同步到`chunk`使用的对象存储中.
- Amazon DynamoDB / Google BigTable: 云数据库
- [Apache Cassandra](https://cassandra.apache.org/): Nosql
- [BoltDB](https://github.com/boltdb/bolt): 简单, 快速, 可靠的key/value 存储, 不支持集群. 

`chunk`支持的存储:

- File System: 存储于本地目录, 非常简单. 
  - 如果需要集群部署, 需要网络存储, 性能较差.
  - 仅适用于要求低, 日志量不大的场景.

- Amazon DynamoDB / Google Bigtable: 云数据库
- Amazon S3 / Google Cloud Storage: 对象存储
- [Apache Cassandra](https://cassandra.apache.org/): 一个Nosql

## 2.怎么用?

### 1.安装

> [Install Loki with Helm](https://grafana.com/docs/loki/latest/installation/helm/)

- 添加Loki仓库

  ```bash
  helm repo add grafana https://grafana.github.io/helm-charts
  helm repo update
  ```

- 安装loki+promtail

  ```bash
  helm upgrade --install loki grafana/loki-stack
  ```

- 可选: 安装Grafana

  ```bash
  helm install loki-grafana grafana/grafana
  
  # 查看 admin 用户密码
  kubectl get secret --namespace <YOUR-NAMESPACE> loki-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
  ```

### 2.Loki配置

-  [storage_config](https://grafana.com/docs/loki/latest/configuration/#storage_config): 存储配置. 
- [schema_config](https://grafana.com/docs/loki/latest/configuration/#schema_config): 配置index, chunk使用的存储, 以及更新存储方式.

### 3.Promtail配置

- [clients](https://grafana.com/docs/loki/latest/clients/promtail/configuration/#clients): promtail链接的Loki信息.

- [scrape_configs](https://grafana.com/docs/loki/latest/clients/promtail/configuration/#scrape_configs): Promtail 如何收集日志

  - ```yaml
    scrape_configs:
    - job_name: local
      static_configs: ...
      file_sd_config: ...
      kubernetes_sd_config: ...
      relabel_configs: ...
    - job_name: kubernetes
      ...
    ```

#### 1.静态文件采集

```yaml
- job_name: log_file
  static_configs:
  - targets:
     - localhost
    labels:
      <labelname> : <labelvalue> # 给当前日志流增加的标签
      __path__: /data/test.log   # __path__ : 需要采集的日志文件名
```

#### 2.pod日志采集

> 大体流程: Promtail监控所在Node的所有Pod信息(kubernetes_sd_configs.role = pod时), 拼接对应的日志路径(需要挂载到promtail中, 默认挂载`/var/log/pods`, `/var/lib/docker`), 并根据配置文件, 打上对应标签(后续查询时使用).

```yaml
- job_name: kubernetes-pods-name
  pipeline_stages:
    - docker: {}
  kubernetes_sd_configs:
  - role: pod
  relabel_configs:
  # 增加 pod: {pod_name} 标签
  - action: replace
    source_labels:
    - __meta_kubernetes_pod_name
    target_label: pod
  # 增加 container: {container_name} 标签
  - action: replace
    source_labels:
    - __meta_kubernetes_pod_container_name
    target_label: container
  # 增加 __path__: /var/log/pods/{pod_uid}/{container_name}/*.log 标签
  # __path__: 采集的日志路径
  - replacement: /var/log/pods/*$1/*.log
    separator: /
    source_labels:
    - __meta_kubernetes_pod_uid
    - __meta_kubernetes_pod_container_name
    target_label: __path__
```

### 4.查询

1. 使用Grafana提供的前端页面.
2. 直接使用loki查询接口: 例如`/loki/api/v1/query_range`
   - `curl -G -s  "http://{loki}:3100/loki/api/v1/query_range" --data-urlencode 'query={pod="pod_name", container="container-1"}'`
   - [LogQL](https://grafana.com/docs/loki/latest/logql/)
   - [HTTP API](https://grafana.com/docs/loki/latest/api/)

参考:

[云原生下的日志新玩法: Grafana Loki 源码分析](https://aleiwu.com/post/grafana-loki/)

[Loki: Prometheus-inspired, open source logging for cloud natives](https://grafana.com/blog/2018/12/12/loki-prometheus-inspired-open-source-logging-for-cloud-natives/)

[Loki调研](http://wiki.baidu.com/pages/viewpage.action?pageId=972975329)

[Helm 部署 Loki 日志聚合](https://www.akiraka.net/kubernetes/849.html)

[Loki日志系统介绍](https://www.jianshu.com/p/77b9ce1c320e)

