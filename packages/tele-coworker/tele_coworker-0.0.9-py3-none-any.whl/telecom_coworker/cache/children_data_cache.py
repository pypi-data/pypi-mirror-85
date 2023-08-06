import json
from json import JSONDecodeError

from kazoo.client import KazooClient

from telecom_coworker import log


class ChildrenDataCache(object):

    def __init__(self, zk: KazooClient, path: str, added_func=None, lost_func=None):
        self.zk = zk
        self.path = path

        self.children = set(self.zk.get_children(path))

        self._data_map = dict()
        self.added_func = added_func
        self.lost_func = lost_func

        self.zk.ChildrenWatch(path, self._watch)

    def _watch(self, next_children):
        self.children = set(next_children)
        loaded_children = set(self._data_map.keys())

        added_children = self.children - loaded_children
        for child in added_children:
            data_bytes, _ = self.zk.get(f"{self.path}/{child}")
            try:
                data = json.loads(data_bytes.decode('utf-8'))
                self._data_map[child] = data
            except JSONDecodeError as e:
                log.exception(f"load data<{self.path}/{child}> failed: check it")

        if len(added_children) > 0 and self.added_func is not None:
            self.added_func(added_children)

        lost_children = loaded_children - self.children
        for child in lost_children:
            if child in self._data_map:
                self._data_map.pop(child)

        if len(lost_children) > 0 and self.lost_func is not None:
            self.lost_func(lost_children)

    @property
    def data(self):
        return self._data_map

    def clear(self):
        for child in list(self._data_map.keys()):
            self.zk.delete(f"{self.path}/{child}")


if __name__ == '__main__':
    from telecom_coworker.utils import set_interval

    zk = KazooClient()
    zk.start()

    cache = ChildrenDataCache(zk, "/basic/messages")


    def foo():
        print("==============start=============")
        print(cache.data)
        print(len(cache.data))
        print("==============end=============")


    set_interval(foo)
