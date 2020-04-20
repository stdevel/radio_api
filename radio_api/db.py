#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SQLite database backend
"""
import sqlite3
import logging
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    This function created a database connection and returns the handler.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    """
    This function closes the database.
    """
    database = g.pop('db', None)
    if error:
        logging.error(error)
    if database is not None:
        database.close()

def init_db():
    """
    This function initializes the database.
    """
    database = get_db()

    with current_app.open_resource('schema.sql') as db_file:
        database.executescript(db_file.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    This function clears the existing data and creates new tables.
    """
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """
    This function initializes the application.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
