from typing import NamedTuple

from kazoo.client import KazooClient

from telecom_coworker.cache.big_cache import BigCache
from telecom_coworker.utils import set_interval


class TaskStats(NamedTuple):
    task_type: str
    payload_num: int
    total_num: int


class Stats(object):

    def __init__(self, big_cache: BigCache):
        self.big_cache = big_cache

    def payload_by_worker(self):
        assign_mapping = self.big_cache.assign_mapping()
        worker_infos = self.big_cache.worker_infos

        payload_by_w = dict()
        for w, info in worker_infos.items():
            current_handle_num = len(assign_mapping.get(w, set()))
            payload_by_w[w] = current_handle_num

        return payload_by_w

    def payload_by_task_type(self):
        assign_mapping = self.big_cache.assign_mapping()
        worker_infos = self.big_cache.worker_infos

        payload_by_t = dict()
        for w, info in worker_infos.items():
            current_handle_num = len(assign_mapping.get(w, set()))
            handle_type = info.get('handle_type', 'unknown')
            payload_by_t[handle_type] = payload_by_t.get(handle_type, 0) + current_handle_num

        return payload_by_t

    def payload_total(self):
        assign_mapping = self.big_cache.assign_mapping()
        return sum([len(tasks) for _, tasks in assign_mapping.items()])

    def workers_total_num(self):
        return len(self.big_cache.worker_infos)

    def tasks_total_num(self):
        return len(self.big_cache.tasks)

    def tasks_by_task_type(self):
        task_infos = self.big_cache.task_infos

        tasks_by_t = dict()
        for t, info in task_infos.items():
            task_type = info.get('task_type', 'unknown')
            tasks_by_t[task_type] = tasks_by_t.get(task_type, 0) + 1

        return tasks_by_t

    def task_stats(self):
        tasks_by_t = self.tasks_by_task_type()
        payload_by_t = self.payload_by_task_type()

        result = []
        for task_type, total_num in tasks_by_t.items():
            payload_num = payload_by_t.get(task_type, 0)
            ts = TaskStats(task_type, payload_num, total_num)
            result.append(ts)
        return result

    def task_type_list_need_more_workers(self):
        task_stats = self.task_stats()

        return [task_type for task_type, payload_num, total_num in task_stats if total_num > payload_num]

    def worker_stats(self):
        payload_by_w = self.payload_by_worker()

        result = {}
        for w, info in self.big_cache.worker_infos.items():
            payload = payload_by_w.get(w, 0)
            info['curr_handle_num'] = payload
            result[w] = info
        return result


if __name__ == '__main__':
    zk = KazooClient()
    zk.start()

    b = BigCache(zk, "basic")
    stats = Stats(b)


    def foo():
        print("-----------------------")
        print(f"payload_by_worker: {stats.payload_by_worker()}")
        print(f"payload_by_task_type: {stats.payload_by_task_type()}")
        print(f"payload_total: {stats.payload_total()}")
        print(f"workers_total_num: {stats.workers_total_num()}")
        print(f"tasks_total_num: {stats.tasks_total_num()}")
        print(f"tasks_by_task_type: {stats.tasks_by_task_type()}")
        print(f"task_stats: {stats.task_stats()}")
        print(f"worker_stats: {stats.worker_stats()}")
        print(f"task_type_list_need_more_workers: {list(stats.task_type_list_need_more_workers())}")


    set_interval(foo)
