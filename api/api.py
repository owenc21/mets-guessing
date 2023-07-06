from flask import Flask
from flask_restful import Resource, Api

from user import Register, LogIn, LogInToken, Stats
from game_ep import Init, InitGuest, Guess

app = Flask(__name__)
api = Api(app)

api.add_resource(Register, "/auth/register")
api.add_resource(LogIn, "/auth/login")
api.add_resource(LogInToken, "/auth/login/<token>")
api.add_resource(Stats, "/user/info/<token>")
api.add_resource(Init, "/init/<token>")
api.add_resource(InitGuest, "/init")
api.add_resource(Guess, "/<token>")

if __name__ == '__main__':
    app.run(debug=True)