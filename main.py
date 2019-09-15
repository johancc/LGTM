"""
Main server script. Uses various apis to determine whether the person speaking is under the influence or not.
The server is stateless, no information is stored.
WIRE PROTOCOL --
POST:
    {"path" : string pointing to filepath of the audio} -> True or False, depending on whether the audio is of a
    person under the influence.

"""
import os
from dataclasses import dataclass

from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

a = ".mp3"


@dataclass
class Analysis:
    """
    Response of the speech to text analysis from various apis.
    More fields should be added as the api interface is finalized.
    """
    drunk: bool


def analyze(filename: str) -> Analysis:
    # TODO: Feed the audio file into the api interface.
    if not os.path.isfile(filename):
        raise ValueError("Path does not exist.")
    analysis = Analysis(drunk=True)
    return analysis


class LGTM(Resource):

    def post(self) -> tuple:
        parser = reqparse.RequestParser()
        parser.add_argument("path")
        args = parser.parse_args()

        audio_file_path = args["path"]
        try:
            analysis = analyze(audio_file_path)
        except ValueError:
            return False, 400
        if analysis.drunk:
            return True, 200
        else:
            return False, 200


api.add_resource(LGTM, "/verify")
if __name__ == "__main__":
    app.run(debug=True)
