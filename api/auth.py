"""
Module with authentication/authorization utilites
"""
from werkzeug.security import check_password_hash, generate_password_hash

from utils.http_code import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from utils.auth_utils import generate_response, Token
from db.db import get_db
    

def create_user(user_data):
    """
    Function to create new user and store in database

    @param user_data: JSON object of credentials for new user
    @return Tuple of response data, HTTP status
    """

    username = str(user_data.get("username"))
    password = str(user_data.get("password"))
    errors = None

    # "Cleanse" username and password
    if username is None:
        errors = "Username cannot be empty"
    elif len(username) <= 3 or len(username) >= 50:
        errors = "Username must be between 3 and 49 characters long"
    elif password is None:
        errors = "Password cannot be empty"
    elif len(password) <=3:
        errors = "Password must be at least 4 characters long"

    # Check if user exists
    db = get_db()
    user_check = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user_check is not None:
        errors = "Username already exists"
        del user_check
    
    # Return errors if they exist
    if errors is not None:
        return generate_response(
            data=user_data,
            message=errors,
            status=HTTP_400_BAD_REQUEST
        )
    
    # Insert user into database
    db.execute("INSERT INTO user (username, password) VALUES (?,?)",
                (username, generate_password_hash(password=password)))
    db.commit()
    
    del user_data["password"]

    return generate_response(
        data=user_data,
        message="User Created",
        status=HTTP_201_CREATED
    )


def login(user_data):
    """
    Function to log user in and generate JWT token

    @param user_data: JSON object of credentials for user
    @return Tuple of response data (including token), HTTP status
    """

    username = str(user_data.get("username"))
    password = str(user_data.get("password"))
    errors = None

    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    # Check if user exists
    if user is None:
        errors = "Username does not exist"
    elif not check_password_hash(user["password"], password):
        errors = "Password is incorrect"

    # Return errors if they exist
    if errors is not None:
        return generate_response(
            data=user_data,
            message=errors,
            status=HTTP_400_BAD_REQUEST
        )
    
    # Create JWT token for user
    token = Token.create_token(user["id"])
    user_data["token"] = token

    return generate_response(
        data=user_data,
        message="Logged in successfully; token returned",
        status=HTTP_201_CREATED
    )