# 支持多路径目录监控配置                                                                       

```
source_dir:网盘挂载本地资源路径（监控路径）                                            
dest_dir:strm保存路径（转移路径）                                                    
library_dir:媒体库容器内挂载路径                                                    
compatibility:                                                                  
    fast:性能模式，内部处理系统操作类型选择最优解;                                       
    compatibility:兼容模式，目录同步性能降低且NAS不能休眠，但可以兼容挂载的远程共享目录如SMB   
```
```
sync:
  monitor_confs: [
    {
      "source_dir": "/mnt/user/downloads/cloud/aliyun/emby",
      "dest_dir": "/mnt/user/downloads/link/aliyun",
      "library_dir": "/data/aliyun",
      "monitoring_mode": "compatibility"
    }
  ]

```

```
docker run -d --name alipan_strm \
    -v /mnt/user/downloads/:/mnt/user/downloads/ \
    -v /mnt/config.yaml:/mnt/config.yaml \
    thsrite/alipan-strm:latest
```

启动服务等一会再……

阿里云盘创建文件后，容器内监测有点延迟