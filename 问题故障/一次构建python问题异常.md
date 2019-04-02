> <https://github.com/docker-library/python/issues/378>
>
> 提出的issu

I have same problem.

The most confused is, when i retry it at alpine.

When I splite this cmd to four cmd, and run.every thing is ok.

```
apk add --no-cache --virtual .build-deps gcc musl-dev curl 
```

```
apk add --no-cache --virtual .build-deps 
apk add --no-cache --virtual gcc 
apk add --no-cache --virtual musl-dev 
apk add --no-cache --virtual curl
```

But run at one line, it will give this error.

```
/ # apk add --no-cache --virtual .build-deps gcc musl-dev curl 
fetch http://mirrors.aliyun.com/alpine/v3.6/main/x86_64/APKINDEX.tar.gz
fetch http://mirrors.aliyun.com/alpine/v3.6/community/x86_64/APKINDEX.tar.gz
(1/21) Downgrading musl (1.1.20-r4 -> 1.1.16-r15)
(2/21) Installing binutils-libs (2.30-r1)
(3/21) Installing binutils (2.30-r1)
(4/21) Installing gmp (6.1.2-r0)
(5/21) Installing isl (0.17.1-r0)
(6/21) Installing libgomp (6.3.0-r4)
(7/21) Installing libatomic (6.3.0-r4)
(8/21) Installing pkgconf (1.3.7-r0)
(9/21) Installing libgcc (6.3.0-r4)
(10/21) Installing mpfr3 (3.1.5-r0)
(11/21) Installing mpc1 (1.0.3-r0)
(12/21) Installing libstdc++ (6.3.0-r4)
(13/21) Installing gcc (6.3.0-r4)
(14/21) Installing musl-dev (1.1.16-r15)
(15/21) Installing libressl2.5-libcrypto (2.5.5-r2)
(16/21) Installing libssh2 (1.8.2-r0)
(17/21) Installing libressl2.5-libssl (2.5.5-r2)
(18/21) Installing libcurl (7.61.1-r2)
(19/21) Installing curl (7.61.1-r2)
(20/21) Installing .build-deps (0)
(21/21) Downgrading musl-utils (1.1.20-r4 -> 1.1.16-r15)
Executing busybox-1.29.3-r10.trigger
OK: 115 MiB in 54 packages
/ # python
Error relocating /usr/local/lib/libpython3.7m.so.1.0: getrandom: symbol not found
/ # exit

```

```
# apk add --no-cache --virtual .build-deps 
fetch http://mirrors.aliyun.com/alpine/v3.6/main/x86_64/APKINDEX.tar.gz
fetch http://mirrors.aliyun.com/alpine/v3.6/community/x86_64/APKINDEX.tar.gz
(1/1) Installing .build-deps (0)
OK: 18 MiB in 36 packages
/ # apk add --no-cache --virtual gcc 
fetch http://mirrors.aliyun.com/alpine/v3.6/main/x86_64/APKINDEX.tar.gz
fetch http://mirrors.aliyun.com/alpine/v3.6/community/x86_64/APKINDEX.tar.gz
(1/12) Installing binutils-libs (2.30-r1)
(2/12) Installing binutils (2.30-r1)
(3/12) Installing gmp (6.1.2-r0)
(4/12) Installing isl (0.17.1-r0)
(5/12) Installing libgomp (6.3.0-r4)
(6/12) Installing libatomic (6.3.0-r4)
(7/12) Installing pkgconf (1.3.7-r0)
(8/12) Installing libgcc (6.3.0-r4)
(9/12) Installing mpfr3 (3.1.5-r0)
(10/12) Installing mpc1 (1.0.3-r0)
(11/12) Installing libstdc++ (6.3.0-r4)
(12/12) Installing gcc (6.3.0-r4)
Executing busybox-1.29.3-r10.trigger
OK: 102 MiB in 48 packages
/ # apk add --no-cache --virtual musl-dev
fetch http://mirrors.aliyun.com/alpine/v3.6/main/x86_64/APKINDEX.tar.gz
fetch http://mirrors.aliyun.com/alpine/v3.6/community/x86_64/APKINDEX.tar.gz
(1/1) Installing musl-dev (0)
OK: 102 MiB in 49 packages
/ # apk add --no-cache --virtual curl
fetch http://mirrors.aliyun.com/alpine/v3.6/main/x86_64/APKINDEX.tar.gz
fetch http://mirrors.aliyun.com/alpine/v3.6/community/x86_64/APKINDEX.tar.gz
(1/5) Installing libressl2.5-libcrypto (2.5.5-r2)
(2/5) Installing libssh2 (1.8.2-r0)
(3/5) Installing libressl2.5-libssl (2.5.5-r2)
(4/5) Installing libcurl (7.61.1-r2)
(5/5) Installing curl (7.61.1-r2)
Executing busybox-1.29.3-r10.trigger
OK: 105 MiB in 54 packages
/ # python
Python 3.7.3 (default, Mar 27 2019, 23:48:15) 
[GCC 8.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 

```

> <https://github.com/gliderlabs/docker-alpine/issues/459>
>
> 这个是alpine里面的问题
>
> <https://bugs.alpinelinux.org/issues/9642>
>
> 我是不是也该去提一个？

Layers infomation:

```
"Layers": [
                "sha256:bcf2f368fe234217249e00ad9d762d8f1a3156d60c442ed92079fa5b120634a1",
                "sha256:aabe8fddede54277f929724919213cc5df2ab4e4175a5ce45ff4e00909a4b757",
                "sha256:103a15f3ef0be9572beb5cfa945fe7692498ed2e36a395320e73ea728a171ec2",
                "sha256:8a13ac9ece631626ba70d16b5f718bf4bc4b6036288c752e0e605ed57d37f887",
                "sha256:62960d942fc296c280ad9144ba20db61d6062b05dd148c005868d3c88c2183dc"
            ]

```

It`s my origin Dockerfile, it worked fine at weeks ago:

```
FROM python:latest
RUN apk add --no-cache tzdata
ENV TZ Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
WORKDIR /usr/mabo/
COPY ./mabopython_requirements.txt ./ 
COPY ./simplecannet-0.0.1-py3-none-any.whl ./ 
RUN apk add --no-cache --virtual .build-deps gcc musl-dev curl 
RUN pip -V \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r mabopython_requirements.txt \
    && pip install --no-cache-dir simplecannet-0.0.1-py3-none-any.whl \
    && rm mabopython_requirements.txt \
    && rm simplecannet-0.0.1-py3-none-any.whl
```

The origin image is `python:3.7-alpine`.	(bb1ccaa5880c)

Today I use the newest python, it give me an error.	(f8aff02aba66)