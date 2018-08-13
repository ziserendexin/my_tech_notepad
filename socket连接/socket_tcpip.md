简述：自己复写一个socket的连接，发送/解析TCP报文，解析struct结构体，进行交互

1. #### 连接运作

   1. 原理概述

      使用`sock.connect((self.host, self.port)`)的方式进行连接，其中socket的定义为 `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`。

   2. 收发数据

      使用ak.query进行数据收发，下发的的命令为在配置文件中,`check.ak.allowed_cmd`,遍历这些命令，收发数据。

      ```
      data.update(ak.query(cmd))
      def query()
      	msg = self.pack(cmd, channel_number)
      	self._send(msg)
      	data_recv = self._recv()
      	out = self.unpack(data_recv)
      	if len(out) > 6:    
      		data[cmd] = out[6]
      	else:
      		data[cmd] = cmd
      	return data 
      ```

      因此返回的data是一个是cmd为key的hash。

      ~~PS：真方便粗暴的方式啊~~

   

2. #### 问题

   1. 日志轮训大小太小，10k。。。能记下啥啊。

   2. 没有心跳检测，心跳检测可以从两个方面，一个是对对面ak服务器的检测，主要是在失联时可以报错。二是在自身数据上入手，有数据处理接收，则上报正常，后面这个可以调低。

   3. 我们是否需要在115上建立一个服务，对所有ip进行ping操作。如果ping不上，则检测是否error。貌似那边已经做了一个，同时对是否有数也进行了测试。明天可以再问下是否是这样。

   4. 续上，这里有个基于socket的方式对ip端口进行连通性测试，emm，不一定好用，之后可以试试是否好用。

      > https://www.linuxhub.org/?p=2373

      但这个是基于，其端口支持socket，也就是tcp，udp都行。之后试试吧。难说好用呢。

3. #### socket编程

   > https://gist.github.com/kevinkindom/108ffd675cb9253f8f71

   首先，创建一个基于IPv4和TCP协议的Socket：

   参数为套接字类型。

   ```
   socket(family, type[,protocal])
   ```

   | socket 类型           | 描述                                                         |
   | --------------------- | ------------------------------------------------------------ |
   | socket.AF_UNIX        | 用于同一台机器上的进程通信（既本机通信）                     |
   | socket.AF_INET        | 用于服务器与服务器之间的网络通信                             |
   | socket.AF_INET6       | 基于IPV6方式的服务器与服务器之间的网络通信                   |
   | socket.SOCK_STREAM    | 基于TCP的流式socket通信                                      |
   | socket.SOCK_DGRAM     | 基于UDP的数据报式socket通信                                  |
   | socket.SOCK_RAW       | 原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK_RAW可以；其次SOCK_RAW也可以处理特殊的IPV4报文；此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头 |
   | socket.SOCK_SEQPACKET | 可靠的连续数据包服务                                         |

   建立连接（TCP）

   ```
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   ```

   （UDP）

   ```
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   ```

   服务器端使用`s.listen(backlog) `,客户端使用连接`s.connect()`

   然后使用公共方法，进行收发，详见上面的连接。

   本例子中，使用`pack`和`unpack`进行二进制转码。

   > https://www.cnblogs.com/gala/archive/2011/09/22/2184801.html

   ```
   struct模块中最重要的三个函数是pack(), unpack(), calcsize()
   
   pack(fmt, v1, v2, ...)     按照给定的格式(fmt)，把数据封装成字符串(实际上是类似于c结构体的字节流)
   
   unpack(fmt, string)       按照给定的格式(fmt)解析字节流string，返回解析出来的tuple
   
   calcsize(fmt)                 计算给定的格式(fmt)占用多少字节的内存
   ```

   fmt是结构体的字符串。

   按照网址中的表，进行转换

   例如：

   ```
   struct Header
   
   {
   
       unsigned short id;
   
       char[4] tag;
   
       unsigned int version;
   
       unsigned int count;
   
   }
   解析为
   struct.unpack("!H4s2I", s)
   !	：表示我们要使用网络字节顺序解析（原来字节顺序）因为我们的数据是从网络中接收到的，在网络上传送的时候它是网络字节顺序的.
   H	：表示 一个unsigned short的id
   4s	：表示4字节长的字符串
   2I	：表示有两个unsigned int类型的数据.
   ```

   

**具体实现可以参考两个模板，再根据现场状态进行修改。**