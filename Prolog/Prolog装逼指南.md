1. 目的

   干嘛！逼格高啊！

   没人能挑战我逼格领主的地位！

2. hello world

> https://www.kancloud.cn/kancloud/learn-prolog-hard-way/48784

```prolog
?- wrteln('Hello World').
Correct to: "writeln('Hello World')"? yes
Hello World
true.
```

在Prolog终端输入的时候，没一个语句都是以“?-”这样两个字符开头的，它代表我们输入的程序代码其实是对Prolog系统的一个查询（问询），一旦用户输入了查询，Prolog系统会运用它的知识库来判定这个查询是真(true)是假(false). writeln是Prolog系统自己定义的一个语句, 它的作用是向当前的显示设备输出一个字符串并且换行, 所以很显然, 这个语句是真的, 因为Prolog知道有这个语句. 这就是为什么程序的最后有一个”true”. 有意思的是,因为整个过程中Prolog都是在试图证明这个语句是真是假, 向屏幕输出”Hello World!”这件事实际上是执行这个语句的”副作用”(side effect)!在Prolog中, 很多任务都是靠副作用来实现的, 包括输入输出, 甚至是参数的传递.