"""
Module for game functionality
"""
import os

from utils.http_code import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_201_CREATED
from utils.auth_utils import Token, generate_response
from utils.game_utils import check_guess, gen_guess_response, correct_check
from db.db import get_db


def init_session(token, user_info):
    """
    Function to create a session at the start of a game
    
    @param token    User's JWT token
    @returns        Tuple of (Response, Status)
    """

    db = get_db()
    session = db.execute(
        'SELECT * FROM session WHERE token = ?', (token,)
    ).fetchone()

    if session is None:
        db.execute(
            "INSERT INTO session (token, game_id, win) VALUES (?,?,?)",
            (token, os.environ.get("GAME_ID"), 0)
        )
        db.commit()
    else:
        if session["game_id"] == os.environ.get("GAME_ID") and session["win"] == 1:
            user_info["session"] = session
            return generate_response(
                data=user_info,
                message="Already played this game",
                status=HTTP_403_FORBIDDEN
            )
        
    # At this point, session with token as been created
    return generate_response(
        data=user_info,
        message="Session created",
        status=HTTP_201_CREATED
    )


def game(token, user_info, guess):
    """
    Function to handle the game functionality, user making
    a guess, validating it, and returning response

    @param token        User's JWT token
    @param user_info    Information in body of request
    @param guess        User's guess
    @returns            Tuple of (Response, Status)
    """

    user_info["guess"] = guess
    db = get_db()

    # Get user session
    session = db.execute(
        'SELECT * FROM session WHERE token = ?', (token,)
    ).fetchone()

    if session is None:
        return generate_response(
            data=user_info,
            message="Unknown server error",
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Ensure less than 9 guesses made, update number of guesses
    user_info["session"] = session
    if session["guesses"] > 9:
        return generate_response(
            data=user_info,
            message="8 guesses already made",
            status=HTTP_400_BAD_REQUEST
        )
    db.execute(
        'UPDATE session SET guesses = ?',
        ' WHERE token = ?',
        (session["guesses"]+1, token)
    )
    db.commit()

    session = db.execute(
        'SELECT * FROM session WHERE token = ?', (token,)
    ).fetchone()

    # Check if user is logged in or guest
    is_logged_in = False
    logged_user = None
    if Token.get_user_id(token) != "GUEST":
        is_logged_in = True
        user_id = Token.get_user_id(token)
        logged_user = db.execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id,)
        ).fetchone

    # Ensure guess is valid
    if not check_guess(guess):
        return generate_response(
            data=user_info,
            message="Guess not a Mets' player",
            status=HTTP_400_BAD_REQUEST
        )

    win_status = correct_check(guess)
    response =  gen_guess_response(guess)
    response["win_status"] = win_status

    # Update session if guess is correct
    if win_status:
        db.execute(
            'UPDATE session SET win = ?'
            ' WHERE token = ?',
            (1,token)
        )
        db.commit()

    # Set user stats if logged in
    if is_logged_in:
        if win_status:
            long_winstreak = logged_user["long_winstreak"]
            if long_winstreak == logged_user["cur_winstreak"]:
                long_winstreak += 1
            db.execute(
                'UPDATE user SET games = ?, wins = ?, cur_winstreak = ?, long_winstreak = ?',
                (logged_user["games"]+1, logged_user["wins"]+1, logged_user["cur_winstreak"]+1,
                 long_winstreak)
            )
            db.commit()
        elif not win_status and session["guesses"] == 8:
            db.execute(
                'UPDATE user SET games = ?, cur_winstreak = ?',
                (logged_user["games"]+1, 0,)
            )
            db.commit()
        user_info["user"] = logged_user
    
    user_info["response"] = response
    user_info["session"] = session

    return generate_response(
        data=user_info,
        message=f"Successfully made guess: {guess} : {win_status}",
        stats=HTTP_200_OK
    )

