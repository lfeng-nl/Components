# Ansible

>   Ansible是一个简单的自动化运维管理工具，基于Python语言实现，可用于自动化部署应用、配置、编排task(持续交付、无宕机更新等)。

## 1.安装及环境配置

- 主机要求：只要机器安装python2.6或python2.7，安装Ansible；需要安装`PIP`及相关python模块：

  - ```sh
    sudo pip install paramiko PyYAML Jinja2 httplib2 six
    ```

- 节点要求：托管节点上也需要安装 Python 2.4 或以上的版本.如果版本低于 Python 2.5 ,还需要额外安装一个模块：`python-simplejson`

### 1.主机安装Ansible

- 源码安装：

  - ```sh
    git clone git://github.com/ansible/ansible.git --recursive
    cd ./ansible
    source ./hacking/env-setup
    ```

- yum安装：

  - ```sh
    yum -y install epel-release
    yum -y install ansible
    ```

- pip安装：

  - ```sh
    sudo pip install ansible
    ```

### 2.建立远程连接

>ssh：SSH是Secure Shell的缩写。是目前较可靠，专为远程登录会话和其他网络服务提供安全性的协议。通过使用SSH，可以把所有传输的数据进行加密，而且能够防止DNS欺骗和IP欺骗。使用SSH，还可以将传输的数据压缩，所以可以加快传输的速度。SSH可以为FTP提供一个安全的“通道”。
>SSH保证安全的原因：1.远程主机收到用户的登录请求，把自己的公钥发给用户，2.用户使用公钥，将登录密码加密后，发送回来，3.远程主机用自己的私钥，解密登录密码，如果正确，同意登录。（中间人攻击）
>公钥登录，用户将自己的公钥存储在远程主机上，登录时，远程主机会向用户发送一段随机字符串，用户用自己的私钥加密后，在发回来，远程主机用事先存储的公钥进行解密，成功，就证明用户可信，如GitHub
>使用SSH协议进行FTP传输的协议叫SFTP(安全文件传输)

- 主机同远程节点建立连接需要实现以下几点：1.主机安装Ansible和依赖模块，2.节点安装满足要求的python版本；3.主机的SSH公钥发送到节点（SSH连接）；4.主机建立好节点设置文件（Inventory file），`/etc/ansible/hosts`;


- 主机生成SSH key并发送节点

    - ```shell
        # 生成ssh key,~/.shs/idrsa.pub -t 指定生成key的类型
        ssh-keygen -t rsa
        # 如果生成密钥的时候配置了密码，ansible每次都要密码，可通过以下方式记录密码：
        ssh-agent bash
        ssh-add ~/.ssh/id_rsa
        # 主机将公钥推送到节点，节点或自动保存到 ~/.ssh/authorized_keys 中
        ssh-copy-id -i ~/.ssh/id_rsa.pub root@172.16.80.181:22
        ```

- 配置主机Inventory file `/etc/ansible/hosts`，参考Inventory file章节；

- 配置Ansible；`/etc/ansible/ansible.cfg`，也可使用默认配置；

- 配置完成后可以用`ansible -m ping  'group_name'`测试连通性；

## 2.[Invertory File](http://www.ansible.com.cn/docs/intro_inventory.html)

>   Ansible 可同时操作一个组的多台主机，组和主机的关系通过`Invertory File`控制；默认路径`/etc/ansible/hosts`，文件格式和ini文件类似；

- 基本文件格式如下：

  - ```
    [group_name]
    host:port
    172.16.80.181:22
    172.16.80.182:22223
    ```

- 可以定义主机和组变量，用于后续的`playbooks`中使用；

  - 主机变量：

    ```
    [atlanta]
    host1 http_port=80 maxRequestsPerChild=808
    host2 http_port=303 maxRequestsPerChild=909
    ```

  - 组变量：

    ```
    [atlanta]
    host1
    host2

    // atlanta组的组变量
    [atlanta:vars]
    ntp_server=ntp.atlanta.example.com
    proxy=proxy.atlanta.example.com
    ```

- 组也可以是另一组的成员：

  - ```
    // 用于定义southeast组所包含的成员：atlanta raleight
    [southeast:children]
    atlanta
    raleigh
    ```

