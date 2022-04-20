import logging
import os
from time import sleep

import google.api_core.exceptions
import requests

# Remove SSL Warning
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)
# Remove Excwption
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

from datetime import datetime

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "/home/xcloud/PycharmProjects/parser/voice-recognition-346809-01b557a42772.json"


def transcribe_file(speech_file):
    try:

        """Transcribe the given audio file asynchronously."""
        from google.cloud import speech

        client = speech.SpeechClient()
        first_lang = "iw-IL"
        # second_lang = "ar-IL"
        # third_lang = "en-US"
        # fourth_lang = "ru-RU"

        with open(speech_file, "rb") as audio_file:
            content = audio_file.read()

        """
         Note that transcription is limited to a 60 seconds audio file.
         Use a GCS file for audio longer than 1 minute.
        """
        audio = speech.RecognitionAudio(content=content)

        diarization_config = speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=True,
            min_speaker_count=2,
            max_speaker_count=10,
        )

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
            audio_channel_count=2,
            sample_rate_hertz=8000,
            language_code=first_lang,
            # alternative_language_codes=[second_lang, third_lang,fourth_lang],  # don't work correctly yet
            enable_word_time_offsets=True,
            diarization_config=diarization_config,


        )

        operation = client.long_running_recognize(config=config, audio=audio)

        print("Waiting for operation to complete...")
        response = operation.result()

        # Convert response to dict
        result_dict = type(response).to_dict(response)

        # Save result_dict in log file
        logger = logging.getLogger()
        handler = logging.FileHandler("logfile.log")
        logger.addHandler(handler)
        logger.error("Date: " + str(datetime.now()) + " | Text: " + str(result_dict))

        list_transcript = []
        for key in result_dict["results"]:
            for j in key["alternatives"]:
                list_transcript.append(j["transcript"])

        transcription_text = " ".join(list_transcript)
        print(transcription_text)

        response = requests.post(
            "https://pbxt.x-cloud.info/stats/api/voiceRecognition/storeVoiceTranscript.php",
            verify=False,
            data={"transcription": transcription_text},
        )

        print(response.content)
    except google.api_core.exceptions.ServiceUnavailable:
        sleep(5)
        transcribe_file(speech_file)
