import json
import boto3
import aiohttp
import asyncio
import logging
import threading
import paho.mqtt.client as mqtt
from discord import Webhook, Embed

# hopefully this imports config/config.py and there's not some library out there named config... that would be awkward
import config.config as config

if config.model == "whisper":
    import models.whisper as whisper

if config.model == "canary":
    import models.canary as canary

# log config
# TODO: make this a config option
logging.basicConfig(level=logging.INFO)


def mqtt_on_connect(client, userdata, flags, rc):
    logging.info("MQTT Broker connected with result code " + str(rc))
    client.subscribe(config.mqtt_config["mqtt_uploaded_topic"])


def mqtt_on_message(client, userdata, msg):
    filename = msg.payload.decode()
    logging.debug(f"Received filename: {filename}")
    # Start a new thread for handling the transcription process
    threading.Thread(target=mqtt_handle_message, args=(filename,)).start()


def mqtt_handle_message(filename):
    talkgroup = int(filename.split("-")[0])

    if check_tg(talkgroup):
        # Download file from S3
        local_filename = f"temp_{filename}"
        s3.download_file(config.s3_config["s3_bucket"], filename, local_filename)
        logging.debug(f"Downloaded {filename} from S3")

        logging.info(f"Transcribing {filename}")
        if config.model == "whisper":
            # FasterWhisper
            fulltext = whisper.transcribe(local_filename)
        if config.model == "canary":
            fulltext = canary.transcribe(local_filename)

        # fire off discord notification unless there's no transcription text
        if fulltext:
            try:
                # Get the current event loop or create a new one if necessary
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If the loop is already running, use run_coroutine_threadsafe
                    asyncio.run_coroutine_threadsafe(
                        send_discord_webhook(talkgroup, filename, fulltext),
                        loop
                    ).result()
                else:
                    # If no loop is running, use asyncio.run
                    asyncio.run(send_discord_webhook(talkgroup, filename, fulltext))
                logging.info(f"Transcription of {filename}: {fulltext}")
            except Exception as e:
                logging.error(f"Failed to send Discord webhook: {e}")

        if not fulltext:
            logging.info(f"Transcription of {filename}: No text found.")

        # fire off mqtt notification
        # i don't really love just tossing out the file name, talkgroup, and transcription. we should ingest call data with the upload script and use that maybe?
        x = {"talkgroup": talkgroup, "filename": filename, "transcription": fulltext}
        mqtt_transcribed_payload = json.dumps(x)
        mqtt_client.publish(
            config.mqtt_config["mqtt_transcribed_topic"], mqtt_transcribed_payload
        )


def check_tg(talkgroup):
    # Should we be transcribing this talkgroup?

    if config.talkgroups_allowlist == [] and config.talkgroups_denylist == []:
        return True

    if config.talkgroups_allowlist != []:
        if talkgroup in config.talkgroups_allowlist:
            return True

    if config.talkgroups_denylist != []:
        if talkgroup not in config.talkgroups_denylist:
            return True

    return False


async def send_discord_webhook(talkgroup, filename, transcription):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(config.tg_webhooks[talkgroup], session=session)
        e = Embed(
            title=config.tg_displaynames[talkgroup],
            description=(
                f"{transcription}\n\n[Call Audio]({'https://' + config.s3_config['s3_endpoint'] + '/' + config.s3_config['s3_bucket'] + '/' + filename})"
            ),
        )
        await webhook.send(embed=e, username=config.discord_username)


# S3 initialization
session = boto3.session.Session()
s3 = session.client(
    service_name="s3",
    aws_access_key_id=config.s3_config["s3_access_key"],
    aws_secret_access_key=config.s3_config["s3_secret_key"],
    endpoint_url="https://" + config.s3_config["s3_endpoint"],
)


# mqtt initialization
mqtt_client = mqtt.Client()
mqtt_client.on_connect = mqtt_on_connect
mqtt_client.on_message = mqtt_on_message
mqtt_client.connect(config.mqtt_config["mqtt_host"], config.mqtt_config["mqtt_port"])

# Loop forever
mqtt_client.loop_forever()
