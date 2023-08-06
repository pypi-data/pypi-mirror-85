import sys
import time
import traceback
from functools import wraps

from loguru import logger


def singleton(cls):
    """实现单例模式的装饰器"""
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)

        return instances[cls]

    return getinstance


def log_traceback(func):
    def decorator(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception:
            _, value, tb = sys.exc_info()
            msg = []
            for line in traceback.TracebackException(type(value), value, tb).format(
                chain=True
            ):
                msg.append(line)
            raise logger.error("".join(msg))
        return result

    return decorator


def log_time(name):
    def decorator(func):
        def int_time(*args, **kwargs):
            start_time = time.time()  # 程序开始时间
            result = func(*args, **kwargs)
            over_time = time.time()  # 程序结束时间
            total_time = over_time - start_time
            if total_time > 60:
                logger.info(f"Total {name} Time: {total_time / 60:.2f}min")
            else:
                logger.info(f"Total {name} Time：{total_time:.2f}s")
            return result

        return int_time

    return decorator
