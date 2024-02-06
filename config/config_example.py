# CONFIG
s3_config = {
    's3_endpoint': 's3.example.net',  # e.g., 's3.amazonaws.com'
    's3_access_key': 'ACCESS_KEY',
    's3_secret_key': 'SECRET_KEY',
    's3_bucket': 'PLEASE ONLY ONE TRUNK-RECORDER SYSTEM PER BUCKET FOR NOW THANKS'
}

mqtt_config = {
    'mqtt_host': '127.0.0.1',
    'mqtt_port': 1883,  # Default MQTT port
    'mqtt_uploaded_topic': 'trunk-recorder/uploadscript/uploaded',
    'mqtt_transcribed_topic': 'trunk-recorder/transcriber/transcribed',
    'mqtt_username': 'uploadscript',  # Optional
    'mqtt_password': '',  # Optional
}

tg_webhooks = {
    123: 'httpx://discord.com/api/webhooks/obviously-not-a-real-webhook',
    456: 'httpx://discord.com/api/webhooks/obviously-not-a-real-webhook'
}

tg_displaynames = {
    123: 'What you want the nickname of the sender in discord to be',
    456: 'Police Tac 3'
}

# If both are empty, all calls transcribed
# If denylist has entries, all but denylist transcribed
# if allowlist has entries, only listed tgs will be transcribed
talkgroups_allowlist = [123, 456]
talkgroups_denylist = []

model_name = "large-v3"  # Choose the appropriate model size and language
device_type = "cpu" # need to check ctranslate2 for documentation but assume for now that "cuda" and "cpu" are your two options.