background：

> https://stackoverflow.com/questions/19581059/misconf-redis-is-configured-to-save-rdb-snapshots

遇到

```
MISCONF Redis is configured to save RDB snapshots, but is currently not able to persist on disk. Commands that may modify the data set are disabled. Please check Redis logs for details about the error.
```

导致redis崩溃的问题。以做相关研究。

网络上的推荐的修改 etc/sysctl/xx.conf的方法，在docker镜像里面，找不到这个配置文件，及sysctl工具。估计需要重新构建其redis镜像才能解决这个。

aim：

- 持续化
- 尽量减少redis挂的可能性



redis配置，使用如下所示的docker内部环境：

```
redis:
    image: "redis:latest"   
    restart: always
    ports: 
      - "6379:6379"
#    command: redis-server --requirepass patac2016
    command: redis-server --appendonly yes --stop-writes-on-bgsave-error no
    volumes:
       - ./redis/data:/data
    environment: 
       TZ: 'Asia/Shanghai'
    networks: 
        back: 
            aliases: 
                - redis
```

测试虚拟机，分配内存1024，cpu1，硬盘20G。

1. 当存储数据达到500w条时，中间机down。

2. 在复原后，显示info中可以看出（全部info可以看附件）

   ```
       used_memory:2067296904		# 由 Redis 分配器分配的内存总量，以字节（byte）为单位
       used_memory_human:1.93G
       used_memory_rss:446636032	# 从操作系统的角度，返回 Redis 已分配的内存总量（俗称常驻集大小）。这个值和top 、 ps 等命令的输出一致。
       used_memory_rss_human:425.95M
       used_memory_peak:2075570736	# Redis 的内存消耗峰值（以字节为单位）
       used_memory_peak_human:1.93G
       used_memory_peak_perc:99.60%
       used_memory_overhead:860752
       used_memory_startup:786504
       used_memory_dataset:2066436152
       used_memory_dataset_perc:100.00%
       total_system_memory:1023934464
       total_system_memory_human:976.50M
       used_memory_lua:77824
       used_memory_lua_human:76.00K
       maxmemory:0
       maxmemory_human:0B
       maxmemory_policy:noeviction
       mem_fragmentation_ratio:0.22
       mem_allocator:jemalloc-4.0.3
       active_defrag_running:0
       lazyfree_pending_objects:0
   ```

   网络解释中可以看出，

   > https://blog.csdn.net/kexiaoling/article/details/51810919

   此时已经达到此redis处理性能的上限。

3. 因此需要对输入端进行限制，或者对输出端进行提升。

   但filebeat中，没有此类相关的限制。

   https://discuss.elastic.co/t/how-set-filebeat-output-logstash-speed-limit/43359

   filebeat建议从网络层对其进行限制。比如qos、emq之类的。

4. 使用如上配置，rm后，redis可以从aof中读取data。持续化ok。

5. 备份策略：

   aof：开启aof。

   rdb：

   **stop-writes-on-bgsave-error yes** ：此处设置为no，防止因为备份挂掉

   ​	默认情况下如果上面配置的RDB模式开启且最后一次的保存失败，redis 将停止接受写操作，让用户知道问题的发生。 

   ​	如果后台保存进程重新启动工作了，redis 也将自动的允许写操作。如果有其它监控方式也可关闭。 

6. 改进建议：

   - 在redis配置文件中设置**maxmemory** 、**maxmemory-policy noeviction** 、**maxmemory-samples** 的配置信息。

   - 同时redis记录慢查询日志，以做备份策略。

   - redis日志配置没有turn机制，因此日志输出到sys，由docker进行turn操作。
   - PS：**databases 16** ，设置数据库个数。默认数据库是 DB 0 。so，倩工，你不用担心db不够用了。

   则compose配置变为

   ```
   redis:
       image: "redis:latest"   
       restart: always
       ports: 
         - "6379:6379"
   #    command: redis-server --requirepass patac2016
       command: redis-server --appendonly yes --stop-writes-on-bgsave-error no --maxmemory 1374389534 --maxmemory-policy  volatile-ttl --maxmemory-samples 5 --slowlog-log-slower-than 10000 --databases 16
       volumes:
          - ./redis/data:/data
       environment: 
          TZ: 'Asia/Shanghai'
       networks: 
           back: 
               aliases: 
                   - redis
   ```

7. 再次进行压测

   1. 当数据量超限后，

      filebeat显示，数据上传失败：

      ```
      2018-08-24T12:44:40.004+0800    ERROR   pipeline/output.go:92   Failed to publish events: OOM command not allowed when used memory > 'maxmemory'.   
      ```

      按照filebeat的逻辑，这些数据会标记为未上传，等待处理完毕后才会继续上传。因此可以保证filebeat的收割的正确性。

   2. watchman会显示

      ```
      ERROR,channel:file_watcher,line_118: OOM command not allowed when used memory > 'maxmemory'.
      ```

      导致无法再次写入redis。

      此时陷入一个无法跳出的死循环。

      **这个要不传递到另外一个redis中？**

      

      但至少好消息是，这样可以保证filebeat收割器的稳定，并且加上这些配置，可以提高1倍以上的处理能力。

      

8. 其他建议：

   1. 中间机如果有redis，建议修改默认RDB备份为APO备份，虽然下降了一定重新加载的速度，但可以让数据量增加
   2. 如果中间机挂了，可以查看redis的状态，查看是否是因为redis的RDB或者是日志上限的问题。
   3. mts流程中，最大的限制是watchman，watchman处理速度很慢，导致数据挤压在filebeat-redis-watchman中，所以如果可以增加watchman的处理速度。(感觉无论怎么样都比不上filebeat，但也从另外一个角度说明了filebeat的处理速度是真的快)
   4. 当然如果filebeat收割上来的数据没那么大的话，以上都是废话。
   5. 可以考虑给filebeat配置一些设置，比如drop掉一些很久以前的日志，drop无意义日志。这样可以有效减少收割量。

   

​			      