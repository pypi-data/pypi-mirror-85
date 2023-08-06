from flask import Blueprint, request

from telecom_coworker.models import Task
from telecom_coworker.web import log
from telecom_coworker.web.utils import fail, ok
from telecom_coworker.web.zk import kazoo_helper

bp = Blueprint("api", __name__)


@bp.route('/task', methods=['POST'])
def create_task():
    log.info(f"create task with json: {request.json}")
    try:
        task: Task = request.json
    except AttributeError as e:
        return fail(40, "需要参数: task_type:str[len>5], params:dict")

    if len(task["task_type"]) < 5:
        return fail(41, '需要参数: task_type:str[len>5]')

    helper = kazoo_helper()
    tid = helper.add_task(task["task_type"], **task['params'])

    return ok({"task_id": tid})


@bp.route('/task/<uuid:task_id>/cancel', methods=['GET', 'POST'])
def cancel_task(task_id):
    helper = kazoo_helper()
    result = helper.cancel_task(task_id)
    if result:
        return ok()
    else:
        return fail(44, '没有找到对应的Task')
