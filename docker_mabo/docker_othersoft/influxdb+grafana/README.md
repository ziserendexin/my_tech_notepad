```
# 启动即可
docker-compose -f docker_server_influxdb.yaml up -d
```

配置文件放于根目录，telegraf没有用到。

influxdb使用的额是官方的默认配置文件。

两个container文件夹是用于给influx与grafana持续使用。



反正只是本地测试，做个记录，就不写得很详细了。