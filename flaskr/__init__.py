import os
from flask import Flask
import threading


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'stats.sqlite'),
    )
    app.use_reloader = False

    if test_config is None:
        # override default values with config set in config.py
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test config otherwise
        app.config.from_mapping(test_config)


    from . import gen_player
    from . import config

    #create daemon thread to reset player every 24 hours
    playerThread = threading.Thread(target=gen_player.set_player, args=(86400,), daemon=True)
    playerThread.start()

    from . import game
    app.register_blueprint(game.bp)


    return app