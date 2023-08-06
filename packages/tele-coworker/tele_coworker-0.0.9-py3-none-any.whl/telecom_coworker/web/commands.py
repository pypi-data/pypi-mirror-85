import click
from flask import current_app
from flask.cli import with_appcontext

from telecom_coworker.recorder import Recorder
from telecom_coworker.web.zk import client


@click.command("recorder")
@with_appcontext
def recorder():
    """run one single recorder"""
    zk_namespace = current_app.config['ZK_NAMESPACE']
    r = Recorder(client(), zk_namespace, current_app)
    r.run()
