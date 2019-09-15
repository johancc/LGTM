"""
Main server script. Uses various apis to determine whether the person speaking is under the influence or not.
The server is stateless, no information is stored.
WIRE PROTOCOL --
POST:
    {"path" : string pointing to filepath of the audio} -> True or False, depending on whether the audio is of a
    person under the influence.
    {"link" : link to the Google Cloud Object Storage object. The object must be public.
"""
import os
import requests
from dataclasses import dataclass

from flask import Flask
from flask_restful import Api, Resource, reqparse

from revAI import RevAI

AUDIO_FILE_EXTENSION = ".mp3"
BUCKET_NAME = "lgtm_hackmit/o/"
REV_AI = RevAI()
app = Flask(__name__)
api = Api(app)



@dataclass
class Analysis:
    """
    Response of the speech to text analysis from various apis.
    More fields should be added as the api interface is finalized.
    """
    drunk: bool


def download(url: str) -> str:
    """
    Download file to temporary storage
    :param url: Path to the Google Cloud Object Storage file. Must be a public object.
    :return: file path
    """
    # Extracting the filename from the url
    # Based on the assumption that the filename is between the bucket name and '?'
    start_index = url.index(BUCKET_NAME) + len(BUCKET_NAME)
    filename = url[start_index: url.index("?")]
    r = requests.get(url)
    with open(filename, "wb") as code:
        code.write(r.content)
    return filename


def analyze(filename: str) -> Analysis:
    # TODO: Feed the audio file into the api interface.
    if not os.path.isfile(filename):
        raise ValueError("Path does not exist.")
    print("made it.")
    rev_ai_output = REV_AI.get_transcript(filename)
    print("finished.")
    # Find some way to compare the example text with the output.
    print("Transcript: " + rev_ai_output)
    analysis = Analysis(drunk=True)

    return analysis


class LGTM(Resource):

    def post(self) -> tuple:
        parser = reqparse.RequestParser()
        parser.add_argument("path")
        parser.add_argument("link")
        args = parser.parse_args()
        audio_file_path = args["path"]
        google_object_link = args["link"]

        if google_object_link is not None:
            audio_file_path = download(google_object_link)
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
