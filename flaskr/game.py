from flask import (
    Blueprint, g, render_template, request, session
)
from . import gen_player
from . import db

bp = Blueprint('game', __name__, url_prefix='/')


#check if user has an ID stored in session, if so load their stats
@bp.before_app_request
def load_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id)
        ).fetchone()


@bp.route('/', methods=('GET',))
def game():
    return render_template('game.html')


@bp.route('/genresult', methods=('GET', 'POST'))
def genresult():
    player = request.args.get('player')
    
    guess_values = gen_player.gen_return_response(player)

    if guess_values is False:
        return {
            "error": "not a met player"
        }
    else:
        pass

    guess_attrs = guess_values[0]
    adjust_attrs = guess_values[1]

    print(guess_attrs)
    return {
        "guess":
        {
            "player": guess_attrs[0],
            "birth": guess_attrs[1],
            "pos": guess_attrs[2],
            "age": guess_attrs[3],
            "bat": guess_attrs[4],
            "throw": guess_attrs[5],
            "height": guess_attrs[6],
            "weight": guess_attrs[7]
        },
        "adjust":
        {
            "adj_player": adjust_attrs[0],
            "adj_birth": adjust_attrs[1],
            "adj_pos": adjust_attrs[2],
            "adj_age": adjust_attrs[3],
            "adj_bat": adjust_attrs[4],
            "adj_throw": adjust_attrs[5],
            "adj_height": adjust_attrs[6],
            "adj_weight": adjust_attrs[7],
            "correct": adjust_attrs[8]
        }
    }


@bp.route('/set', methods=('GET', 'POST'))
def setresult():
    db = db.get_db()
    if request.method == 'POST':

        result = request.args.get('result')
        if result == "w":
            if g.user == None:
