#### 0、介绍

[官方Git]: https://github.com/vmware/harbor/blob/master/docs/user_guide.md

简单的说，Harbor 是一个企业级的 Docker Registry，可以实现 images 的私有存储和日志统计权限控制等功能，并支持创建多项目(Harbor 提出的概念)，基于官方 Registry V2 实现。 

简单而言，就是一个贼酷炫的Docker Registry。

参考链接：

> https://mritd.me/2016/06/27/Harbor-%E4%BC%81%E4%B8%9A%E7%BA%A7-Docker-Registry-%E5%88%9D%E8%AF%95/

安装步骤归结为以下内容

1. 下载安装程序;
2. 配置**harbor.cfg** ;
3. 运行**install.sh**安装并启动Harbor;

#### 1、下载

> https://github.com/vmware/harbor/blob/master/docs/installation_guide.md

依照官方的安装页面细节，下载离线安装文件。

本例使用的是：

harbor-offline-installer-v1.5.1.tgz     md5:1f3a1cde8f6ad21602d0c87dba3325c5 

#### 2、配置

## 必须修改的参数：

- **hostname**：目标主机的主机名，用于访问UI和注册表服务。它应该是目标计算机的IP地址或完全限定的域名（FQDN），例如，`192.168.1.10`或`reg.yourdomain.com`。*不要使用localhost或127.0.0.1作为主机名 - 外部客户端需要访问注册表服务！*

### 其他重要参数：

- **db_password**：用于**db_auth**的MySQL数据库的root密码。*更改此密码以用于任何生产用途！*
- **max_job_workers** :(默认值为50）作业服务中的最大复制工作数。对于每个映像复制作业，工作程序将存储库的所有标记同步到远程目标。增加此数量可以在系统中实现更多并发复制作业。但是，由于每个工作者都消耗一定量的网络/ CPU / IO资源，请根据主机的硬件资源仔细选择该属性的值。
- **log_rotate_count**：日志文件在被删除之前会被轮换**log_rotate_count**次。如果count为0，则删除旧版本而不是旋转。
- **log_rotate_size**：仅当日志文件大于**log_rotate_size**字节时才会轮换日志文件。如果大小后跟k，则假定大小以千字节为单位。如果使用M，则大小以兆字节为单位，如果使用G，则大小为千兆字节。尺寸100，尺寸100k，尺寸100M和尺寸100G都是有效的。

### 可选功能（怎么搞自己看官方doc喽）：

- **电子邮件设置**：Harbor需要这些参数才能向用户发送“密码重置”电子邮件，并且仅在需要该功能时才需要。 

-  **harbor_admin_password**：管理员的初始密码。此密码仅在Harbor首次启动时生效。之后，将忽略此设置，并且应在UI中设置管理员密码。*请注意，默认用户名/密码为\**admin / Harbor12345**。* （反正可以网页设置，无所谓啦）

#### 3、安装

配置完配置文件以后，在解压目录，运行

```
./install.sh 
```

运行完以后，如果一切正常，可以用浏览器访问：**hostname**中的地址进行访问。

例如：http://192.168.245.134

### **注意：**

Harbor的默认安装使用*HTTP* - 因此，您需要将该选项添加`--insecure-registry`到客户端的Docker守护程序并重新启动Docker服务。 

即：在/etc/docker/daemon.json 下"insecure-registries":中添加**hostname，**"192.168.245.134"。

同时，docker登录时请使用 docker  -D login 192.168.245.134。

[http等权限问题1]: https://github.com/vmware/harbor/issues/130
[http等权限问题2]: https://github.com/vmware/harbor/issues/811

#### 4、重启操作

在docker-compose 的目录下，

```
#停止docker： 
docker-compose stop
# 启动docker
docker-compose start
```

要更改Harbour的配置，请先停止现有的Harbor实例并进行更新`harbor.cfg`。然后运行`prepare`脚本以填充配置。最后重新创建并启动Harbor的实例： 

```
docker-compose down -v
vim harbor.cfg
prepare
docker-compose up -d
```

删除Harbor的容器，同时将图像数据和Harbor的数据库文件保存在文件系统上：

```
$ sudo docker-compose down -v
```

删除Harbor的数据库和图像数据（用于干净的重新安装）：

```
$ rm -r /data/database
$ rm -r /data/registry
```

#### 5、端口占用、本地保存文件说明

#### **持久数据：**

默认情况下，注册表数据保留在主机的`/data/`目录中。 

此外，Harbor使用*rsyslog*来收集每个容器的日志。默认情况下，这些日志文件存储在`/var/log/harbor/`目标主机上的目录中以进行故障排除。 

如需修改本地保存路径，需要对docker-compose.yaml文件的挂载点进行逐一修改。

会新建以下目录：

```
# registry
/data/registry	
# mysql
/data/database 
# adminserver
/data/config/ 	
/data/secretkey
# ui
/data/ca_download/
/data/psc/
# jobservice
/data/job_logs/
# redis
/data/redis/
```



#### 端口占用：

```
# docker-compose.yml中
proxy:
    ports:
      - 80:80
      - 443:443
      - 4443:4443
```

如需使用其他端口，如8888，则修改docker-compose.yml中的ports，将80:80改为8888:80，同时修改hostname = 192.168.0.2:8888。

