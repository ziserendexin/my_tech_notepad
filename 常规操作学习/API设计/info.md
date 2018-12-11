1. 前言

   年月日收到windows这些庞大而且强大，并且迷一般的感觉好多余的影响，想看看供给各种程序调用的api是如何设计，实现的。

2. 钩子式

   在程序中(函数)写入钩子列表，每个函数调用前后，都会先访问钩子列表以及钩子列表中所指向的函数。

   然后通过指针，再去看其他程序想要做的事情。当然，这种设计需要对修改者程序有充分的了解。或者有充分的文档？

   可以参考下面的两个。

   > https://www.kilerd.me/archives/26
   >
   > https://blog.csdn.net/rankun1/article/details/50973190

3. RESTFUL API

   > RESTFUL API 原理以及实现
   >
   > https://www.zybuluo.com/phper/note/79184
   >
   > RESTful API 设计指南
   >
   > http://www.ruanyifeng.com/blog/2014/05/restful_api.html

   比如，获取QQ空间用户发的说说列表：：

   > - QQ空间网站里面需要这个功能。
   > - Andoid APP里面也需要这个功能。
   > - iOS APP里面也需要这个功能。

   就可以以以下方式实现：

   > - QQ Zone web: <https://api.qzone.com/user/getUserFeedList?from=web>
   > - QQ Zone Android: <https://api.qzone.com/user/getUserFeedList?from=android>
   > - QQ Zone iOS: <https://api.qzone.com/user/getUserFeedList?from=ios>
