import time
from typing import List, Union

import pymysql
from loguru import logger
from pydantic import BaseModel

# 数据库配置, 识别bit转bool
from onetools.decorator import log_traceback
from onetools.restful import HttpCode, process

converions = pymysql.converters.conversions
converions[pymysql.FIELD_TYPE.BIT] = lambda x: True if ord(x) else False


def get_mysql_connection(
    host: str, port: Union[str, int], user: str, password: str, database: str
):
    return pymysql.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        database=database,
        conv=converions,
        read_timeout=60,
        write_timeout=60,
    )


def get_limit(page: int, size: int) -> str:
    if page and size:
        skip = size * (page - 1)
        return f"limit {skip},{size}"
    return ""


def get_replace_list_sql(table: str, model_list: List[BaseModel]):
    items = []
    for model in model_list:
        old_item = model.dict() if isinstance(model, BaseModel) else model
        item = {}
        for k, v in old_item.items():
            if v is None:
                v = ""
            item[k] = v
        items.append(item)

    s = ["replace", "into"]

    if not items:
        logger.warning("No items to replace!")
        return ""

    # 单 key 时后面会多个逗号
    keys = tuple(items[0].keys())
    if len(keys) > 1:
        key = str(keys).replace("'", "")
        s.append(f"`{table}`{key}")
        s.append("value")
        value = [str(tuple(item.values())) for item in items]
    else:
        key = str(keys).replace("'", "").replace(",", "")
        s.append(f"`{table}`{key}")
        s.append("value")
        value = [str(tuple(item.values())).replace(",", "") for item in items]

    s.append(",".join(value))

    return " ".join(s).replace(" 'NULL'", " NULL")


def get_insert_list_sql(table: str, model_list: List[BaseModel]):
    items = []
    for model in model_list:
        old_item = model.dict() if isinstance(model, BaseModel) else model
        item = {}
        for k, v in old_item.items():
            if v is None:
                v = ""
            item[k] = v
        items.append(item)

    s = ["insert", "into"]

    if not items:
        logger.warning("No items to insert!")
        return ""

    # 单 key 时后面会多个逗号
    keys = tuple(items[0].keys())
    if len(keys) > 1:
        key = str(keys).replace("'", "")
        s.append(f"`{table}`{key}")
        s.append("value")
        value = [str(tuple(item.values())) for item in items]
    else:
        key = str(keys).replace("'", "").replace(",", "")
        s.append(f"`{table}`{key}")
        s.append("value")
        value = [str(tuple(item.values())).replace(",", "") for item in items]

    s.append(",".join(value))

    return " ".join(s)


def get_insert_sql(table: str, model: Union[dict, BaseModel], duplicate_keys=None):
    old_item = model.dict() if isinstance(model, BaseModel) else model
    item = {}
    for k, v in old_item.items():
        if v is None:
            continue
        item[k] = v

    s = ["insert", "into"]

    key = str(tuple(item.keys())).replace("'", "")
    s.append(f"`{table}`{key}")

    value = str(tuple(item.values()))
    s.append(f"value{value}")
    if duplicate_keys:
        s.append(f"on duplicate key update")
        for key in duplicate_keys:
            value = item[key]
            if isinstance(value, str):
                value = f"'{value}'"
            s.append(f"{key}={value}")
            s.append("and")
        else:  # 去除最后一个 and
            s.pop()

    return " ".join(s)


def get_replace_sql(table: str, model: Union[dict, BaseModel]):
    old_item = model.dict() if isinstance(model, BaseModel) else model
    item = {}
    for k, v in old_item.items():
        if v is None:
            continue
        item[k] = v

    s = ["replace", "into"]

    key = str(tuple(item.keys())).replace("'", "")
    s.append(f"`{table}`{key}")

    value = str(tuple(item.values()))
    s.append(f"value{value}")

    return " ".join(s)


def get_update_sql(
    table: str, data: Union[dict, BaseModel], update_data: Union[dict, BaseModel]
):
    item = data.dict() if isinstance(data, BaseModel) else data
    update_data = (
        update_data.dict() if isinstance(update_data, BaseModel) else update_data
    )

    s = ["UPDATE", table, "SET"]

    for key, value in update_data.items():
        if value is None:
            continue
        if isinstance(value, str):
            value = f"'{value}'" if value.lower() != "null" else f"null"
        s.append(f"{key}={value}")
        s.append(", ")
    else:  # 去除最后一个 and
        s.pop()

    s.append("WHERE")
    for key, value in item.items():
        if isinstance(value, str):
            value = f"'{value}'"
        s.append(f"{key}={value}")
        s.append("and")
    else:  # 去除最后一个 and
        s.pop()

    return " ".join(s)


def get_real_delete_sql(table: str, data: Union[dict, BaseModel]):
    item = data.dict() if isinstance(data, BaseModel) else data

    s = ["DELETE", "FROM", table, "WHERE"]

    for key, value in item.items():
        if isinstance(value, str):
            value = f"'{value}'"
        s.append(f"{key}={value}")
        s.append("and")
    else:  # 去除最后一个 and
        s.pop()

    return " ".join(s)


def get_delete_sql(table: str, data: Union[dict, BaseModel]):
    return get_update_sql(table, data, {"isDeleted": 1})


