> https://www.zhihu.com/question/29620953
>
> https://www.cnblogs.com/guogangj/p/4118605.html

------

阅读指南

1、2需要了解，

3，为扩展知识，

4....你看心情吧。。。虽然我是写了，但都不代表我看懂了。但可以使用‘乘法来类比’，这个来作为类比概念性理解。

5,6,是一些资料。

7，就是个实践性的操作，这里以实际所用的influxdb作为方式。

------

1. #### 目标

   搞清楚什么是https，怎么加密，相互通信的时候需要什么样子的证书，需要哪些解密加密信息。

   > https://www.cnblogs.com/handsomeBoys/p/6556336.html

   http的缺点：

   - 容易被监听 
     - http通信都是明文，数据在客户端与服务器通信过程中，任何一点都可能被劫持。比如，发送了银行卡号和密码，hacker劫取到数据，就能看到卡号和密码，这是很危险的
   - 被伪装 
     - http通信时，无法保证通行双方是合法的，通信方可能是伪装的。比如你请求www.taobao.com,你怎么知道返回的数据就是来自淘宝，中间人可能返回数据伪装成淘宝。
   - 被篡改 
     - hacker中间篡改数据后，接收方并不知道数据已经被更改

   https的优点：

   - 防监听 
     - 数据是加密的，所以监听得到的数据是密文，hacker看不懂。
   - 防伪装 
     - 伪装分为客户端伪装和服务器伪装，通信双方携带证书，证书相当于身份证，有证书就认为合法，没有证书就认为非法，证书由第三方颁布，很难伪造
   - 防篡改 
     - https对数据做了摘要，篡改数据会被感知到。hacker即使从中改了数据也白搭。

2. #### 加密方式

   > http://www.ruanyifeng.com/blog/2011/08/what_is_a_digital_signature.html
   >
   > https://www.zhihu.com/question/33645891

   1. 公钥&私钥

      简单记忆：

      > https://zh.wikipedia.org/wiki/%E5%85%AC%E5%BC%80%E5%AF%86%E9%92%A5%E5%8A%A0%E5%AF%86

      内容：公钥加密，私钥解密。

      签名：私钥加密，公钥解密。

   2. 实际内容的加密

      私钥拥有者(一般是在server端)，通过对私钥进行运算，得到一个公钥。

      内容发送者，用公钥进行加密(不可逆)，这样，除了使用私钥以外的任何方式，都无法对这段内容进行解密。

   3. 信息传递过程

      ![TLS加密握手](.\jpg\TLS加密握手.jpg)

      研究思路是，先看要防止什么问题，然后怎么做。然后再来个simple的流程。

      1. 密钥的传递

         在一般的https交互中，通过向server申请公钥（客户端发起HTTPS请求，链接到443端口）。

      2. 证书验证（公钥放在证书里）

         为了防止证书被其他人作为中介给占用了，所以可以先组织申请证书，这样client接到公钥证书以后，会向组织进行一次验证，验证这个证书是否合法。

         PS：比如谷歌就在15年的时候吊销了CNNIC的所有证书的信任，以及12306，日常要求安装根证书(CA,就是基础信任的证书)。

         PS2:https最可能被攻击的方式就是中间人攻击，因此CA体系才是尤其的重要。

         PS3:https://www.zhihu.com/question/19974739 看看八卦。就基本理清楚证书的含义以及各种签发方式和可以做的玩法。

         PS4:对于防止中间人攻击的某个方式就是，通过对证书加一个指纹，sha1，与远端进行比对下，

      3. client加密及对称加密

         由于非对称加密（比如RSA）的性能很低，所以一般只在我收过程中使用非对称，之后则转换为对称加密

         所以在2中需要增加一个加密算法以及信息完整性校验算法（对称和md5）。

         同时考虑到1浏览器不一定支持所有加密方式，所有在1中会传递支持的加密方式。

         此时，client使用server给的hash，对传递过来的握手消息进行计算，并产生用于对称加密的随机数。将这两个用对称加密进行加密。

      4. server端解析

         server端后，得到对称加密的随机数，并且可以使用hash校验数据是否一致。

      5. 之后使用对称加密

      简而言之就是：

      ```
      1.浏览器将自己支持的一套加密规则发送给网站。 
      2.网站从中选出一组加密算法与HASH算法，并将自己的身份信息以证书的形式发回给浏览器。证书里面包含了网站地址，加密公钥，以及证书的颁发机构等信息。 
      3.浏览器获得网站证书之后浏览器要做以下工作： 
      	a) 验证证书的合法性（颁发证书的机构是否合法，证书中包含的网站地址是否与正在访问的地址一致等），如果证书受信任，则浏览器栏里面会显示一个小锁头，否则会给出证书不受信的提示。 
      	b) 如果证书受信任，或者是用户接受了不受信的证书，浏览器会生成一串随机数的密码，并用证书中提供的公钥加密。 
      	c) 使用约定好的HASH算法计算握手消息，并使用生成的随机数对消息进行加密，最后将之前生成的所有信息发送给网站。 
      4.网站接收浏览器发来的数据之后要做以下的操作： 
      	a) 使用自己的私钥将信息解密取出密码，使用密码解密浏览器发来的握手消息，并验证HASH是否与浏览器发来的一致。 
      	b) 使用密码加密一段握手消息，发送给浏览器。 
      5.浏览器解密并计算握手消息的HASH，如果与服务端发来的HASH一致，此时握手过程结束，之后所有的通信数据将由之前浏览器生成的随机密码并利用对称加密算法进行加密。
      ```

      PS:在看what_is_a_digital_signature.html的时候就有个疑惑，为啥还要再多一次握手动作，实际上多的这一次是为了加快速度及传递对称加密的信息。

      > https://en.wikipedia.org/wiki/Certificate_authority

      PS2:CA申请的时候，会将CA自己的公钥及私钥共同打包传递给申请者。

