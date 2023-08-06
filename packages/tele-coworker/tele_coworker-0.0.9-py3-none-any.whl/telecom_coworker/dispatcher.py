"""Dispatcher run

Usage:
  dispatcher.py NAMESPACE ZK_HOSTS
"""
import json
import time
from collections import defaultdict, Counter
from datetime import datetime
from functools import reduce
from reprlib import repr

import click
import numpy as np
from kazoo.client import KazooClient

from telecom_coworker import log
from telecom_coworker.cache.big_cache import BigCache
from telecom_coworker.kazoo_helper import KazooHelper
from telecom_coworker.models import TaskState, STATE_EXITED, STATE_RUNNING, RecordTuple, Task, WorkerInfo
from telecom_coworker.utils import search_dict_by_keys


class Dispatcher(object):

    def __init__(self, namespace, hosts="localhost:2181"):
        self.namespace = namespace
        self.zk = KazooClient(hosts=hosts)
        self.namespace = namespace
        self.cache: BigCache = None

        self.changed = True

        self.helper: KazooHelper = None

    def _watch_tasks(self, next_tasks):
        self.changed = True

    def _watch_workers(self, next_workers):
        self.changed = True

    def _master_func(self):
        log.info("I ready to by a good dispatcher")
        self.cache = BigCache(self.zk, self.namespace,
                              canceled_tasks_handle_func=self.canceled_tasks_handle,
                              lost_workers_handle_func=self.lost_workers_handle,
                              added_tasks_handle_func=self.added_tasks_handle,
                              added_workers_handle_func=self.added_workers_handle)

        self._assign_mapping = self.cache.assign_mapping()

        # self.zk.ChildrenWatch(f"{self.namespace}/tasks")(self._watch_tasks)
        # self.zk.ChildrenWatch(f"{self.namespace}/workers")(self._watch_workers)

        while True:
            # self.handle_messages()
            self.assign_task_if_needed()
            time.sleep(2)

    def assign_task_if_needed(self):
        log.info("==> assign_task_if_needed")
        if self.changed:
            self.assign_tasks()
            self.changed = False

    def canceled_tasks_handle(self, canceled_tasks):
        self.changed = True
        log.info(f"canceled tasks[size: {len(canceled_tasks)}]: {repr(canceled_tasks)}")
        unassign_worker_task = search_dict_by_keys(self._assign_mapping, canceled_tasks)
        self._unassign_tasks(unassign_worker_task)

    def lost_workers_handle(self, lost_workers):
        self.changed = True
        log.info(f"lost workers[size: {len(lost_workers)}]: {repr(lost_workers)}")
        self._unassign_workers(lost_workers)

    def added_workers_handle(self, added_workers):
        self.changed = True
        log.info(f"added workers[size:{len(added_workers)}]: {repr(added_workers)}")

    def added_tasks_handle(self, added_tasks):
        self.changed = True
        log.info(f"added tasks[size: {len(added_tasks)}]: {repr(added_tasks)}")

    def assign_tasks(self):
        log.info("@_@ start assign tasks")
        assigned_tasks = reduce(lambda s1, s2: s1 | s2, self._assign_mapping.values(), set())
        unassigned_tasks = self.cache.tasks - assigned_tasks

        task_infos_by_type = defaultdict(list)
        for ut in unassigned_tasks:
            task_infos_by_type[self.cache.task_infos[ut]["task_type"]].append(self.cache.task_infos[ut])

        assign_count = {w: len(tasks) for w, tasks in self._assign_mapping.items()}

        worker_infos_by_type = defaultdict(list)
        for w in self.cache.worker_infos.values():
            worker_infos_by_type[w["handle_type"]].append(w)

        for task_type in task_infos_by_type:
            tasks = task_infos_by_type[task_type]

            valid_worker_resources = Counter(
                {w['wid']: max(w.get("max_handle_num", 2) - assign_count.get(w['wid'], 0), 0) for w in
                 worker_infos_by_type[task_type]})

            num = min(sum(valid_worker_resources.values()), len(tasks))
            selected_worker_ids = np.random.choice(list(valid_worker_resources.elements()), num, replace=False)
            selected_workers = [self.cache.worker_infos.get(wid) for wid in selected_worker_ids]

            for t, w in zip(tasks, selected_workers):
                wid = w['wid']
                self.assign_task_to_worker(t, wid)
                self._do_assign_record(w, t)
                assign_count[wid] = assign_count.get(wid, 0) + 1

    def assign_task_to_worker(self, task: Task, worker_id: str):
        tid = task["tid"]
        log.info("assign task %s to worker: %s", tid, worker_id)
        task_content = json.dumps(task).encode("utf-8")
        self.zk.create(f"{self.namespace}/assign/{worker_id}/{tid}", task_content, makepath=True)
        self._assign_mapping[worker_id].add(tid)

    def _do_assign_record(self, worker: WorkerInfo, task: Task):
        r = RecordTuple('assign', worker['wid'], worker['hostip'], task["tid"], task['task_type'],
                        datetime.utcnow().isoformat())
        self.helper.add_record(r)

    def _do_unassign_record(self, worker_id: str, task_id: str):
        worker_info: WorkerInfo = self.cache.worker_infos.get(worker_id, {})
        # task_info be pop, replace by worker_info['handle_type']
        task_type = worker_info['handle_type']
        r = RecordTuple('unassign', worker_id, worker_info.get('hostip', 'unknwon'), task_id, task_type,
                        datetime.utcnow().isoformat())
        self.helper.add_record(r)

    def _unassign_tasks(self, worker_task_map: defaultdict):
        for w, tasks in worker_task_map.items():
            log.info("unassign task: %s by worker: %s", tasks, w)

            for t in tasks:
                self.zk.delete(f"{self.namespace}/assign/{w}/{t}")
                self._assign_mapping[w].discard(t)

                self._do_unassign_record(w, t)

    def _unassign_workers(self, workers):
        for w in workers:
            w_tasks = self._assign_mapping[w]

            for task in w_tasks:
                state: TaskState = self.helper.get_task_state(task)

                if state['state'] == STATE_RUNNING:
                    exited_task_state = TaskState(tid=task, state=STATE_EXITED, exitcode=-15)
                    self.helper.update_task_state(task, exited_task_state)
                    self._do_terminate_record(w, task)

                self.zk.delete(f"{self.namespace}/assign/{w}", recursive=True)
            if w in self._assign_mapping:
                self._assign_mapping.pop(w)

    def _do_terminate_record(self, wid, tid):
        task_info: Task = self.cache.task_infos.get(tid)
        r = RecordTuple('terminate', wid, 'unknown', tid, task_info['task_type'],
                        datetime.utcnow().isoformat())
        self.helper.add_record(r)

    def _ensure_base_node(self):
        self.zk.ensure_path(f"{self.namespace}/tasks")
        self.zk.ensure_path(f"{self.namespace}/workers")
        self.zk.ensure_path(f"{self.namespace}/assign")
        self.zk.ensure_path(f"{self.namespace}/messages")
        # self.zk.ensure_path(f"{self.namespace}/failed_tasks")

    def run(self):
        self.zk.start()
        self._ensure_base_node()
        self.helper = KazooHelper(self.zk, self.namespace)

        election = self.zk.Election(f"{self.namespace}/master", "my-identifier")
        election.run(self._master_func)

    def inspect(self):
        log.info(f"assign cache: {self._assign_mapping}")

    def handle_messages(self):
        pass


@click.command()
@click.argument("namespace")
@click.argument("zk_hosts")
def main(namespace, zk_hosts):
    from telecom_coworker.log import setup_logging
    setup_logging()

    dispatcher = Dispatcher(namespace, zk_hosts)
    dispatcher.run()


if __name__ == '__main__':
    main()
