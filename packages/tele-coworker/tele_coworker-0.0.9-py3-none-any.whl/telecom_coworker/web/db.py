from datetime import datetime

import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import Model, SQLAlchemy


class CRUDMixin(Model):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


db = SQLAlchemy(model_class=CRUDMixin)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.String(80), nullable=False)
    wid = db.Column(db.String(100), nullable=False, index=True)
    worker_ip = db.Column(db.String(100), index=True)
    tid = db.Column(db.String(100), index=True)
    task_type = db.Column(db.String(100), index=True)
    comment = db.Column(db.TEXT)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Record id: %r type: %r, wid: %r, tid: %r> created_at: %r' % (
            self.id, self.record_type, self.wid, self.tid, self.created_at)


@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()


def init_app(app: Flask):
    db.init_app(app)
    app.cli.add_command(init_db_command)
