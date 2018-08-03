#### 1、编写Dockerfile

**注意：RUN命令，最好一批运行一次。比如在安装应用的场景上：复制安装文件，编辑，删除安装文件，使用&&相连，这样可以有效减少docker的层次及占用空间。**

示意：

```
FROM python:3.7.0-stretch	 # 从3.7.0-stretch构建镜像
WORKDIR /usr/mabo/		     # docker内部的工作环境
COPY ./mabopython_requirements.txt ./   # 复制requirements列表进去
RUN pip install -r mabopython_requirements.txt \ # pip安装所有
	&& rm mabopython_requirements.txt		# 删除requirements
```

#### 2、构建Dockerfile

```
docker build --rm -t mabo/python:lastest -f mabopython_Dockerfile .
```

部分参数：

> http://www.runoob.com/docker/docker-build-command.html

**--rm :**设置镜像成功后删除中间容器 

**-f :**指定要使用的Dockerfile路径； 

**-t :**输出镜像的名字； 

同时可以通过参数设置构建时的内存、cpu消耗。



#### 3、构建失败，删除\<none\>镜像

> https://docs.docker.com/engine/reference/commandline/image_prune/#filtering

```
 docker image prune 
 # 删除所有悬空图像。如果-a已指定，还将删除未被任何容器引用的所有图像。
 docker system prune
 # 删除所有未使用的容器，网络，图像（悬空和未引用）以及可选的卷。
```

#### 4、构建成功，上传镜像

参考pull&push_batch/README.md

```
../pull&push_batch/push.sh mabo/python:lastest
```

