# 安装说明

base on CentOS7:1611

#### 1、支撑安装

原始命令为：

```
yum install -y yum-utils \
           device-mapper-persistent-data \
           lvm2
```

离线状态下，使用：

```
yum localinstall ./docker_package/*.rpm
```



#### 2、docker本体的安装

原始命令：

```
# 添加yum源：阿里
yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
# 更新yum索引
yum makecache fast
# 安装docker 社区版。cc为商业版，此处使用ce版。
yum install docker-ce
```

离线状态：

```
yum localinstall ./docker/*.rpm
```

#### 3、启动&检测

然后就到了万众瞩目的启动阶段。

```
# 加载deamon
systemctl daemon-reload
# 重启docker
systemctl restart docker
# 查看是否安装成功
docker info
```

#### 4、镜像源说明(可跳过)

鉴于GFW，可以添加以下几个镜像源。

同时，不同镜像源有挺多不同私人镜像。

当然，也可以在pull的时候单独拉取某地址的某些信息。

添加方式：(添加官方中文镜像源)

```
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://registry.docker-cn.com"]
}
EOF
```

其他几个：推荐度：阿里>官方>163>其他

阿里需要在阿里云的开发者平台注册，然后进入右上角的管理中心，进入镜像加速器，获取专属镜像源，但用别人的也没事。

```
 "https://registry.docker-cn.com",	# 官方
 "http://hub-mirror.c.163.com",		# 163
 "https://74bks5gr.mirror.aliyuncs.com"	# 阿里源
```

#### 5、添加docker-compose功能

将docker-compose文件夹下内容，放入/usr/local/bin/下，然后chmod +x即可。

```
sudo cp ./docker-compose/docker-compose /usr/local/bin/
sudo chmod +x /usr/local/bin/docker-compose
```



#### 6、添加内网环境镜像源（研究中）

需要在/etc/docker/daemon.json 下添加私服。

添加以下文字：

```
{
    "registry-mirrors": [
        "http://192.168.245.134:5000",
        "https://registry.docker-cn.com"
    ],
    "insecure-registries": [
        "192.168.245.134:5000","192.168.245.134"
    ]
}
```



[HTTP response to HTTPS]: https://blog.csdn.net/jiankunking/article/details/71190814



#### 7、与私有库，registry，进行测试

```
# 测试网络连通性 获取信息

curl 192.168.245.134:5000/v2/_catalog

# 查看某个镜像的所有tag

curl -X GET 192.168.245.134:5000/v2/【image】/tags/list
```

