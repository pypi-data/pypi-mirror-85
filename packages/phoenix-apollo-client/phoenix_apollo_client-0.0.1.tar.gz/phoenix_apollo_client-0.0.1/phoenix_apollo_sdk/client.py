import logging
import requests
import traceback
import time
import os
import json
from redis import StrictRedis, ConnectionPool


logger = logging.getLogger(__name__)

CACHE_PREFIX = os.environ.get("CACHE_PREFIX", "phoenix-apollo")
VERSION = os.environ.get("VERSION", "1")


class ApolloException(Exception):
    pass


class Client(object):

    def __init__(self, api_url):
        """
        :param api_url: phoenix api 地址
        """
        self.api_url = api_url
        self.redis_url = None
        self.redis_conn = None

    def init_config(self):
        """
            初始化配置
        :return:
        """
        logger.info("*** start init config")
        self.get_redis()

    def get_redis(self):
        if self.redis_conn:
            return self.redis_conn
        count = 0
        while count < 3:
            url = f"{self.api_url}/api/config/query/"
            try:
                response = requests.post(url)
                if not response.ok:
                    logger.error(f"apollo get redis url error {response.content}")
                    continue
                data = response.json()
                logger.info(f"apollo get redis url {data}")
                results = data.get("results", [])
                if results:
                    self.redis_url = results[0].get("address")
                    self.connect_redis(url=self.redis_url)
                    return self.redis_conn
                time.sleep(1)
            except Exception as e:
                logger.error(f"apollo get redis url error {traceback.format_exc()}")
                continue

    def connect_redis(self, url):
        pool = ConnectionPool.from_url(url)
        self.redis_conn = StrictRedis(connection_pool=pool)

    def get_redis_key(self, key):
        return "%s_%s" % (CACHE_PREFIX, key)

    def ab_check(self, key, customer_id="", site_id="", level=""):
        """
            a/b check
        :param key:
        :param customer_id:
        :param site_id:
        :param level:
        :return:
        """
        try:
            real_key = self.get_redis_key(key=key)
            self.get_redis()
            value = self.redis_conn.get(real_key)
            if value:
                data = json.loads(value)
                if data.get("all"):
                    logger.info(f"key {key} 全量放开")
                    return True
                if customer_id:
                    if data.get("customer_ids", []):
                        if customer_id in data.get("customer_ids", []):
                            logger.info(f"key {key} 当前用户: {customer_id} 放开")
                            return True
                if site_id:
                    if data.get("site_ids", []):
                        if site_id in data.get("site_ids", []):
                            logger.info(f"key {key} 当前节点: {site_id} 放开")
                            return True
                if level:
                    if data.get("levels", []):
                        if level in data.get("levels", []):
                            logger.info(f"key {key} 当前客户级别: {level} 放开")
                            return True
                return False
            else:
                return False
        except Exception as e:
            logger.error(f"get key {key} error {traceback.format_exc()}")
            return False

