import logging
import colorlog
import os
import websockets
import asyncio
from logging.handlers import QueueHandler, QueueListener

class LogManager:
    def __init__(self) -> None:
        pass

    def GetLogger(self,log_name: str = "default", out_to_console:bool = True, web_log_mode: bool = False, post_url: str = ""):
        # 确保日志名称有效
        log_name = log_name if log_name else "default"
        if out_to_console == True:
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

        console_handler = logging.StreamHandler()
        if out_to_console == True:
            file_handler = logging.FileHandler(filename=f'logs/{log_name}/{log_name}.log', mode='a', encoding='utf-8')
            queue: asyncio.Queue = asyncio.Queue()
            queue_handler = QueueHandler(queue)
            queue_listener = QueueListener(queue, file_handler)

        logger.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)
        if out_to_console == True:
            file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            fmt='%(asctime)s.%(msecs)03d | %(levelname)-8s | %(filename)s:%(lineno)d | %(name)s | %(funcName)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s %(asctime)s.%(msecs)03d | %(levelname)-8s | %(filename)s:%(lineno)d | %(name)s | %(funcName)s | %(message)s %(reset)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors=log_color_config
        )
        console_handler.setFormatter(console_formatter)
        if out_to_console == True:
            file_handler.setFormatter(formatter)

        if not logger.handlers:
            # 检查代码是否在异步环境中运行
            if asyncio.iscoroutinefunction(logging.Handler.emit):
                logger.addHandler(queue_handler)
                asyncio.ensure_future(queue_listener.start())
            else:
                logger.addHandler(console_handler)
                if out_to_console == True:
                    logger.addHandler(file_handler)

        logger.addHandler(console_handler)
        if out_to_console == True:
            logger.addHandler(file_handler)

        if web_log_mode and post_url:
            websocket_handler = WebsocketHandler(post_url)
            websocket_handler.setLevel(logging.INFO)
            websocket_handler.setFormatter(formatter)
            logger.addHandler(websocket_handler)

        return logger

class WebsocketHandler(logging.Handler):
    def __init__(self, server_address):
        super().__init__()
        self.server_address = server_address
    
    async def send_log_async(self, message):
        async with websockets.connect(self.server_address) as websocket:
            await websocket.send(message)
    
    def send_log_sync(self, message):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send_log_async(message))

    def emit(self, record):
        log_entry = self.format(record)
        
        if asyncio.get_event_loop().is_running():
            asyncio.create_task(self.send_log_async(log_entry))
        else:
            try:
                self.send_log_sync(log_entry)
            except Exception as e:
                logging.warning("Failed to send log synchronously: %s", e)

if __name__ == '__main__':
    log_manager = LogManager()
    logger = log_manager.GetLogger(log_name='example')
    logger.info('这是一个成功信息')
    logger.debug('这是一个调试信息')
    logger.critical('这是一个严重错误信息')
    logger.error('这是一个错误信息')
    logger.warning('这是一个警告信息')