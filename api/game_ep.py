"""
Module containing endpoints (ep) for game
"""
from flask import Response, request, make_response
from flask_restful import Resource

from game import init_session, game
from utils.auth_utils import Token


class Init(Resource):
    @staticmethod
    def post(token) -> Response:
        """
        POST method for initializing session with token
        
        @returns JSON object of response and HTTP status
        """
        
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
    def post() -> Response: