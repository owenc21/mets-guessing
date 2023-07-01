import functools
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

# Create blueprint named 'user'
bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """ 
    Register user and instantiate entry in database
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        if not username:
            #TODO: add handler for not endering username
            print("Handled not entering username")
        elif not password:
            #TODO: add handler for not entering password
            print("Handled not entering password")

        error = None
        try:
            db.execute("INSERT INTO user (username, password) VALUES (?,?)",
                       (username, generate_password_hash(password=password)))
            db.commit()
        except db.IntegrityError:
            error = f"Username {username} is already taken"
        else:
            return redirect(url_for("user.login"))
        # flash(error)
        
    return render_template('user/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Log user in, set user cookie to be used elewhere
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # Handle incorrect username or password
        error = None
        if user is None or not check_password_hash(user['password'], password):
            error = 'Incorrect username or password'
            print("Handled incorrect username or password")
        
        if error is None:
            print("Handled correct username and password")
            # Save current play state
            play = session.get('play')
            # Store user information in cookie
            session.clear()
            session['user_id'] = user['id']
            if play is not None:
                # Player played game before logging in
                update_user_play_db(play)
                session['play'] = play

            return redirect(url_for('index'))
        # flash(error)
    
    return render_template('user/login.html')


@bp.route('/logout')
def logout():
    """
    Log user out by clearing cookies (but saving play state)
    """
    play = session.get('play')
    session.clear()
    if play is not None:
        session['play'] = play
    
    print("handled logout")

    return redirect(url_for('index'))
        


@bp.before_app_request
def load_logged_user():
    """
    If user has logged in, access user ID from cookies
    and set g.user to that user for access in pages
    Runs before every view
    """
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.before_app_request
def load_play_state():
    """
    Load the current play state of a user from cookies
    and set g.play to that state
    Tracks information about whether current day's game
    was played, and stats if it was played (track across
    logins and logous)
    """
    play = session.get('play')
    if play is None:
        g.play = None
    else:
        g.play = play


def login_required(view):
    """
    Utility function to require user to be logged
    in. Can be used for any view
    """
    @functools.wraps(wrapped=view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(location=url_for(endpoing='user.login'))
        
        return view(**kwargs)
    
    return wrapped_view


def update_user_play_db(play):
    """
    Updates the user's stats in the db
    @param play:    dict of information about user's
    game
    """
    user = g.user
    db = get_db()
    if not play['game']:
        return
    db.execute(
        'UPDATE user SET games = ?, wins = ?'
        ' WHERE id = ?',
        (user['games']+1,
         user['wins']+1 if play['win'] else user['wins'],
         user['id'])
    )
    db.commit()