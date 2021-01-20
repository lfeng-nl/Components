# Kubernetes

> Kubernetes项目要解决的问题: **运行在大规模集群中的各种任务之间，实际上存在着各种各样的关系, 这些关系的处理，才是作业编排和管理系统最困难的地方**
>
> Kubernetes提供了一个框架, 可以弹性的运行分布式系统, 它提供**服务发现和负载平衡**, **自动部署和回滚**, **自我修复**,**密钥和配置管理**.

## 1.整体架构

> 一个Kubernetes系统, 通常称之为Kubernetes集群. 由一个Master节点, 和若干Node节点组成.

<img src="./image/components-of-kubernetes.svg" alt="k8s" style="zoom: 80%;" />

![k8s](./image/k8s.jpg)

### 1.Master(Control Plane)

> 负责协调集群中的所有活动

- `kube-apiserver`: 提供整个系统对外的HTTP接口. 可以使用`kubectl`的封装.
- `kube-scheduler`: Pod调度, 决定Pod放在哪一个Node上运行.
    -  根据预选规则, 选出合适的主机.
    -  根据优选规则打分, 选择合适的Node.
- `controller-manager`: 一组控制器, `Node Controller`, `Replication Controller`, `Endpoints Controller`...
- `etcd`: 分布式存储, 负责保存集群的配置信息和资源的状态. 

### 2.Node

> 维护Pod, 使用API和Master通信, 指单台服务器(物理或者虚拟)

![node](./image/node.jpg)

- `kubelet`: 负责Pod的管理.
- `kube-proxy`: 维护节点上的网络规则, 负责Pod的负载均衡和服务发现(service的落地).
- `continue-runtime`: 容器运行时, 负责运行容器.
- Pod: 可以在Kubernetes中创建和管理的, 最小的可部署计算单元. 
    - 一组容器以及共享的资源(网络资源, 空间资源等), 容器间时相对紧密的耦合在一起的. 

## 2.概念

![概念](./image/概念.png)

### 1.Pod

- 多个关联的容器和一些共用资源. 就是Kubernetes世界的一个应用.

- 为什么需要Pod?
    - 有些任务需要一组进程共同完成, 进程间相互会直接发生文件交换, 使用`localhost`或本地`socket`通信, 会发生频繁的远程调用, 需要共享某些Namespace.
    - Pod是Kubernetes的原子调度单位.
    - Pod就是一组共享了某些资源的容器.
    - Pod中的容器, 通过`Infra`容器关联在一起. Pod的生命周期只和Infra容器一致.

### 2.Deployment

> 定义多副本应用(多副本Pod)的对象. ,用户负责描述Deployment中的目标状态(声明式更新). Deployment控制器实施更新, 使其变更为期望状态.
>
> Deployment还负责在Pod定义发生变化时, 对每个副本进行滚动更新.

- 例如, 下面的Deployment负责启动三个`nginx`Pods:

```yaml
apiVersion: apps/v1
kind: Deployment

# metadata: 对象的元数据
metadata:
  name: nginx-deployment
  # 通过 labels 过滤出它所关心的被控制对象. 会将所有携带"app:nginx" 标签的Pod识别为被管理对象. 
  labels:
    app: nginx
    
# spec: 存放对象特有的数据
spec:
  # replicas 副本数量
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

### 3.Ingress

> Ingress对集群中`service`的外部访问进行管理的API对象. 可以提供负载均衡

- 

- 例如一个最小的`Ingress`资源:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /testpath
        pathType: Prefix
        backend:
          service:
            name: test
            port:
              number: 80
```

### 4.Service

> 将一组Pod上应用程序公开为网络服务的抽象.

- **为什么需要`Service`?**
    - 每个Pod都有自己的IP地址, 但是Pod是**非永久性资源, 存在动态创建和销毁**. 那么, 一组Pod如何为其他的Pod提供持续服务? 其他Pod如何感知服务IP? 所以, 需要引入`Services`概念.
    - `service`可以对多个Pod进行包括, 负责负载均衡.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```



## 3.设计理念

- API设计原则: 
    - 1.声明式API(用户期望的系统应该是什么样子), 对于重复操作是稳定的.
    - 2.API 以业务基础, 操作意图出发, 设计API.

- 控制机设计原则:
    - 假定任何错误的可能并对错误进行处理.
    - 每个模块都可以在出错后自动恢复.
    - 每个模块都考虑服务降级(高级功能, 基本功能).
