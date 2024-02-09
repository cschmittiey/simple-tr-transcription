import os
from faster_whisper import WhisperModel
import config.config as config
# faster-whisper initialization
model = WhisperModel(config.whisper_model_name, device=config.whisper_device_type, download_root=config.whisper_model_path)

def transcribe(filename, cleanup=True):
    segments, info = model.transcribe(filename, beam_size=5, language="en", vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500))

    fulltext = ""
    for segment in segments:
        fulltext += segment.text

    if cleanup:
        # clean up, clean up, everybody do your share
        os.remove(filename)

    return fulltext
