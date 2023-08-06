import json
from datetime import datetime
from uuid import uuid4 as uuid

from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError, NotEmptyError
from kazoo.recipe.queue import Queue

from telecom_coworker import log
from telecom_coworker.models import Task, TaskState, STATE_PENDING, Message, RecordTuple


class KazooHelper(object):
    def __init__(self, zk: KazooClient, namespace):
        self.zk = zk
        self.namespace = namespace
        self.zk.ensure_path(f"{namespace}/records")
        self.records_queue = Queue(zk, f"{namespace}/records")

    def add_task(self, task_type, task_id=None, **params):
        tid = task_id if task_id is not None else str(uuid())
        task: Task = {"tid": tid, "task_type": task_type, "params": params}
        self.zk.create(f"{self.namespace}/tasks/{tid}", json.dumps(task).encode("utf-8"))
        return tid

    def cancel_task(self, task_id):
        try:
            self.zk.delete(f"{self.namespace}/tasks/{task_id}", recursive=True)
            return True
        except (NoNodeError, NotEmptyError) as e:
            log.exception("cancel task failed, ERROR:%s", e)
            return False

    def get_task_state(self, task_id):
        try:
            state_str, _ = self.zk.get(f"{self.namespace}/tasks/{task_id}/state")
            state: TaskState = json.loads(state_str.decode('utf-8'))
        except NoNodeError as e:
            if self.zk.exists(f"{self.namespace}/tasks/{task_id}"):
                state = TaskState(tid=task_id, state=STATE_PENDING)
                return state
            raise e

        return state

    def update_task_state(self, task_id, task_state: TaskState):
        state: TaskState = TaskState(**task_state)
        state['updated_at'] = datetime.now().isoformat()
        log.info(f"task[{task_id}] state changed: => {state}")
        if self.zk.exists(f"{self.namespace}/tasks/{task_id}") is not None:
            self.zk.ensure_path(f"{self.namespace}/tasks/{task_id}/state")
            self.zk.set(f"{self.namespace}/tasks/{task_id}/state", json.dumps(state).encode("utf-8"))
        else:
            log.warning(f"task[{task_id} update state: {task_state}, but it not exists]")

    def send_message(self, msg: Message):
        self.zk.create(f"{self.namespace}/messages/msg-", json.dumps(msg).encode("utf-8"), sequence=True)

    def add_record(self, record: RecordTuple):
        self.records_queue.put(json.dumps(record).encode("utf-8"))
