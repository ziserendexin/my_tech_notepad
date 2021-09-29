[toc]

# hello world

## vscode的配置

被墙无法安装:

https://zhuanlan.zhihu.com/p/53566172

...

https://blog.csdn.net/lvsehaiyang1993/article/details/109067451

还是参考这个, 直接配代理吧

## 配置代理镜像

https://goproxy.io/zh/

```PowerShell 
# Set the GOPROXY environment variable
$env:GOPROXY = "https://goproxy.io,direct"
# Set environment variable allow bypassing the proxy for specified repos (optional)
$env:GOPRIVATE = "git.mycompany.com,github.com/my/private"
```

噢噢噢噢, 这个是配置代理镜像.

## Vscode的go

正常的go倒是可以了. 但vscode这个, 还是下载不下来.

```
Tools environment: GOPATH=C:\Users\ziserendexin\go
```

在日志有个这个, 说明这里这个env需要改一下

https://juejin.cn/post/6869362277896847367

环境变量里面的改了就能装了...emmm....

实际上vscode取的还是环境变量里面的, 而不是go env里面.

所以实质上还是尽量保持两个一致比较好.

### vscode的调试

基本上按照提示安装完那堆包, 然后F5就行了...emmm

其中报错:

https://stackoverflow.com/questions/66894200/go-go-mod-file-not-found-in-current-directory-or-any-parent-directory-see-go

```
go: go.mod file not found in current directory or any parent directory; see 'go help modules'
```

然后

```
go mod init test3
```

这个不是很懂为啥, 后续需要看看go mod的相关内容, 这里先看gopath的介绍

### go path

http://c.biancheng.net/view/88.html

从这里看出, 关于GOPATH这个问题, 需要考虑是否跟随项目, 

> 大家现在go项目如何管理的？一个项目是一个gopath下的包，还是一个新的gopath？ - 匿名人士的回答 - 知乎 https://www.zhihu.com/question/47538279/answer/126170419

> #### 关于gopath和项目, vgo的问题===>貌似就是go mod 1.11版本加的东西?
>
> https://stackoverflow.com/questions/40715285/setting-gopath-for-each-vscode-project
>
> 这里提出了一个叫做vgo的概念.
>
> 但貌似也不是啥主流的做法.

**所以go的版本依赖问题, 也不小啊**

### go mod

https://www.jianshu.com/p/760c97ff644c

首先需要开启:

```
GO111MODULE="on"
```

<!--这几个111是什么鬼, 为了最先读取到, 你特么真拼...-->

https://learnku.com/go/t/39086
