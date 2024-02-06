import paho.mqtt.client as mqtt
import boto3
import os
from faster_whisper import WhisperModel
import string
import threading
from discord import Webhook, Embed
import aiohttp
import asyncio
import logging
import json
# hopefully this imports config/config.py and there's not some library out there named config... that would be awkward
import config.config as config

#log config
logging.basicConfig(level=logging.INFO)

# S3 initialization
session = boto3.session.Session()
s3 = session.client(service_name='s3',
                    aws_access_key_id=config.s3_config['s3_access_key'],
                    aws_secret_access_key=config.s3_config['s3_secret_key'],
                    endpoint_url='https://' + config.s3_config['s3_endpoint'])

# faster-whisper initialization
# TODO: make this a config option
model = WhisperModel(config.model_name, device=config.device_type, download_root="./config")

def on_connect(client, userdata, flags, rc):
    logging.info("MQTT Broker connected with result code " + str(rc))
    client.subscribe(config.mqtt_config['mqtt_uploaded_topic'])

def on_message(client, userdata, msg):
    filename = msg.payload.decode()
    logging.debug(f"Received filename: {filename}")
    # Start a new thread for handling the transcription process
    threading.Thread(target=handle_message, args=(filename,)).start()

def handle_message(filename):
    # Transcribe audio if the talkgroup is one we're interested in
    talkgroup = int(filename.split('-')[0])

    if check_tg(talkgroup):
        # Download file from S3
        local_filename = f"temp_{filename}"
        s3.download_file(config.s3_config['s3_bucket'], filename, local_filename)
        logging.debug(f"Downloaded {filename} from S3")
                
        logging.info(f"Transcribing {filename}")
        segments, info = model.transcribe(local_filename, beam_size=5, language="en", vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500))

        fulltext = ""
        for segment in segments:
            fulltext += segment.text

        logging.info(f"Transcription of {filename}: {fulltext}")

        #fire off discord notification unless there's no transcription text
        if fulltext:
            asyncio.run(send_talkgroup_webhook(talkgroup, filename, fulltext))

        #fire off mqtt notification
        #i don't really love just tossing out the file name, talkgroup, and transcription. we should ingest call data with the upload script and use that maybe?
        x = { 'talkgroup': talkgroup, 'filename':filename, 'transcription':fulltext}
        mqtt_transcribed_payload = json.dumps(x)
        mqtt_client.publish(config.mqtt_config['mqtt_transcribed_topic'], mqtt_transcribed_payload)

        # Clean up downloaded file
        os.remove(local_filename)


def check_tg(talkgroup):

    if config.talkgroups_allowlist == [] and config.talkgroups_denylist == []:
        return True
    
    if config.talkgroups_allowlist != []:
        if talkgroup in config.talkgroups_allowlist:
            return True
    
    if config.talkgroups_denylist != []:
        if talkgroup not in config.talkgroups_denylist:
            return True
    
    return False

async def send_talkgroup_webhook(talkgroup, filename, transcription):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(config.tg_webhooks[talkgroup], session=session)
        e = Embed(
            title=config.tg_displaynames[talkgroup],
        description=(f"{transcription}\n\n[Call Audio]({'https://' + config.s3_config['s3_endpoint'] + '/' + config.s3_config['s3_bucket'] + '/' + filename})")
        )
        await webhook.send(embed=e, username='dawn 🌅')

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(config.mqtt_config['mqtt_host'], config.mqtt_config['mqtt_port'])



# Loop forever
mqtt_client.loop_forever()
