import json
import wave
import logging
from pathlib import Path

#logging!
logger = logging.getLogger(__name__)


def get_duration(filename):

    # Open the WAV file
    with wave.open(filename, 'r') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration_in_seconds = frames / float(rate)
        return duration_in_seconds

def craft_input_manifest(filename, duration):
    manifest = {}
    manifest['audio_filepath'] = filename
    manifest['duration'] = duration
    manifest['taskname'] = 'asr'
    manifest['source_lang'] = 'en' #shouldn't hardcode this
    manifest['target_lang'] = 'en'
    manifest['pnc'] = 'yes'

    manifest_file_name = Path(filename).stem + ".json"

    with open(manifest_file_name, "w") as outfile:
        outfile.write(json.dumps(manifest))

    return manifest_file_name

def transcribe(filename, canary_model):

    logger.debug(f"canary.transcribe.filename: {filename}")
    duration = get_duration(filename)

    manifest = craft_input_manifest(filename, duration)

    #canary-1b
    fulltext = canary_model.transcribe(
        manifest,
        batch_size=16,  # batch size to run the inference with
    )

    return fulltext

