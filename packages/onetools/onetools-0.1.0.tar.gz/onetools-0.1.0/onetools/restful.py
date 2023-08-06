from typing import Any


class HttpCode:
    OK = 20000

    ERROR = 40001

    MYSQL_ERROR = 40000
    LOGIN_ERROR = 60204

    ILLEGAL_TOKEN = 50008
    OTHER_CLIENTS = 50012
    TOKEN_EXPIRED = 50014


def process(data: Any = "", message: str = "success", code: int = HttpCode.OK):
    """处理return信息"""
    return {"code": code, "data": data, "message": message}
