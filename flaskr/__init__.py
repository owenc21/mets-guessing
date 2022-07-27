import os
from flask import Flask, redirect, url_for, g


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'stats.sqlite'),
    )

    if test_config is None:
        # override default values with config set in config.py
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test config otherwise
        app.config.from_mapping(test_config)

    #need to create app.instance_path for sql database
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #from . import db
    #db.init_app(app)

    from . import gen_player
    with app.app_context():
        gen_player.set_player()

    from . import game
    app.register_blueprint(game.bp)


    return app