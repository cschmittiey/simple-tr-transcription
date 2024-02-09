import json
import os
import wave
import logging
from pathlib import Path
from nemo.collections.asr.models import EncDecMultiTaskModel

# canary 1b initialization
# load model
canary_model = EncDecMultiTaskModel.from_pretrained('nvidia/canary-1b')
# update dcode params
decode_cfg = canary_model.cfg.decoding
decode_cfg.beam.beam_size = 1
canary_model.change_decoding_strategy(decode_cfg)

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

    if os.path.split(filename)[0] == '':
        audio_filepath = os.getcwd() + "/" + filename
    else:
        audio_filepath = filename

    manifest = {}
    manifest['audio_filepath'] = audio_filepath
    manifest['duration'] = duration
    manifest['taskname'] = 'asr'
    manifest['source_lang'] = 'en' #shouldn't hardcode this
    manifest['target_lang'] = 'en'
    manifest['pnc'] = 'yes'
    manifest['answer'] = "idk"

    manifest_file_name = Path(filename).stem + ".json"

    with open(manifest_file_name, "w") as outfile:
        outfile.write(json.dumps(manifest))

    return manifest_file_name

def transcribe(filename, cleanup=True):

    logger.debug(f"canary.transcribe.filename: {filename}")
    duration = get_duration(filename)
    logger.debug(f"canary.transcribe.duration: {duration}")

    manifest = craft_input_manifest(filename, duration)

    fulltext = canary_model.transcribe(manifest)
    fulltext = fulltext[0]

    if cleanup:
        # clean up, clean up, everybody everywhere
        os.remove(filename)
        os.remove(manifest)

    return fulltext

