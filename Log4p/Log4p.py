import logging
import colorlog
import os
from Log4p.websocketHander import WebsocketHandler
import asyncio
from Log4p.HttpHander import HTTPhandler , AsyncHTTPhandler
class LogManager:
    def __init__(self) -> None:
        pass

    def GetLogger(self, log_name: str = "default",
                  out_to_console: bool = True,
                  web_log_mode: bool = False,
                  WSpost_url: str = "",
                  HTTPpost_url: str = "",
                  http_mode: bool = False):
        # 确保日志名称有效
        log_name = log_name if log_name else "default"
        if out_to_console:
            log_folder = f'./logs/{log_name}'
            if not os.path.exists(log_folder):
                os.makedirs(log_folder, exist_ok=True)

        logger = logging.getLogger(log_name)
        if logger.hasHandlers():
            # Logger已经配置过处理器，避免重复配置
            return logger

        # 颜色配置
        log_color_config = {
            'DEBUG': 'bold_blue', 'INFO': 'bold_cyan',
            'WARNING': 'bold_yellow', 'ERROR': 'red',
            'CRITICAL': 'bold_red', 'RESET': 'reset',
            'asctime': 'green'
        }
        if out_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_formatter = colorlog.ColoredFormatter(
                fmt='%(log_color)s %(asctime)s.%(msecs)03d | %(levelname)-8s | %(filename)s:%(lineno)d | %(name)s | %(funcName)s | %(message)s %(reset)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors=log_color_config
            )
            console_handler.setFormatter(console_formatter)

            logger.setLevel(logging.DEBUG)
            logger.addHandler(console_handler)

        file_handler = logging.FileHandler(
            filename=f'logs/{log_name}/{log_name}.log', mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            fmt='%(asctime)s.%(msecs)03d | %(levelname)-8s | %(filename)s:%(lineno)d | %(name)s | %(funcName)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)

        # 检查代码是否在异步环境中运行
        if asyncio.iscoroutinefunction(logging.Handler.emit):
            logger.addHandler(file_handler)
        else:
            logger.addHandler(file_handler)

        if web_log_mode and WSpost_url:
            websocket_handler = WebsocketHandler(WSpost_url)
            websocket_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                fmt='%(asctime)s.%(msecs)03d | %(levelname)-8s | %(filename)s:%(lineno)d | %(name)s | %(funcName)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            websocket_handler.setFormatter(formatter)
            logger.addHandler(websocket_handler)

        if http_mode and HTTPpost_url:
            # 检查代码是否在异步环境中运行
            if asyncio.iscoroutinefunction(logging.Handler.emit):
                async_http_hander = AsyncHTTPhandler(HTTPpost_url)
                async_http_hander.setLevel(logging.INFO)
                formatter = logging.Formatter(
                    fmt='%(asctime)s.%(msecs)03d | %(levelname)-8s | %(filename)s:%(lineno)d | %(name)s | %(funcName)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                async_http_hander.setFormatter(formatter)
                logger.addHandler(async_http_hander)
            http_handler = HTTPhandler(HTTPpost_url)
            http_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                fmt='%(asctime)s.%(msecs)03d | %(levelname)-8s | %(filename)s:%(lineno)d | %(name)s | %(funcName)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            http_handler.setFormatter(formatter)
            logger.addHandler(http_handler)

        return logger


if __name__ == '__main__':
    logger = LogManager().GetLogger(log_name='example')
    logger.info('这是一个成功信息')
    logger.debug('这是一个调试信息')
    logger.critical('这是一个严重错误信息')
    logger.error('这是一个错误信息')
    logger.warning('这是一个警告信息')