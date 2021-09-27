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

