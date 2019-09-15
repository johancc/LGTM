"""
Main server script. Uses various apis to determine whether the person speaking is under the influence or not.
The server is stateless, no information is stored.
WIRE PROTOCOL --
POST:
    {"path" : string pointing to filepath of the audio} -> True or False, depending on whether the audio is of a
    person under the influence,
    "link" : link to the Google Cloud Object Storage object. The object must be public,
    "original_text": The original text that the user was asked to recite.
"""
import os
from dataclasses import dataclass

import requests
from flask import Flask
from flask_restful import Api, Resource, reqparse
from fuzzywuzzy import fuzz

from revAI import RevAI

AUDIO_FILE_EXTENSION = ".mp3"
BUCKET_NAME = "lgtm_hackmit/o/"
REV_AI = RevAI()
app = Flask(__name__)
api = Api(app)
overall_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_sound_file.wav")


@dataclass
class Analysis:
    """
    Response of the speech to text analysis from various apis.
    More fields should be added as the api interface is finalized.
    """
    intoxicated: bool
    similarity: float


# def download(url: str) -> str:
#     """
#     Download file to temporary storage
#     :param url: Path to the Google Cloud Object Storage file. Must be a public object.
#     :return: file path
#     """
#     # Extracting the filename from the url
#     # Based on the assumption that the filename is between the bucket name and '?'
#     start_index = url.index(BUCKET_NAME) + len(BUCKET_NAME)
#     filename = url[start_index: url.index("?")]
#     r = requests.get(url)
#     with open(filename, "wb") as code:
#         code.write(r.content)
#     return filename

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
    filename = overall_file
    r = requests.get(url)
    with open(filename, "wb") as code:
        code.write(r.content)
    return filename


def analyze(filename: str, original_text: str) -> Analysis:
    """
    Computes the fuzzy string similarity between the speech and the original text by using
    various Speech to Text APIs
    :param filename: Audio of the user reciting the original text.
    :param original_text: Text spoken by the user.
    :return: The final analysis, which includes whether the user is intoxicated or not and the fuzzy similarity.
    """
    if not os.path.isfile(filename):
        raise ValueError("Path does not exist.")
    match_ratio = 0
    rev_ai_output = REV_AI.get_transcript(filename)
    print(rev_ai_output)
    match_ratio += fuzz.ratio(original_text, rev_ai_output)
    analysis = Analysis(similarity=match_ratio / 1,
                        intoxicated=match_ratio / 1 <= 80)
    print(analysis)
    return analysis


class LGTM(Resource):

    def get(self) -> tuple:
        return self.post()

    def post(self) -> tuple:
        parser = reqparse.RequestParser()
        parser.add_argument("path")
        parser.add_argument("link")
        parser.add_argument("original_text")
        args = parser.parse_args()
        audio_file_path = args["path"]
        google_object_link = args["link"]
        original_text = args["original_text"]
        if google_object_link is not None:
            audio_file_path = download(google_object_link)
        analysis = analyze(audio_file_path, original_text)
        print("Analysis: ", analysis)
        if analysis.intoxicated:
            return True, 200
        else:
            return False, 200


api.add_resource(LGTM, "/verify")
if __name__ == "__main__":
    app.run(debug=True)
