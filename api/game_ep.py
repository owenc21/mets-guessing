"""
Module containing endpoints (ep) for game
"""
from flask import Response, request, make_response
from flask_restful import Resource

from game import init_session, game
from utils.auth_utils import Token, generate_response
from utils.http_code import HTTP_403_FORBIDDEN


class Init(Resource):
    @staticmethod
    def post(token) -> Response:
        """
        POST method for initializing session with token
        
        @returns JSON object of response and HTTP status
        """
        
        # Veryify Token

        if not Token.check_token(token):
            response, status = generate_response(
                data=token,
                message="Invalid token",
                status=HTTP_403_FORBIDDEN
            )
            return make_response(response, status)

        input_data = request.get_json()
        response, status = init_session(user_info=input_data, token=token)
        return make_response(response, status)


class InitGuest(Resource):
    @staticmethod
    def post() -> Response:
        """
        POST method for initializing session without token

        @returns    JSON object of response and HTTP status
        """

        token = Token.create_token()
        
        input_data = request.get_json()
        response, status = init_session(user_info=input_data, token=token)
        return make_response(response, status)


class Guess(Resource):
    @staticmethod
    def post(token) -> Response:
        """
        POST method for making a guess in the game

        @returns JSON object of response and HTTP status
        """

        # Veryify Token

        if not Token.check_token(token):
            response, status = generate_response(
                data=token,
                message="Invalid token",
                status=HTTP_403_FORBIDDEN
            )
            return make_response(response, status)

        input_data = request.get_json()
        response, status = game(token, input_data)
        return make_response(response, status)

        