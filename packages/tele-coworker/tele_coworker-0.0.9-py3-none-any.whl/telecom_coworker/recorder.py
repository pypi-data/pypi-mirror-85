import json
from datetime import datetime
from time import sleep

from flask import Flask
from kazoo.client import KazooClient
from kazoo.recipe.queue import Queue

from telecom_coworker.models import RecordTuple
from telecom_coworker.web.db import Record


class Recorder(object):

    def __init__(self, zk: KazooClient, namespace: str, app: Flask):
        self.zk = zk
        self.namespace = namespace
        self.app = app

    def run(self):
        election = self.zk.Election(f"{self.namespace}/recorder")
        election.run(self._master_func)

    def _master_func(self):
        queue = Queue(self.zk, f"{self.namespace}/records")
        while True:
            event_record_bytes = queue.get()
            if event_record_bytes is None:
                sleep(1)
            else:
                with self.app.app_context():
                    rt = RecordTuple(*json.loads(event_record_bytes.decode('utf-8')))
                    created_at = datetime.fromisoformat(rt.created_at)
                    r = Record(record_type=rt.record_type, wid=rt.wid, worker_ip=rt.worker_ip, tid=rt.tid,
                               task_type=rt.task_type, comment=rt.comment, created_at=created_at)
                    r.save()

    def __call__(self, *args, **kwargs):
        self.run()
