import json
from collections import defaultdict
from json import JSONDecodeError

from kazoo.client import KazooClient

from telecom_coworker import log
from telecom_coworker.models import WorkerInfo, Task


class BigCache(object):

    def __init__(self, zk: KazooClient, namespace,
                 added_tasks_handle_func=None,
                 canceled_tasks_handle_func=None,
                 lost_workers_handle_func=None,
                 added_workers_handle_func=None
                 ):
        self.zk = zk
        self.namespace = namespace
        self.workers = set(self.zk.get_children(f"{self.namespace}/workers"))
        self.tasks = set(self.zk.get_children(f"{self.namespace}/tasks"))

        self.worker_infos = dict()
        self.task_infos = dict()

        self.added_tasks_handle_func = added_tasks_handle_func
        self.canceled_tasks_handle_func = canceled_tasks_handle_func
        self.lost_workers_handle_func = lost_workers_handle_func
        self.added_workers_handle_func = added_workers_handle_func

        self.zk.ChildrenWatch(f"{self.namespace}/tasks")(self._watch_tasks)
        self.zk.ChildrenWatch(f"{self.namespace}/workers")(self._watch_workers)

    def _watch_workers(self, next_workers):
        self.workers = set(next_workers)
        loaded_infos = set(self.worker_infos.keys())

        added_workers = self.workers - loaded_infos
        for w in added_workers:
            worker_info, _ = self.zk.get(f"{self.namespace}/workers/{w}")
            try:
                w_info: WorkerInfo = json.loads(worker_info.decode('utf-8'))
                self.worker_infos[w] = w_info
            except JSONDecodeError as e:
                log.exception(f"load worker<{w}> failed: check it")

        if len(added_workers) > 0 and self.added_workers_handle_func is not None:
            self.added_workers_handle_func(added_workers)

        lost_workers = loaded_infos - self.workers
        for w in lost_workers:
            if w in self.worker_infos:
                self.worker_infos.pop(w)

        if len(lost_workers) > 0 and self.lost_workers_handle_func is not None:
            self.lost_workers_handle_func(lost_workers)

    def _watch_tasks(self, next_tasks):
        self.tasks = set(next_tasks)
        loaded_tasks = set(self.task_infos.keys())

        added_tasks = self.tasks - loaded_tasks
        for t in added_tasks:
            task_info, _ = self.zk.get(f"{self.namespace}/tasks/{t}")
            try:
                t_info: Task = json.loads(task_info.decode('utf-8'))
                self.task_infos[t] = t_info
            except JSONDecodeError as e:
                log.exception(f"load task<{t}> failed: check it")

        if len(added_tasks) > 0 and self.added_tasks_handle_func is not None:
            self.added_tasks_handle_func(added_tasks)

        canceled_tasks = loaded_tasks - self.tasks
        for t in canceled_tasks:
            if t in self.task_infos:
                self.task_infos.pop(t)

        if len(canceled_tasks) > 0 and self.canceled_tasks_handle_func is not None:
            self.canceled_tasks_handle_func(canceled_tasks)

    def assign_mapping(self):
        m = defaultdict(set)

        assigned_workers = self.zk.get_children(f"{self.namespace}/assign")
        valid_assigned_workers = {w for w in assigned_workers if w in self.workers}

        for w in valid_assigned_workers:
            assign_tasks = self.zk.get_children(f"{self.namespace}/assign/{w}")
            for task in assign_tasks:
                m[w].add(task)

        return m


def l_tasks(lost_tasks):
    print(f"lost tasks ==> {lost_tasks}")


def a_tasks(added_tasks):
    print(f"added tasks ==> {added_tasks}")


if __name__ == '__main__':
    from telecom_coworker.utils import set_interval

    zk = KazooClient()
    zk.start()

    big_cache = BigCache(zk, "basic", added_tasks_handle_func=a_tasks, canceled_tasks_handle_func=l_tasks)


    def foo():
        print(f"tasks: {big_cache.tasks}")
        print(f"tasks: {big_cache.workers}")
        print(f"assign: {big_cache.assign_mapping()}")
        print("--------------------")
        print(f"task infos: {big_cache.task_infos}")
        print("--------------------")
        print(f"worker infos: {big_cache.worker_infos}")
        print("--------------------")


    set_interval(foo)
