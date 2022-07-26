from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)


bp = Blueprint('game', __name__, url_prefix='/')


@bp.route('/', methods=('GET',))
def game():
    return render_template('game.html')


@bp.route('/genresult', methods=('GET', 'POST'))
def genresult():
    g.guesses = 0
    if g.guesses >= 8:
        return False
    else:
        player = request.args.get('player')
        print("player was " + player)
        g.guesses += 1
        return {
            "player": player,
        }