from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from kazoo.exceptions import NoNodeError

from telecom_coworker.web.db import Record
from telecom_coworker.web.zk import stats as zk_stats, kazoo_helper

bp = Blueprint("pages", __name__, url_prefix="/page")


@bp.route("/")
def index():
    stats = zk_stats()
    task_size = stats.tasks_total_num()
    worker_size = stats.workers_total_num()
    payload_size = stats.payload_total()
    task_stats = stats.task_stats()
    task_type_list_need_more_workers = stats.task_type_list_need_more_workers()

    return render_template("index.html", task_size=task_size,
                           worker_size=worker_size, payload_size=payload_size,
                           task_stats=task_stats,
                           task_type_list_need_more_workers=task_type_list_need_more_workers)


@bp.route("/workers")
def page_workers():
    stats = zk_stats()
    workers = stats.worker_stats().values()
    return render_template("workers.html", workers=workers)


@bp.route("/task", methods=('GET', 'POST'))
def page_task():
    if request.method == 'POST':
        tid = request.form.get('tid')
        if tid is not None:
            tid = tid.strip()
        if tid is not None and len(tid) > 5:
            return redirect(url_for("pages.page_task", tid=tid))
        else:
            flash("没有找到对应的任务")

    query_task_id = request.args.get('tid')
    if query_task_id is not None and len(query_task_id) > 0:
        try:
            helper = kazoo_helper()
            state = helper.get_task_state(query_task_id)
            return render_template("task.html", state=state, tid=query_task_id)
        except NoNodeError as e:
            flash('没有找到对应的任务')

    return render_template("task.html")


@bp.route("/record", methods=('GET', 'POST'))
def page_record():
    if request.method == 'POST':
        query_type = request.form.get('query_type')
        query_value = request.form.get('q')
        if query_value:
            query_value = query_value.strip()

        if query_type not in ('wid', 'tid', 'worker_ip', 'task_type') or len(query_value) < 5:
            abort(404)

        return redirect(url_for("pages.page_record", query_type=query_type, q=query_value))

    else:
        query_type = request.args.get("query_type")
        query_value = request.args.get("q")

        if query_type in ('wid', 'tid', 'worker_ip', 'task_type') and len(query_value) >= 5:
            q = {
                query_type: query_value
            }
            records = Record.query.filter_by(**q).order_by(Record.id.desc()).limit(50).all()
        else:
            records = Record.query.order_by(Record.id.desc()).limit(50).all()

        return render_template("record.html", records=records, query_type=query_type, q=query_value)

# @bp.route("/clear_messages", methods=('GET',))
# def clear_messages():
#     msg_h = msg_handler()
#     msg_h.clear()
#
#     return redirect(url_for("index"))
