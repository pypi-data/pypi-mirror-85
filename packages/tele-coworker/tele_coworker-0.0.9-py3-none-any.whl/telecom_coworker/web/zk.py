from flask import current_app, g
from kazoo.client import KazooClient

from telecom_coworker.cache.big_cache import BigCache
from telecom_coworker.cache.children_data_cache import ChildrenDataCache
from telecom_coworker.kazoo_helper import KazooHelper
from telecom_coworker.web.stats import Stats


def _get_kazoo_client():
    zk_hosts = current_app.config['ZK_HOSTS']
    zk = KazooClient(zk_hosts)
    zk.start()

    return zk


def client() -> KazooClient:
    if "client" not in g:
        g.client = _get_kazoo_client()
    return g.client


def kazoo_helper() -> KazooHelper:
    if "zk_helper" not in g:
        zk = client()
        zk_namespace = current_app.config['ZK_NAMESPACE']
        g.zk_helper = KazooHelper(zk, zk_namespace)

    return g.zk_helper


def big_cache() -> BigCache:
    if "big_cache" not in g:
        zk = client()
        zk_namespace = current_app.config['ZK_NAMESPACE']
        g.big_cache = BigCache(zk, zk_namespace)
    return g.big_cache


def stats():
    if "stats" not in g:
        cache = big_cache()
        g.stats = Stats(cache)
    return g.stats


def msg_handler():
    if "msg_handler" not in g:
        zk = client()
        zk_namespace = current_app.config['ZK_NAMESPACE']
        g.msg_handler = ChildrenDataCache(zk, f"/{zk_namespace}/messages")
    return g.msg_handler
