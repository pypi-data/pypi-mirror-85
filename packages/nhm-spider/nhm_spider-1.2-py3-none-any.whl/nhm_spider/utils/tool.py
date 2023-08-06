import re
import time

from pymongo.database import Collection

from connection.mongo_connections import mongo
from nhm_spider.utils import date_to_timestamp, timestamp_to_date


def trans_cookies(ori, start=""):
    """
    转换webdriver.get_cookies获取的cookie格式
    """
    return {
        _["name"]: _["value"] for _ in ori
        if _["name"].startswith(start)
    }


def str_to_dict_cookie(string):
    cookies = {}
    for single in string.split("; "):
        key, value = single.split("=")
        cookies[key] = value
    return cookies


def gen_date_list(start_date, end_date, interval=86400):
    """
    根据开始时间和结束时间，按时间间隔切割时间段
    """
    format_string = "%Y-%m-%d"
    start_timestamp = date_to_timestamp(start_date, format_string)
    end_timestamp = date_to_timestamp(end_date, format_string)
    date_list = []
    for timestamp in range(start_timestamp, end_timestamp, interval):
        date_list.append(f"'{timestamp_to_date(timestamp, '%Y.%m.%d')}',"
                         f"'{timestamp_to_date(timestamp + interval - 1, '%Y.%m.%d')}'")
    return date_list


def to_mongo(table, item, unique_key=None):
    """存储原始数据到mongodb里"""
    if isinstance(table, Collection):
        collection = table
    else:
        database = mongo.connection[mongo.db_name]
        collection = database[table]
    if unique_key is None:
        filter_dict = {"uid": item["uid"]}
    else:
        filter_dict = {_: item[_] for _ in unique_key}
    db_data = collection.find_one(filter_dict)
    if not db_data:
        item["create_time"] = item["update_time"] = int(time.time())
        collection.insert_one(item)
    else:
        need_update_fields = {}
        for key in item:
            if key not in db_data or item[key] != db_data[key]:
                need_update_fields[key] = item[key]
        if need_update_fields:
            need_update_fields["update_time"] = int(time.time())
            collection.update_one(filter_dict, {"$set": need_update_fields})


def get_verify_code(message):
    """
    从格式化消息中提取验证码
    """
    return re.search(r"(?<=验证码：)\d{6}(?=（5分钟有效）)", message).group()