- 分文件存储主机和组变量：在 inventory 主文件中保存所有的变量并不是最佳的方式，还可以保存在独立的文件中，这些独立文件与 inventory 文件保持关联。不同于 inventory 文件(INI 格式)，这些独立文件的格式为 [`YAML`](http://www.ansible.com.cn/docs/YAMLSyntax.html)


## 3.YAML语法

>   YAML:是一种可读性高的用来表达资料序列的语言，其语法和其他高阶语言类似，并且可以简单表达清单、散列表、标量等数据结构。对于 Ansible, 每一个 YAML 文件都是从一个列表开始. 列表中的每一项都是一个键值对, 通常它们被称为一个 “哈希” 或 “字典”. 所以, 我们需要知道如何在 YAML 中编写==列表==和==字典==.

-   所有YAML文件以`---`开头，表明文件开始；

-   列表：所有成员都开始于相同的缩进级别，并且使用一个 `"- "` 作为开头(一个横杠和一个空格)；

-   字典：字典是由一个简单的 `键: 值` 的形式组成（这个冒号后面必须是一个空格）；

-   Ansible 使用 `“{{ var }}”`来引用变量， 如果一个值以 `{` 开头, YAML 将认为它是一个字典，所以必须==用引号把整行括起来== ：

    -   ```yaml
        foo: "{{ var }}"
        ```


##4.Playbooks

>   Ansible提供两种方式去完成任务,一是 ad-hoc 命令；一是写 Ansible playbook。前者可以解决一些简单的任务,
>   后者解决较复杂的任务；
>
>   ad-hoc命令：例如`ansible -m ping  'group_name'`
>
>   Ansible playbook：使用`ansible-playbook xxxx.yml`命令

### 1.基础

-   Playbooks 是 Ansible的配置，部署，编排语言。他们可以被描述为一个需要希望远程主机执行命令的方案，或者一组IT程序运行的命令集合。

-   例如：

    ```yaml
    ---
    # This playbook uses the ping module to test connectivity to hosts
    - name: Ping 
      hosts: all 

      tasks:
      - name: ping
        ping:
    ```

-   每个play可以指定：`name, hosts, remote_user, tasks, vars， handler`;

-   `name`：便于输出信息中识别；

-   `hosts`：指定主机，或主机组；

    -   ```yaml
        hosts: all
        ```

-   `remote_user`：执行命令的远程主机用户名；

    -   ```yaml
        remote_user: root
        ```

-   `tasks`：执行那些模块、命令；

    -   ```yaml
        tasks:
        	- name: ping
        	# 参考ansible 常用模块
        	  ping:
        ```

-   `vars`：定义变量；

    -   ```yaml
        vars:
        	keypair: mykeypair
        	instance_type: m1.small
        	security_group: default
        	image: emi-048B3A37
        ```

-   `handler`：Handlers 也是一些 task 的列表，通过名字来引用。Handlers 是由通知者进行 notify，如果没有被 notify，handlers 不会执行。不管有多少个通知者进行了 notify，等到 play 中的所有 task 执行完成之后，handlers  也只会被执行一次。Handlers 最佳的应用场景是用来重启服务,或者触发系统重启操作.除此以外很少用到了。

    -   ```yaml
        - name: Create Mysql configuration file
          template: src=my.cnf.j2 dest=/etc/my.cnf
          notify:
          # 通知名为“restart mysql”的 Handler
          - restart mysql
        ```

    -   ```yaml
        ---
        # Handler to handle DB tier notifications

        - name: restart mysql
          service: name=mysqld state=restarted
        ```

### 2.Include and Roles

-   例如用在任务列表中：

    -   ```yaml
        tasks:
          - include: tasks/foo.yml
        ```

-   导入其他的playbook：

    -   ```yaml
        - name: xxx
          host: xxx
          tasks:
          	- name: xxx
          	
        - include: xxx.yml
        - include: xxx.yml
        ```

-   roles：基于一个已知的文件结构，去自动的加载某些 `vars_files`，`tasks` 以及 `handlers`等；

-    `playbook `为一个角色`xxx`指定了如下的行为：

    -   如果 `roles/xxx/tasks/main.yml `存在, 其中列出的 `tasks` 将被添加到 play 中
    -   如果 `roles/xxx/handlers/main.yml `存在, 其中列出的 `handlers` 将被添加到 play 中
    -   如果 `roles/xxx/vars/main.yml `存在, 其中列出的 `variables` 将被添加到 play 中
    -   如果 `roles/x/meta/main.yml `存在, 其中列出的 “角色依赖” 将被添加到` roles `列表中 (1.3 and later)
    -   所有 `copy tasks` 可以引用 `roles/xxx/files/ `中的文件，不需要指明文件的路径。
    -   所有 `script tasks` 可以引用 `roles/xxx/files/ `中的脚本，不需要指明文件的路径。
    -   所有` template tasks` 可以引用 `roles/xxx/templates/` 中的文件，不需要指明文件的路径。
    -   所有 `include tasks` 可以引用` roles/xxx/tasks/ `中的文件，不需要指明文件的路径。

    >   还可以为`roles`的搜索设定 `roles_path` 配置项。使用这个配置项将所有的 common 角色 check out 到一个位置，以便在多个 playbook 项目中可方便的共享使用它们。

### 3.[Variables](http://www.ansible.com.cn/docs/playbooks_variables.html#id10)

-   变量的定义位置：

    -   `playbook`中，通过`vars`关键字直接定义：

        -   ```yaml
            - hosts: webservers
              vars:
                http_port: 80
            ```

    -   通过`roles`定义，`roles/xxx/vars/main.yml`

    -   通过`group_vars`定义，`gropu_vars/all、group_vars/xxx、...`

    -   通过`vars_files`关键字引入变量文件；

    -   `Invertory file`中定义：

-   通过facts获取变量：例如获取远程主机的IP地址、操作系统等信息；

    -   `ansible hostname -m setup` 可以查看有那些信息是可用的；
    -   例如`ansible_devices.sda.model= "WDC WD3200AAKS-7"`第一个硬盘的模型；

-   变量的另一个主要用途是在运行命令时，把命令结果存储到一个变量中。不同模块的执行结果是不同的，运行playbook时使用`-v`选项可以看到可能的结果值。在ansible执行任务的结果值可以保存在变量中,以便稍后使用它。

-   `Register Variable `：Ansible的==运行结果==可以存储在变量里面以便模版或条件语句使用，可以用Register注册变量。

### 4.顺序控制

-   when

    -   在playbooks 和 inventory中定义的变量都可以使用。下面一个例子,就是基于布尔值来决定一个任务是否被执行:

        ```yaml
        vars:
          epic: true
        ```

        一个条件选择执行也许看起来像这样:

        ```yaml
        tasks:
            - shell: echo "This certainly is epic!"
              when: epic
        ```

-   循环

    -   例如，`item` 会以此取`with_items`中定义的值；

        ```yaml
        name: add several users  
        user: name={{ item }} state=present groups=wheel  
        with_items:
        	- testuser1
            - testuser2
        ```

    -   嵌套循环

        ```yaml
        # 创建文件 file1_1, file1_2, file2_1, file2_2 
        name: create file
        file: 
        	path: {{ item[0] }} {{ itme[1] }}
        	state: touch
        	mode: 0755
        with_nested:
        	- ['file1', 'file2']
        	- ['_1', '_2']
        ```

## 5.模块

参考[Ansible常用模块](http://blog.csdn.net/pushiqiang/article/details/78249665)：

-   常用模块有：`ping,raw, yum, apt, pip, synchronize, template, copy, service , get_url, file, command , shell `等；
-   `script`模块：可以实现到对象节点上执行本机脚本。

## 6.实例

### 1.[Directory Layout](http://www.ansible.com.cn/docs/playbooks_best_practices.html#id11)

-   比较重要的文件有：
    -   `group_vars`：定义各组主机所使用变量；
    -   `site.yml `：master playbook；
    -   `roles`：角色目录，
        -   `common`：角色名
            -   `tasks`：
                -   `main.yml `：common的主要操作；
            -   `handlers `：
                -   `main.yml `：common的主要handler；
            -   ... ：通常还有`vars,files,templates ` ；
        -   `xxx`：其他角色，

