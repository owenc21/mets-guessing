from flask import Flask
from flask_restful import Resource, Api

from user import Register, LogIn, Stats

app = Flask(__name__)
api = Api(app)

api.add_resource(Register, "/auth/register")
api.add_resource(LogIn, "/auth/login")
api.add_resource(Stats, "/user/info/<token>")

if __name__ == '__main__':
    app.run(debug=True)