3. #### 加密方式

       非对称加密算法：RSA，DSA/DSS 
       对称加密算法：AES，RC4，3DES 
       HASH算法：MD5，SHA1，SHA256

4. #### 密码学base

   http://www.ruanyifeng.com/blog/2006/12/notes_on_cryptography.html

   设计原则：

   - 公钥和私钥是一一对应的关系，有一把公钥就必然有一把与之对应的、独一无二的私钥，反之亦成立。

   - 所有的（公钥, 私钥）对都是不同的。

   - 用公钥可以解开私钥加密的信息，反之亦成立。

   - 同时生成公钥和私钥应该相对比较容易，但是从公钥推算出私钥，应该是很困难或者是不可能的。

   目前，通用的单钥加密算法为DES（Data Encryption Standard），通用的双钥加密算法为RSA（ Rivest-Shamir-Adleman），都产生于上个世纪70年代。

   在双钥体系中，**公钥用来加密信息，私钥用来数字签名**。

   ```
     (对内容进行摘要(digest)，使用私钥加密，得到数字签名(signature))
   ```

   让我们再来深入一点，了解加密具体是怎么做的。

   1. RSA

      > https://zh.wikipedia.org/wiki/RSA%E5%8A%A0%E5%AF%86%E6%BC%94%E7%AE%97%E6%B3%95

      **原理&简述**：对极大整数做[因数分解](https://zh.wikipedia.org/wiki/%E5%9B%A0%E6%95%B0%E5%88%86%E8%A7%A3)的难度决定了RSA算法的可靠性。换言之，对一极大整数做因数分解愈困难，RSA算法愈可靠。假如有人找到一种快速因数分解的算法的话，那么用RSA加密的信息的可靠性就肯定会极度下降。但找到这样的算法的可能性是非常小的。今天只有短的RSA钥匙才可能被强力方式解破。到目前为止，世界上还没有任何可靠的攻击RSA算法的方式。只要其钥匙的长度足够长，用RSA加密的信息实际上是不能被解破的。

      **过程：**

      .......????????????????????????????

      > https://www.zhihu.com/question/33645891

      参考知乎这篇文章，貌似有点道理。

      先拿乘法来类比下：

      - 对方想一个3位数(123)，并把其和91相乘。得到11193，取出最后三位。123。

        貌似

      - 但如果对方告诉我，他使用91乘的，辣么，我对123，再乘以11，就能得到对方想的数字。

      - 因为，91*11=1001，而1001无论乘以任何三位数，后三位都不变。

      - 同时，知道91以后，可以推得11.但不知91，就很难吧1001分解成91和11.

      - 只要数字够长，那么加密性能就越好。

      再用实际的RSA来看看。

      加密：
      $$
      \begin{align*}
      1. & 选两个很大的质数 p, q ；\\
      
      2. &计算 N=p\cdot q ，且 N 被公开； \\
      
      3.&根据\textbf{欧拉函数}，求得r=φ(N)=φ(p)φ(q)=(p-1)(q-1)   \\
      
      4. &再选一个数字 e ，需要保证 e 和 (p-1)(q-1) 互质。\\ 
      
      5. &\textbf{加密}:如需加密信息 X，计算Y= X^e \mod N 。\\
      
      6. &为解密，找到一个数字 d ，满足 de\equiv1\mod(p-1)(q-1) ； \\
      &（模反元素存在，当且仅当 {\displaystyle e} 与 {\displaystyle r} 互质）\\
      
      \end{align*}
      $$
      ​	(N,d)为**私钥**，

      ​	(N,e)为**公钥**。

      **解密**的过程简单来讲是这样的：
      $$
      \begin{align*}
      
      
      
      1. &解密信息 Y ，需要计算 Y^d\mod N 。\\\\
      
      PS:& 也就是说，d*e与1对(p-1)(q-1)同余.\\
      & 当两个整数除以同一个正整数，若得相同余数，则二整数同余。
      \\
      
      
      \end{align*}
      $$

      安全性：

        	当获取到了(N,e),及加密消息Y,的时候，是无法直接获得d的，

        	要获得 d，最简单的方法是将 N 分解为 p和p，这样她可以得到[同余方程](https://zh.wikipedia.org/wiki/%E7%BA%BF%E6%80%A7%E5%90%8C%E4%BD%99%E6%96%B9%E7%A8%8B)：
      ​    
      $$
      {\displaystyle de=1(\mathrm {mod} (p-1)(q-1))}并解出{\displaystyle d}，然后代入解密公式。
      $$
      ​	并解出d，然后代入解密公式。

        	导出*n*（破密）。但至今为止还没有人找到一个多项式时间的算法来分解一个大的整数的因子，同时也还没有人能够证明这种算法不存在（见[因数分解](https://zh.wikipedia.org/wiki/%E5%9B%A0%E6%95%B0%E5%88%86%E8%A7%A3)）。

        	至今为止也没有人能够证明对N进行因数分解是唯一的从c导出N的方法，但今天还没有找到比它更简单的方法。（至少没有公开的方法。）

        当然，此处也应该指出，如果p、q被舍弃掉的情况下，是无法从私钥推导出公钥。

      > https://blog.csdn.net/caomiao2006/article/details/7470637
      >
      > >   [阮一峰](http://www.ruanyifeng.com/)：http://www.ruanyifeng.com/blog/2013/07/rsa_algorithm_part_two.html

        扩展**欧拉定理**：
      $$
        \begin{align*}
        &在数论中，欧拉定理（也称费马-欧拉定理或欧拉 {\displaystyle {\varphi }} 函数定理）是一个关于同余的性质。 \\
        &欧拉定理表明，若 {\displaystyle n,a} 为正整数，且 {\displaystyle N,a}互素（即 {\displaystyle \gcd(N,a)=1} )，则 \\
        \end{align*}
        \\ {\displaystyle a^{\varphi (N)}\equiv 1{\pmod {N}}} 
        \\
        \ \ \ 即 {\displaystyle a^{\varphi (N)}}与1在模n下同余；φ(n)为欧拉函数。\\
        \ \ \ 本例子中，φ(N)为(p-1)(q-1)
      $$

   2. 椭圆曲线密码学(ECC)

      对于ECC系统来说，完成运行系统所必须的群操作比同样大小的因数分解系统或模整数离散对数系统要慢。不过，ECC系统的拥护者相信ECDLP问题比DLP或因数分解问题要难的多，并且因此使用ECC能用小的多的[密钥长度](https://zh.wikipedia.org/wiki/%E5%AF%86%E9%92%A5%E9%95%BF%E5%BA%A6)来提供同等的安全，在这方面来说它确实比例如[RSA](https://zh.wikipedia.org/wiki/RSA%E5%8A%A0%E5%AF%86%E6%BC%94%E7%AE%97%E6%B3%95)之类的更快。到目前为止已经公布的结果趋于支持这个结论，不过一些专家表示怀疑。

      ECC被广泛认为是在给定密钥长度的情况下，最强大的非对称算法，因此在对带宽要求十分紧的连接中会十分有用。

      **过程：**

      .......????????????????????????????

5. #### SSL(TSL)&OpenSSL

   **传输层安全性协议**（英语：Transport Layer Security，[缩写](https://zh.wikipedia.org/wiki/%E7%B8%AE%E5%AF%AB)作 **TLS**），及其前身**安全套接层**（Secure Sockets Layer，缩写作 **SSL**）是一种[安全协议](https://zh.wikipedia.org/wiki/%E5%AE%89%E5%85%A8%E5%8D%8F%E8%AE%AE)，目的是为[互联网](https://zh.wikipedia.org/wiki/%E7%B6%B2%E9%9A%9B%E7%B6%B2%E8%B7%AF)通信提供安全及数据[完整性](https://zh.wikipedia.org/wiki/%E5%AE%8C%E6%95%B4%E6%80%A7)保障。

   **OpenSSL** - 简单地说,OpenSSL是SSL的一个实现,SSL只是一种规范.理论上来说,SSL这种规范是安全的,目前的技术水平很难破解,但SSL的实现就可能有些漏洞,如著名的"心脏出血".OpenSSL还提供了一大堆强大的工具软件,强大到90%我们都用不到.

6. #### 数字证书格式

   > https://zh.wikipedia.org/wiki/X.509

   X.509有多种常用的扩展名。不过其中的一些还用于其它用途，就是说具有这个扩展名的文件可能并不是证书，比如说可能只是保存了私钥。

   - `.pem` – ([隐私增强型电子邮件](https://zh.wikipedia.org/w/index.php?title=%E9%9A%90%E7%A7%81%E5%A2%9E%E5%BC%BA%E5%9E%8B%E7%94%B5%E5%AD%90%E9%82%AE%E4%BB%B6&action=edit&redlink=1)) [DER](https://zh.wikipedia.org/w/index.php?title=DER&action=edit&redlink=1)编码的证书再进行[Base64](https://zh.wikipedia.org/wiki/Base64)编码的数据存放在"-----BEGIN CERTIFICATE-----"和"-----END CERTIFICATE-----"之中
   - `.cer`, `.crt`, `.der` – 通常是[DER](https://zh.wikipedia.org/w/index.php?title=DER&action=edit&redlink=1)二进制制式的，但Base64编码后也很常见。
   - `.p7b`, `.p7c` – [PKCS#7](https://zh.wikipedia.org/wiki/%E5%85%AC%E9%92%A5%E5%AF%86%E7%A0%81%E5%AD%A6%E6%A0%87%E5%87%86) SignedData structure without data, just certificate(s) or [CRL](https://zh.wikipedia.org/wiki/%E8%AF%81%E4%B9%A6%E5%90%8A%E9%94%80%E5%88%97%E8%A1%A8)(s)
   - `.p12` – [PKCS#12](https://zh.wikipedia.org/wiki/%E5%85%AC%E9%92%A5%E5%AF%86%E7%A0%81%E5%AD%A6%E6%A0%87%E5%87%86)制式，包含证书的同时可能还有带密码保护的私钥
   - `.pfx` – PFX，PKCS#12之前的制式（通常用PKCS#12制式，比如那些由[IIS](https://zh.wikipedia.org/wiki/IIS)产生的PFX文件）

7. #### influxDB开启https

   > https://docs.influxdata.com/influxdb/v1.6/administration/https_setup/

   1. 生成自签名证书

      ```
      # sudo openssl req -x509 -nodes -newkey rsa:2048 -keyout /usr/mabo/ssl_key/ssl_keyinfluxdb-selfsigned.key -out /usr/mabo/ssl_key/influxdb-selfsigned.crt -days 3650
      
      sudo openssl req -x509 -nodes -newkey rsa:2048 -keyout /etc/ssl/influxdb-selfsigned.key -out /etc/ssl/influxdb-selfsigned.crt -days <NUMBER_OF_DAYS>
      ```

   2. 重检TLS配置

   3. 开启ssl配置

      ```
      https-enabled to true
      https-certificate to /etc/ssl/influxdb-selfsigned.crt
      https-private-key to /etc/ssl/influxdb-selfsigned.key
      ```

   4. 重启influxdb

   5. 通过命令行验证ssl是否正常工作

   6. 注意修改telegraf为https模式

      **试验失败。。。不行不行，这样做需要配置的东西太多了。不行不行。还是使用Nginx的代理来做ssl**

8. #### 代理服务

   还有种方式是把Nginx放在这些应用前面，实现方向代理。这样做的好处是，只需要配置一个代理即可。个人比较喜欢这个，但还是出两个版本吧。

   1. base

      首先需要了解nginx的配置说明。

      其配置文件名为nginx.conf，位置不一定一样，但在docker内部，其配置文件文件位于`/etc/nginx/conf.d/default.conf`。

      官方docker中的方式，是使用`envsubst`将个性化配置加入到`default.conf`中。优劣。。。仁者见仁智者见智吧。

   2. 负载均衡

      需要使用upstream，上有服务器，设置，将其放于http块中。参考应用：

      https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/#proxying-http-traffic-to-a-group-of-servers

      例如，以下配置定义了一个名为**backend**的组，它由三个服务器配置组成（可以在三个以上的实际服务器中解析）：

      ```
      http {
          upstream backend {
              server backend1.example.com;
              server backend2.example.com;
              server 192.0.0.1 backup;
          }
          
          server {
              location / {
                  proxy_pass http://backend;
              }
          }
      }
      ```

       默认使用Round Robin算法进行负载均衡。

      同时，可以如下所示，给server设置权重，权重高德更容易被选中。

      ```
      upstream backend {
          server backend1.example.com weight=5;
          server backend2.example.com;
          server 192.0.0.1 backup;
      }
      ```

      值得注意的是，有以下功能。后续如需配置，可以参考：

      - 慢启动：恢复可用后，逐渐增加权重
      - 持久会话：可以按照cookie、路由、学习的方式，建立持久性会话。
      - 限制连接数
      - 连接健康检查：可以设置失败次数，重试时间间隔。
      - 活跃健康检查

   3. 响应缓存

      NGINX Plus会将响应保存在磁盘缓存中，并使用它们响应客户端，而无需每次都代理对相同内容的请求。

   4. 网络服务

      1. web服务器

         可以使用Nginx做一些简单的重定向之类的操作。

      2. 静态网页内容

      3. 反向代理

         通过不同协议，将请求从Nginx传递到代理服务器。

         当然还能设置缓存与传出ip。

      4. 压缩gzip

      5. 【重点来了】安全控制

         1. https

            设置https的时候，在配置文件中的server包换ssl参数。

            ```
            worker_processes auto;
            
            http {
                ssl_session_cache   shared:SSL:10m;
                ssl_session_timeout 10m;
            
                server {
                    listen              443 ssl;
                    server_name         www.example.com;
                    keepalive_timeout   70;
            
                    ssl_certificate     www.example.com.crt;
                    ssl_certificate_key www.example.com.key;
                    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
                    ssl_ciphers         HIGH:!aNULL:!MD5;
                    #...
                }
            }
            ```

         2. 对上游服务而言的ssl 终止

            SSL终止意味着NGINX Plus充当与客户端连接的服务器端SSL端点：它执行请求的解密和后端服务器本来必须执行的响应的加密。该操作称为终止，因为NGINX Plus关闭客户端连接，并通过新创建的未加密连接将客户端数据转发到上游组中的服务器。在R6及更高版本中，NGINX Plus为TCP连接和HTTP连接执行SSL终止。【这就是我想要的】

            完整的例子：

            ```
            stream {
                upstream stream_backend {
                     server backend1.example.com:12345;
                     server backend2.example.com:12345;
                     server backend3.example.com:12345;
                }
            
                server {
                    listen                12345 ssl;
                    proxy_pass            stream_backend;
            
                    ssl_certificate       /etc/ssl/certs/server.crt;
                    ssl_certificate_key   /etc/ssl/certs/server.key;
                    ssl_protocols         SSLv3 TLSv1 TLSv1.1 TLSv1.2;
                    ssl_ciphers           HIGH:!aNULL:!MD5;
                    ssl_session_cache     shared:SSL:20m;
                    ssl_session_timeout   4h;
                    ssl_handshake_timeout 30s;
                    #...
                 }
            }
            ```

            在此示例中，`server`块中的指令指示NGINX Plus终止并解密来自客户端的安全TCP流量，并将其未加密传递到`stream_backend`由三个服务器组成的上游组。

         3. 基于http身份的访问限制

            > https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/

         4. 访问限制

            比如禁止一些ip地址，禁止一些端口之类的操作。

      6. 监控方式——仪表盘及配置简单的api工具等

         > https://docs.nginx.com/nginx/admin-guide/monitoring/live-activity-monitoring/

      7. 高可用

         。。。去死吧，看不懂。感觉不如直接上k8s。。。

   5. docker之Nginx配置

      貌似不能直接使用其配置了，这样需要直接使用覆盖配置文件的方式来做了。



   > > http://seanlook.com/2015/05/17/nginx-install-and-config/
   >
   > > Nginx配置文件主要分成四部分：main（全局设置）、server（主机设置）、upstream（上游服务器设置，主要为反向代理、负载均衡相关配置）和 location（URL匹配特定位置后的设置），每部分包含若干个指令。main部分设置的指令将影响其它所有部分的设置；server部分的指令主要用于指定虚拟主机域名、IP和端口；upstream的指令用于设置一系列的后端服务器，设置反向代理及后端服务器的负载均衡；location部分用于匹配网页位置（比如，根目录“/”,“/images”,等等）。他们之间的关系式：server继承main，location继承server；upstream既不会继承指令也不会被继承。它有自己的特殊指令，不需要在其他地方的应用。
   >
   > 1. 结构组成
   >
   >    > https://docs.nginx.com/nginx/admin-guide/basic-functionality/managing-configuration-files/
   >
   >    配置文件由指令和参数组成，指令以分号皆为。将指令组合在一起，括在花括号中，这个称为块。
   >
   >    为了便于维护，可以将部分存储于特定目录中。
   >
   >    观察官方配置文件。见文件夹[nginx.conf](./example_conf/nginx/nginx.conf)。可以看到这个配置文件包含了两种配置文件，一个是`/etc/nginx/mime.types`另一个是`/etc/nginx/conf.d/*.conf`,
   >
   > 2. main部分
   >
   >    woker_xxx
   >
   >    这部分配置cpu消耗部分的设置，需要根据cpu进行配置。影响最大链接、转发性能等问题。
   >

9. #### **docker secret**

   > https://blog.csdn.net/dkfajsldfsdfsd/article/details/79961552
   >
   > https://www.ibm.com/developerworks/community/blogs/132cfa78-44b0-4376-85d0-d3096cd30d3f/entry/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8_Secret_%E6%AF%8F%E5%A4%A95%E5%88%86%E9%92%9F%E7%8E%A9%E8%BD%AC_Docker_%E5%AE%B9%E5%99%A8%E6%8A%80%E6%9C%AF_108?lang=en

   对于docker来说，适合把所有的加密信息给保存至secret中。

   但这个只适用于docker swarm集群中。单机貌似不行，所以此处跳过。

   当然，k8s也有secret。所以参考下面k8s的说明：

   > https://kubernetes.io/docs/concepts/configuration/secret/
