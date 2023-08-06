from typing import TypedDict, NamedTuple


class WorkerInfo(TypedDict):
    wid: str
    handle_type: str
    max_handle_num: int
    curr_handle_num: int
    hostname: str
    hostip: str
    pid: str


class Task(TypedDict):
    tid: str
    task_type: str
    params: dict


class TaskState(TypedDict):
    tid: str
    state: str
    ip: str
    pid: str
    exitcode: int
    updated_at: str  # format: ISO 8601
    logs: str
    retries: list


class Message(NamedTuple):
    type: str
    tid: str
    wid: str
    content: str


class RecordTuple(NamedTuple):
    record_type: str
    wid: str
    worker_ip: str
    tid: str
    task_type: str
    created_at: str
    comment: str = None


STATE_RUNNING = 'running'
STATE_PENDING = 'pending'
STATE_EXITED = 'exited'
STATE_FATAL = 'fatal'

if __name__ == '__main__':
    w = WorkerInfo(wid="my_wid", handle_type="type1", max_handle_num=10)
    print(w.get("curr_handle_num", 0))
    w["curr_handle_num"] = 10
    print(w)
