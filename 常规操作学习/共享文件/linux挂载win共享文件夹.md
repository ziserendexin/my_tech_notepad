


## 1.组建局域网,建立windows/windsxp与centos的通讯
1. 设置Windows/windsxp IP和子网掩码
- 192.168.1.3
- 255.255.255.0
2. 设置centos IP和子网掩码
- 修改文件`/etc/sysconfig/network-script/ifcfg-enp1s0`

```
TYPE=Ethernet
BOOTPROTO=static
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=enp1s0
UUID=d125a0**...
DEVICE=enp1s0
ONBOOT=yes
IPADDR=192.168.1.2
NETMASK=255.255.255.0
```
3. 重启网络
- ifdown ifcfg-enp1s0
- ifup ifcfg-enp1s0


## 2.关闭centos防火墙
1. 关闭防火墙
- systemctl stop firewalld.service 
2. 关闭开机启动防火墙
- systemctl disable firewalld.service

## 3.Windows共享日志文件夹，挂载到centos盘符下

1. windows/windsxp下添加共享用户

   > username：eim
   >
   > password：patac2016

2. 共享以下日志文件夹

   > `C:\Revolutionary Engineering\PATAC\Setup Files\Default`

3. centos下的挂载点路径为

   > 挂载点为`/usr/mabo/re_mount`

4. 后续操作：

   > * 修改配置文件
   > * 一键建立挂载点
   > * 创建监控服务
   > * 启动监控服务
   > * 开机启动监控服务
   >
   > 等操作，[参看监控脚本文档](https://github.com/Mabo-IoT/monitor_shared-folders/blob/master/README.md)

## 4.配置内网IP，方便远程操作centos
1. 修改文件`/etc/sysconfig/network-script/ifcfg-ens1`

```
TYPE=Ethernet
BOOTPROTO=static
DEFROUTE=yes
PEERDNS=yes
PEERROUTES=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_PEERROUTES=yes
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens1
UUID=d125a0**...
DEVICE=ens1
ONBOOT=yes
IPADDR=10.7.95.78
NETMASK=255.255.255.224
GATEWAY=10.7.95.94

```
2. 重启网络
- ifdown ifcfg-ens1
- ifup ifcfg-ens1



## 5.注册程序自启动服务
1. 在 /etc/systemd/system下注册服务,参考re_udp.service：

```
[Unit]
Description=re_udp
Requires=redis_6379.service
After=redis_6379.service

[Service]
WorkingDirectory=/usr/mabo/RE/RE

ExecStart=/usr/local/bin/python3 /usr/mabo/RE/RE/udpserver.py

[Install]
WantedBy=multi-user.target
```
2. 重新加载进程
- systemctl daemon-reload
3. 设置开机启动这个Unit
- systemctl enable re_udp

4. 启动进程
- systemctl start re_udp

5. 查看进程状态是否正确
- systemctl status re_udp -l

