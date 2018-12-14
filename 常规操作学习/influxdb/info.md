1. 名词

   | [database](https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/#database)数据库 | [field key](https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/#field-key) 更类似于键值 | [field set](https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/#field-set) 键值与数据的hash集 |
   | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
   | [field value](https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/#field-value)字段值 | [measurement](https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/#measurement) 表 | [point](https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/#point) |
   | [retention policy](https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/#retention-policy) 保留策略 | [series](https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/#series) | [tag key](https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/#tag-key) |
   | [tag set](https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/#tag-set) | [tag value](https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/#tag-value) | [timestamp](https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/#timestamp) 时间 |

   当然，influx说，fileds的作用只是value。

   使用字段值作为过滤器的查询，会扫描所有与查询中其他条件匹配的值。所以，这种查询的性能并不好。通常，字段不应包含常用查询元数据。

   tag，标签，tag会将所有tag value 组成不同的组合。tag会建立索引，所以应该包含常用元数据。

   measurement作为所有tags、fields、time的容器，同时，其名字，是对数据关于相关fields的描述。
