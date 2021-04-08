# Pod

## 1.pod的生命周期

> Pod是一个临时性的实体, Pod会被创建, 赋予一个唯一性的ID(UID), 并被调度到节点.

### 1.Pod状态

- `Pending`: Pod已经被Kubernetes系统接受, 但有一个或者多个容器尚未创建亦或者未运行.
- `Running`: Pod已经绑定到某个节点, Pod中的所有容器都已经被创建.至少有一个容器仍在运行.
- `Success`: Pod中的所有容器都已经成功终止, 并不会在重启.
- `Failed`: Pod中的容器都已经终止, 并且至少有一个容器因为失败终止.
- `Unknown`: 因为某些原因, 无法获取Pod的状态. 通常是与Pod所在主机通信失败.

### 2.容器状态

- `Waiting`: 仍在运行完成启动所需的操作.例如拉取镜像.
- `Running`: 
- `Terminated`: 容器已经结束(正常/异常)

### 3.Probe

> 由kubelet对容器执行定期诊断.

- `livenessProbe`: 探测容器是否正在运行.
- `readinessProbe`: 容器是否准备就绪.
- `startupProbe`: 容器中的应用是否已经启动. 和其他所有探针互斥.

## 2.Init容器

> Init容器会按照顺序逐个运行, 每个Init容器须运行成功, 下一个才能运行. 
>
> `spec.initContainers`