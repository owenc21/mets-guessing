from functools import wraps
import os
import jwt
from datetime import datetime, timedelta, timezone
from flask import request

from db.db import get_db
from .http_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
"""
Collection of utilites for authenticaiton/authorization
"""


class Token:
    @staticmethod
    def create_token(user_id="GUEST"):
        """
        Creates a JWT token that is encoded with an expiration date
        of one week from time of creation along with user's ID (from
        the DB)

        @param user_id: ID of user for whom token is created for
        @returns JWT Token for user
        """

        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
            "id": str(user_id)
        }

        token = jwt.encode(
            payload,
            os.environ.get("SECRET_KEY"),
            algorithm="HS256"
        )
        return token
    

    @staticmethod
    def decode_token(token):
        """
        Returns decoded JWT token

        @param token: JWT token to decode
        @returns decoded JWT token
        """

        return jwt.decode(
            str(token),
            os.environ.get("SECRET_KEY"),
            algorithms="HS256",
            options={"require_exp": True}
        )

    
    @staticmethod
    def check_token(token):
        """
        Takes a token and checks if token is valid

        @param token: JWT token to verify
        @returns boolean indicating token validity (True iff valid)
        """
        try:
            Token.decode_token(token)
            return True
        except:
            return False
    

    @staticmethod
    def get_user_id(token):
        """
        Takes a token and returns user's ID

        @param token: JWT token to get user's ID from
        @returns user's ID
        """

        data = Token.decode_token(token)
        return data["id"]


def generate_response(data=None, message=None, status=400):
    """
    It takes in a data, message, and status, and returns a dictionary with the data, message, and status
    
    :param data: The data that you want to send back to the client
    :param message: This is the message that you want to display to the user
    :param status: The HTTP status code, defaults to 400 (optional)
    :return: A tuple of a dictionary with the keys: (data, message, status),
    """
    if status == HTTP_200_OK or status == HTTP_201_CREATED:
        status_bool = True
    else:
        status_bool = False

    return {
        "data": data,
        "message": message,
        "status": status_bool,
    }, status


def login_required(f):
    """
    Wrapper function for API calls that require user to be
    logged in

    Verification is done by ensuring a token is valid AND
    belongs to a User
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get token
        token = kwargs['token']

        # Verify token is valid
        try:
            data = Token.decode_token(token)
            db = get_db()
            current_user = db.execute(
                'SELECT * FROM user WHERE id = ?', (data["id"],)
            ).fetchone()

            if current_user is None:
                return generate_response(
                    data=None,
                    message="Invalid authentication token",
                    status=HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            return generate_response(
                message="Unexpected error",
                data=None,
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return f(*args, **kwargs)
    
    return decorated
