"""
Module containing all user API endpoints
"""
from flask import Response, request, make_response
from flask_restful import Resource

from auth import create_user, login
from utils.auth_utils import token_required, login_required, generate_response


class Register(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user

        @return JSON object of response and HTTP status
        """
        input_data = request.get_json()
        response, status = create_user(input_data)
        return make_response(response, status)
    

class LogIn(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST response method for login user

        @return JSON object of response (including token)
        and HTTP status
        """
        input_data = request.get_json()
        response, status = login(input_data)
        return make_response(response, status)
    

class LogInToken(Resource):
    @staticmethod
    def post(token) -> Response:
        """
        POST response method for login user WITH a TOKEN
        
        @return JSON object of respoinse (including token)
        and HTTP status
        """
        input_data = request.get_json()
        response, status = login(input_data, token)
        return make_response(response, status)


class Stats(Resource):
    @staticmethod
    @login_required
    def post(token) -> Response:
        """
        POST response for method for user stats

        @return JSON object of response (with stats)
        and HTTP status
        """

        data = request.get_json()
        data["hello"] = 69420
        response, status = generate_response(
            data=data,
            message="it worked lol",
            status=200
        )
        return make_response(response, status)