class MysqlEditor:
    def __init__(
        self, host: str, port: Union[str, int], user: str, password: str, database: str
    ):
        self.mysql = get_mysql_connection(
            host=host, port=port, user=user, password=password, database=database
        )

    def commit(self):
        self.mysql.ping()
        self.mysql.commit()
        return process("success")

    @log_traceback
    def insert_in_sql(
        self,
        table: str,
        data: Union[list, dict, BaseModel],
        duplicate_keys=None,
        log=True,
    ):
        self.mysql.ping()
        with self.mysql.cursor() as cursor:
            if isinstance(data, list):
                query = get_insert_list_sql(table, data)
            else:
                query = get_insert_sql(table, data, duplicate_keys)
            if log:
                logger.debug(f"MYSQL: {query}")
            cursor.execute(query)
        return self

    @log_traceback
    def delete_in_sql(self, table: str, data: Union[dict, BaseModel]):
        """软删除"""
        self.mysql.ping()
        with self.mysql.cursor() as cursor:
            query = get_delete_sql(table, data)
            logger.debug(f"MYSQL: {query}")
            cursor.execute(query)
        return self

    @log_traceback
    def real_delete_in_sql(self, table: str, data: Union[dict, BaseModel]):
        self.mysql.ping()
        with self.mysql.cursor() as cursor:
            query = get_real_delete_sql(table, data)
            logger.debug(f"MYSQL: {query}")
            cursor.execute(query)
        return self

    @log_traceback
    def replace_in_sql(
        self, table: str, data_list: List[Union[dict, BaseModel]], log=True
    ):
        self.mysql.ping()
        with self.mysql.cursor() as cursor:
            query = get_replace_list_sql(table, data_list)
            if log:
                logger.debug(f"MYSQL: {query}")
            cursor.execute(query)
        return self

    @log_traceback
    def replace_in_sql_single(self, table: str, key_list: list, values: tuple):
        self.mysql.ping()
        with self.mysql.cursor() as cursor:
            query = f'REPLACE into {table} ({",".join(key_list)}) VALUES ({",".join("%s" for i in key_list)})'
            cursor.execute(query, values)
        return self

    @log_traceback
    def real_delete_all_in_sql(self, table: str):
        """软删除"""
        self.mysql.ping()
        with self.mysql.cursor() as cursor:
            query = f"DELETE FROM {table}"
            logger.debug(f"MYSQL: {query}")
            cursor.execute(query)

    @log_traceback
    def update_in_sql(
        self,
        table: str,
        data: Union[dict, BaseModel],
        update_data: Union[dict, BaseModel],
        log=False,
    ):
        self.mysql.ping()
        with self.mysql.cursor() as cursor:
            query = get_update_sql(table, data, update_data)
            if log:
                logger.debug(f"MYSQL: {query}")
            cursor.execute(query)
        return self


class MysqlQuery:
    def __init__(
        self, host: str, port: Union[str, int], user: str, password: str, database: str
    ):
        self.mysql = get_mysql_connection(
            host=host, port=port, user=user, password=password, database=database
        )

    def commit(self):
        """如果查询的数据会变化，需要调用该方法进行更新"""
        self.mysql.ping()
        self.mysql.commit()

    def ping(self):
        self.mysql.ping()

    def query_total_in_sql(self, table: str, append=None) -> int:
        self.mysql.ping()
        with self.mysql.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            query = f"SELECT COUNT(1) as total FROM `{table}`"
            if append is None:
                pass
            else:
                query += append

            logger.debug(f"MYSQL: {query}")
            cursor.execute(query)
            data = cursor.fetchone()
            return data["total"]

    def execute_sql(self, query: str, log=True) -> dict:
        self.mysql.ping()
        with self.mysql.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            if log:
                logger.debug(f"{self.mysql.db=}, MYSQL: {query}")
            cursor.execute(query)
            query_data = cursor.fetchall()
            return query_data

    @log_traceback
    def get_data_in_sql(self, table: str, append: str = "", column: str = "") -> list:
        """不需要commit"""
        if not column:
            column = "*"
        self.mysql.ping()
        with self.mysql.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            query = f"SELECT {column} from `{table}` {append} "
            logger.debug(f"{self.mysql.db=}, MYSQL: {query}")
            cursor.execute(query)
            return cursor.fetchall()

    @log_traceback
    def get_single_data(
        self, table: str, append: str = "", column: str = "", log=False
    ):
        """不需要commit"""
        if not column:
            column = "*"
        self.mysql.ping()
        with self.mysql.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            query = f"SELECT {column} from `{table}` {append}"
            if log:
                logger.debug(f"MYSQL: {query}")
            cursor.execute(query)
            return cursor.fetchone()

    def get_list(
        self,
        table: str = None,
        page: int = "",
        limit: int = "",
        isDeleted: bool = None,
        sort: str = None,
        where: Union[str, list] = "",
    ) -> dict:
        """不需要commit"""
        self.mysql.ping()
        if where in [None, ""]:
            where = []

        elif isinstance(where, str):
            where = [where]

        if isDeleted is not None:
            where.append(f"isDeleted={int(isDeleted)}")

        where = " AND ".join(where)
        append = f"WHERE {where}" if where else ""

        # 控制排序
        if sort:
            order = "DESC" if sort[0] == "-" else "ASC"
            append += f" ORDER BY `{sort[1:]}` {order}"

        return self.get_data_in_sql_processed(table, page, limit, append)

    def get_data_in_sql_processed(
        self, table: str, page: int = "", size: int = "", append: str = "",
    ) -> dict:
        """不需要commit"""
        self.mysql.ping()
        with self.mysql.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            limit = get_limit(page, size)
            query = f"SELECT * from `{table}` {append} {limit} "
            try:
                logger.debug(f"{self.mysql.db=}, MYSQL: {query}")
                cursor.execute(query)
                query_data = cursor.fetchall()
                total = self.query_total_in_sql(table, append)
                data = {"total": total, "items": [i for i in query_data]}

                return process(data)
            except Exception as e:
                msg = e.args
                return process("error", msg, HttpCode.MYSQL_ERROR)
