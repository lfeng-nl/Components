# Kubernetes集群搭建

## 1.工具搭建

- minikube: [参考](https://minikube.sigs.k8s.io/docs/start/)
    - 搭建本地Kubernetes.
    - `minikube start`
- KIND: [参考](https://kind.sigs.k8s.io/)
    - 使用docke容器来运行本地Kubernetes集群的工具.
    - 安装好docker环境. 
    - `kind create cluster`
- kubeadm: 
    - 可用于生产环境搭建.
    - 

## 2.所需组件

- **etcd(主节点)**: 数据存储和持久化, 需要高可用.
- **kube-apiserver(主节点)**: 管理集群的Rest API接口, 模块和模块间的交互和通信枢纽.
- **kube-controller-manager(主节点)**:  包括`Node Controller`, `Deployment Controller`等.
- **kube-scheduler(主节点)**: 分配调度Pod到集群内的节点上.
- **kubelet(所有节点)**: 每个节点都运行一个`kubelet`服务进程. 默认监听`10250`端口. 接收并执行`master`发来的指令.
- **kube-proxy(所有节点)**: 通过`iptables`为服务配置负载均衡.
- **kube-dns(所有节点)**: 为集群增加dns功能.

## 3.工具安装

### kubectl kubeadm kubelet安装

允许 iptables 检查桥接流量:

```shell
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system
```

禁用SELinux

```shell
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
```

添加源

```shell
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
       http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
```

安装 kubectl, kubeadm, kubectl

```shell
yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes

systemctl enable --now kubelet
```

## 4.kubeadm搭建

**1.禁用 swap**

```shell
swapoff -a
```

**2.检查`product_uuid`和mac地址, 确保每台机器唯一**

```shell
cat /sys/class/dmi/id/product_uuid
ip a
```

**3.安装Docker.**

**4.安装kubeadm, kubelet, kubectl**

**5.初始化集群**

- `kubeadm init`

- `kubeadm config images list`: 可以查看需要拉取的镜像

    - ```
        k8s.gcr.io/kube-apiserver:v1.19.7
        k8s.gcr.io/kube-controller-manager:v1.19.7
        k8s.gcr.io/kube-scheduler:v1.19.7
        k8s.gcr.io/kube-proxy:v1.19.7
        k8s.gcr.io/pause:3.2
        k8s.gcr.io/etcd:3.4.13-0
        k8s.gcr.io/coredns:1.7.0
        ```

- 镜像无法下载的解决方案:
    - 修改tag满足镜像[csdn](https://blog.csdn.net/zhongbeida_xue/article/details/104615259)

    - 使用kubeadm配置文件, 通过在配置文件中指定docker仓库[csdn](https://blog.csdn.net/zhongbeida_xue/article/details/104615259)
        - `kubeadm config print init-defaults > kubeadm.yaml`: 导出配置文件.
        - 修改`imageRepository: k8s.gcr.io` --> `imageRepository: registry.aliyuncs.com/google_containers`
        - `kubeadm config images pull --config kubeadm.yaml`: 下载镜像.
        - `kubeadm init --config kubeadm.yaml`: 
    - `kubeadm init --image-repository registry.aliyuncs.com/google_containers`

**6.配置kubectl**

  `mkdir -p $HOME/.kube`
  `sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config`
  `sudo chown $(id -u):$(id -g) $HOME/.kube/config`

root用户, 可以直接使用: 

  `export KUBECONFIG=/etc/kubernetes/admin.conf`

## 4.证书

### 1.证书生成

### 2.配置更新

