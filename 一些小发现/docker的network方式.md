这里发现有的机子，解析redis有问题。

```shell
bash-4.4# ping redis
ping: bad address 'redis'
```

然后深入研究下，是那里出了问题。

## link方式

https://yq.aliyun.com/articles/55912
关于docker网络的解析，通过link的实现是通过再etc/hosts中添加，但这边docker-compose不是使用这个方式。

## 内置DNS解析（127.0.0.11）

应该是基于基于DNS的名称自动解析

通过：

```shell
bash-4.4# cat /etc/resolv.conf 
search localdomain
nameserver 127.0.0.11
options ndots:0
```

可以看到，这里默认的DNS是127.0.0.11.

可以使用：

```bash
bash-4.4# nslookup redis
nslookup: can't resolve '(null)': Name does not resolve

Name:      redis
Address 1: 172.19.0.4 redis.tv-nel-motor_back
```

解析，正常的DNS是可以解析过去的。

不正常的：

```bash
bash-4.4# nslookup redis
nslookup: can't resolve '(null)': Name does not resolve

nslookup: can't resolve 'redis': Try again
```

自然是解析不到。

下一个问题是，如何查看这个嵌入式DNS服务的状态（embedded DNS server ）呢？

> https://www.jianshu.com/p/4433f4c70cf0
>
> https://cloud.tencent.com/developer/article/1096388

这边通过展示：`netstat -lutnp `发现异常

正常（容器内）：

```bash
bash-4.4# netstat -lutnp 
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      1/python
tcp        0      0 127.0.0.11:42390        0.0.0.0:*               LISTEN      -
udp        0      0 127.0.0.11:47691        0.0.0.0:*                           -
```

异常

```bash
bash-4.4# netstat -lutnp 
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      1/python
udp        0      0 0.0.0.0:34177           0.0.0.0:*                           1/python
udp        0      0 0.0.0.0:41090           0.0.0.0:*                           1/python
```

> -a (all)显示所有选项，默认不显示LISTEN相关
> -t (tcp)仅显示tcp相关选项
> -u (udp)仅显示udp相关选项
> -n 拒绝显示别名，能显示数字的全部转化成数字。
> -l 仅列出有在 Listen (监听) 的服務状态
>
> -p 显示建立相关链接的程序名
> -r 显示路由信息，路由表
> -e 显示扩展信息，例如uid等
> -s 按各个协议进行统计
> -c 每隔一个固定时间，执行该netstat命令。

可以确信是这个DNS挂了，但怎么挂的，为啥挂了。

这就不清楚了。

<!--反正重启容器是可以解决的就是了。-->