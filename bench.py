#!/usr/bin/env python3
import argparse
import models.whisper as whisper
import models.canary as canary
import os
import logging
import subprocess
import pathlib

# log config
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(
                    prog='bench.py',
                    description='Use this program to test the different models and audio transformations against audio files.',
                    epilog='cleeb.')

parser.add_argument('filename')
parser.add_argument('-n', '--normalize', action='store_true')
args = parser.parse_args()

def compare(file):

    if args.normalize:

        # Define the input and output file paths
        input_file = file
        output_file = pathlib.Path(file).stem + ".normalized.wav"

        # Define the speechnorm filter string
        speechnorm_filter = 'speechnorm=e=25:r=0.0001:l=1'

        # Construct the FFmpeg command
        ffmpeg_command = [
            'ffmpeg',
            '-i', input_file,
            '-af', speechnorm_filter,
            output_file
        ]

        # Execute the FFmpeg command
        subprocess.run(ffmpeg_command, check=True)

        file = output_file

    whisper_transcript = whisper.transcribe(file, cleanup=False)
    canary_transcript = canary.transcribe(file, cleanup=False)

    logging.info("===================================================")
    logging.info(f"New Transcription: {file}")
    logging.info(f"Whisper Transcription: {whisper_transcript}")
    logging.info(f"Canary Transcription: {canary_transcript}")
    logging.info(f"Normalized?: {args.normalize}")


if os.path.isdir(args.filename):
    files = os.listdir(args.filename)
    for file in files:
        path = os.path.abspath(os.path.join(args.filename, file))
        compare(path)
else:
    logging.info(args.filename)
    compare(args.filename)

