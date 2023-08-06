import atexit
import json
import os
from datetime import datetime
from json import JSONDecodeError
from time import time
from uuid import uuid4 as uuid

from kazoo.client import KazooClient

from telecom_coworker import log, TASK_RETRIES_MAX_NUM
from telecom_coworker.kazoo_helper import KazooHelper
from telecom_coworker.models import WorkerInfo, Task, TaskState, STATE_RUNNING, STATE_EXITED, STATE_FATAL, \
    STATE_PENDING, RecordTuple
from telecom_coworker.utils import get_hostip, get_hostname, set_interval, Process

ip = get_hostip()


class Coworker(object):
    def __init__(self, namespace, hosts="localhost:2181", worker_id=None):
        self.namespace = namespace
        self.zk = KazooClient(hosts=hosts)
        self.helper = None
        self.worker_id = worker_id if worker_id is not None else f"worker-{uuid()}"

        self._current_task_ids = set()
        self._current_task_infos = dict()
        self._current_task_processes = dict()
        self._task_states = dict()  # {tid: state}

    def run(self, handle_type, handle_num, func):
        self.zk.start()
        self.zk.ensure_path(f"{self.namespace}/assign/{self.worker_id}")
        log.info("***************************************************************")
        log.info(f"*** worker ID: {self.worker_id} ***")
        log.info("***************************************************************")

        self.helper = KazooHelper(self.zk, self.namespace)

        @self.zk.ChildrenWatch(f"{self.namespace}/assign/{self.worker_id}")
        def watch_assign_task(children):
            next_tasks_ids = set(children)

            canceled_task_ids = self._current_task_ids - next_tasks_ids
            self.handle_canceled_tasks(canceled_task_ids)

            added_task_ids = next_tasks_ids - self._current_task_ids
            self.handle_added_tasks(added_task_ids, func)

            self._current_task_ids = next_tasks_ids

        worker_info = WorkerInfo(wid=self.worker_id, handle_type=handle_type, max_handle_num=handle_num,
                                 hostname=get_hostname(), hostip=ip,
                                 pid=os.getpid())
        self.zk.create(f"{self.namespace}/workers/{self.worker_id}",
                       json.dumps(worker_info).encode("utf-8"), ephemeral=True)

        atexit.register(self.close)

        set_interval(self.check_subprocess, interval=5, func2=func)

    def close(self):
        if self.zk and self.zk.connected:
            self.zk.stop()
            self.zk.close()

    def handle_canceled_tasks(self, canceled_task_ids):
        log.info(f"handle canceled tasks: {canceled_task_ids}")
        for tid in canceled_task_ids:
            process = self._current_task_processes.get(tid)
            log.info(f"KILL task process: {process.ident}")
            if process:
                process.kill()

                self._current_task_processes.pop(tid)
                self._current_task_infos.pop(tid)

    def handle_added_tasks(self, added_task_ids, func):
        log.info(f"handle added tasks {added_task_ids}")
        for tid in added_task_ids:
            p = self.up_task_process(tid, func)
            state: TaskState = TaskState(tid=tid, state=STATE_RUNNING, ip=ip, pid=p.pid)
            self.update_task_state(tid, state)

    def up_task_process(self, task_id, func):
        task: Task = self._current_task_infos.get(task_id)
        if task is None:
            try:
                task_content, _ = self.zk.get(f"{self.namespace}/assign/{self.worker_id}/{task_id}")
                task = json.loads(task_content.decode('utf-8'))
            except JSONDecodeError as e:
                log.error(e.msg, stack_info=True)

        if task is None:
            return None

        process = Process(target=func, kwargs=task["params"])
        process.start()
        log.info(f"TASK[{task}] run on PID: {process.ident}")

        self._current_task_infos[task_id] = task
        self._current_task_processes[task_id] = process

        return process

    def check_subprocess(self, func2):
        for tid, p in self._current_task_processes.items():
            task_state = dict(self._task_states.get(tid, TaskState(tid=tid, state=STATE_PENDING)))
            task_state['ip'] = ip

            if not p.is_alive():
                traceback = None
                if p.exception:
                    _, traceback = p.exception
                task_state['state'] = STATE_EXITED
                task_state['exitcode'] = p.exitcode
                task_state['logs'] = traceback

                if len(task_state.get('retries', list())) > TASK_RETRIES_MAX_NUM:
                    task_state['state'] = STATE_FATAL
                else:
                    new_process = self.up_task_process(tid, func2)

                    task_state['state'] = STATE_RUNNING
                    task_state['pid'] = new_process.pid
                    retries = task_state.get('retries', list())
                    retries.append(time())
                    task_state['retries'] = retries

                if self._task_states.get(tid) is None or self._task_states[tid] != task_state:
                    self.update_task_state(tid, task_state)
                    self._task_states[tid] = task_state

    def update_task_state(self, tid, task_state: TaskState):
        state = TaskState(**task_state)
        self.helper.update_task_state(tid, state)

        if state['state'] == STATE_FATAL:
            task: Task = self._current_task_infos.get(tid)
            dt = datetime.now().isoformat()
            record = RecordTuple("failed", self.worker_id, ip, tid, task['task_type'], dt, state['logs'])
            self.helper.add_record(record)
            # msg_content = f"ERROR: {state.get('logs', '')}"
            # msg = Message('failed_task'.upper(), tid, self.worker_id, msg_content)
            # self.helper.send_message(msg)
