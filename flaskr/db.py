import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def create_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db


def close_db(e=None):
    g.pop('db', None)
    
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    #open_resource opens a file relative to flaskr package
    with current_app.open_resource('models.sql') as f:
        db.executescript(f.read().decode('utf-8'))


#defines a command line command called 'init-db' that can be called
#don't need to initialize database every time
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initalized the database.')


def init_app(app):
    #tells flask to call this function when cleaning up following returning response
    app.teardown_appcontext(close_db)
    # new command that can be called with 'flask' command
    app.cli.add_command(init_db_command)
    