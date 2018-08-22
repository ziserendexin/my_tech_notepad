```
version: "3"
services:

  proxy:
    build: ./proxy
    networks:
      - frontend
      - default_network
  app:
    build: ./app
    ports: 	# 暴露端口
      - "6379:6379"
    networks:
      - frontend
      - backend
  db:
    image: postgres
    networks:
      - backend: 
      	aliases: 
      		- postgres	# 设置别名
      - default_network

networks:
  backend:
    # 使用一个现有网络并设置一些乱七八糟的东西
    driver: custom-driver-2
    driver_opts:
      foo: "abcd"
      bar: "efgh"
  default_network: # 活着干脆什么都不做，使用其自定义的网络。
  create_sbname_network: 	# 建一个sbname的网络
  	name: sbname
  frontend:
    # 使用一个现有的sbname网络
    driver: sbname
```

我也知道，太长难看。

- 使用ports，暴露端口。
- 使用networks设定几个组。
- 也可以在network中设置当前app的别名。
- 不同网络注意互相隔离。