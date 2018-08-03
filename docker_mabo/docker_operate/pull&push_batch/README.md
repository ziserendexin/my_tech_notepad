#### 0、请务必修改每个脚本中的registry参数。

registry=192.168.245.134:5000

192.168.245.134为我本地调试的参数，修改为具体docker registry的参数

#### 0.1、添加内网环境镜像源

需要在/etc/docker/daemon.json 下添加私服。

添加以下文字：

```
{
    "insecure-registries": [
        "192.168.245.134:5000"
    ]
}
```

[HTTP response to HTTPS]: https://blog.csdn.net/jiankunking/article/details/71190814



#### 1、获取registry的镜像

```
# 测试网络连通性 获取信息
curl 192.168.245.134:5000/v2/_catalog
# 查看某个镜像的所有tag
curl -X GET 192.168.245.134:5000/v2/【image】/tags/list
```

#### 3、下载上传镜像

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



