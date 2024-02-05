import paho.mqtt.client as mqtt
import boto3
import os
from faster_whisper import WhisperModel
import string
import threading
from discord import Webhook
import aiohttp
import asyncio
import logging

# hopefully this imports config.py and there's not some library out there named config... that would be awkward
import config


#log config
logging.basicConfig(level=logging.INFO)

# S3 initialization
session = boto3.session.Session()
s3 = session.client(service_name='s3',
                    aws_access_key_id=config.s3_config['s3_access_key'],
                    aws_secret_access_key=config.s3_config['s3_secret_key'],
                    endpoint_url='https://' + config.s3_config['s3_endpoint'])

# faster-whisper initialization
model_name = "medium.en"  # Choose the appropriate model size and language
model = WhisperModel(model_name, device="cpu")

def on_connect(client, userdata, flags, rc):
    logging.info("MQTT Broker connected with result code " + str(rc))
    client.subscribe(config.mqtt_config['mqtt_topic'])

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

        segments, info = model.transcribe(local_filename, beam_size=5)

        fulltext = ""
        for segment in segments:
            fulltext += segment.text

        logging.debug(f"Transcription from {talkgroup} Result: {fulltext}")
        asyncio.run(send_talkgroup_webhook(talkgroup, fulltext))

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

async def send_talkgroup_webhook(talkgroup, transcription):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(config.tg_webhooks[talkgroup], session=session)
        await webhook.send(transcription, username=config.tg_displaynames[talkgroup])


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(config.mqtt_config['mqtt_host'], config.mqtt_config['mqtt_port'])



# Loop forever
client.loop_forever()


