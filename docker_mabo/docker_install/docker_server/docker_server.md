#### 1、概述

[官方文档(en)]: https://docs.docker.com/registry/deploying/#run-a-local-registry

docker需要一个registry，用做保存、发布容器的地方，这也是一个统一管理docker的方式之一。

鉴于各种乱七八糟的环境原因，我们需要自建一个registry，就是类似一个docker hub的地方。

当然，如有可能，还是用官方的最好喽。

#### 2、registry安装

实际指令：

```
# 下载注册
docker pull registry：2.6.2
# 另存为
docker image save registry:2.6.2 -o /usr/zhy/docker_server_install/registry
# 加载
docker image load -i /usr/zhy/docker_server_install
# 配置开机自启
systemctl enable docker
```

#### 3、registry启动及配置

```
# 使用配置文件、docker-compose的方式进行配置
docker-compose -f docker_server_compose.yaml up -d
```

[配置参考]: https://www.cnblogs.com/wade-luffy/p/6590849.html
[配置参考]: https://www.jianshu.com/p/fc544e27b507
[registry API]: https://docs.docker.com/registry/spec/api/#deleting-a-layer

测试：

```
# 测试网络连通性 获取信息
curl 192.168.245.134:5000/v2/_catalog
# 查看某个镜像的所有tag
curl -X GET 192.168.245.134:5000/v2/【image】/tags/list
```

#### 4、docker镜像上传

求助：没有找到可行的办法直接向私有registry上传docker镜像。

```
# 修改需要上传的镜像的tag
# 其中，192.168.245.134:5000为替换为服务器的节点的IP地址或域名。
# 此处python:mabo可以使用对应的image id
docker tag python:mabo 192.168.245.134:5000/mabo_python:lastest
# 上传docker 镜像
docker push 192.168.245.134:5000/mabo_python:lastest
```

#### 5、使用脚本批量上传下载

```
# 上传指定镜像(可上传多个，中间用空格隔开)
./push.sh ImageName[:TagName][ImageName[:TagName] ···]
# 例如：./push.sh busybox:latest ubutnu:14.04
# 上传所有镜像
./pushall.sh
# 下载指定镜像(可上传多个，中间用空格隔开)
./pull.sh ImageName[:TagName][ImageName[:TagName] ···]
# 例如：./pull.sh busybox:latest ubutnu:14.04
```

> https://www.cnblogs.com/xcloudbiz/articles/5526727.html 

