from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.user import login_required
from flaskr.db import get_db

bp = Blueprint('game', __name__)

@bp.route('/')
def index():
    return render_template('game/index.html')