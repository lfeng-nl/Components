# Kubernetes集群搭建

## 1.工具选择

### 1.学习环境

- minikube: [参考](https://minikube.sigs.k8s.io/docs/start/)
    - 搭建本地Kubernetes.
    - `minikube start`
- kind: [参考](https://kind.sigs.k8s.io/)
    - 使用docke容器来运行本地Kubernetes集群的工具.
    - 安装好docker环境. 
    - `kind create cluster`

- kubeadm: 

### 2.生产环境

## 2.工具安装

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

# 将 SELinux 设置为 permissive 模式（相当于将其禁用）
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes

systemctl enable --now kubelet
```



## 3.搭建

> Kubernetes不推荐使用命令行的方式直接运行容器, 而是希望用`YAML`文件的方式, 即: 把容器定义, 参数, 配置 ,统统记录在一个YAML文件中, 通过统一的`kubectl apply -f 配置文件`开运行.

- `kubectl apply`: 配置文件是声明式的, kubernetes会自动变更, 实现声明的状态, 所以不需要明确是create还是update.
-  