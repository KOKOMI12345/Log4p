
# Log4p日志库

## 描述

这是一个可以支持异步记录日志,发送到websocket服务器,同时配置简单,它还实现了识别代码异步和同步的环境
以支持不同环境下的日志记录

### 示例用法

```python
from Log4p import LogManager

logger = LogManager().GetLogger(
    log_name='example',
    out_to_console=True,
    web_log_mode=True,
    post_url='ws://localhost:8765'
)

logger.info('这是一个成功信息')
logger.debug('这是一个调试信息')
logger.critical('这是一个严重错误信息')
logger.error('这是一个错误信息')
logger.warning('这是一个警告信息')
```

### 参数介绍

-`log_name`: 指定日志记录器的名称
-`out_to_console`: 是否输出到控制台,默认true
-`web_log_mode`:是否启用websocket日志输出模式,默认false
-`post_url`: 如果启用上述模式,则传入post_url,否则不管,默认None
