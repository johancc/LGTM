from rev_ai import apiclient
import json
import os

f = open("revAI_accessToken.txt", 'r')
overall_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_sound_file.wav")
ACCESS_TOKEN = f.read()


class RevAI:

    def __init__(self):
        # create your client
        self.client = apiclient.RevAiAPIClient(ACCESS_TOKEN)

    def get_transcript(self, path):
        # Use when want a new transcript from rev.ai
        job = self.client.submit_job_local_file(path)
        job_details = self.client.get_job_details(job.id)
        while self.client.get_job_details(job.id).status.name != "TRANSCRIBED":
            print(self.client.get_job_details(job.id).status.name)
            pass
        # Get only the first speaker in case of background noise
        transcript_json = self.client.get_transcript_json(job.id)["monologues"][0]

        # Uncomment when trying to conserve time on rev.ai
        # f = open("transcript.json")
        # Get only the first speaker in case of background noise
        # transcript_json = json.load(f)["monologues"][0]

        transcript_text = ""
        for i in transcript_json["elements"]:
            transcript_text += (i["value"])

        return transcript_text


if __name__ == "__main__":
    revai = RevAI()
    # revai.get_transcript("test.m4a")
    revai.get_transcript(overall_file)
