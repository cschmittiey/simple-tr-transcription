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


"""
Size of the model to use (tiny, tiny.en, base, base.en,
small, small.en, medium, medium.en, large-v1, large-v2, large-v3, or large),
a path to a converted model directory, or a CTranslate2-converted Whisper model ID from the HF Hub. 
When a size or a model ID is configured, the converted model is downloaded from the Hugging Face Hub.
"""
model_name = "large-v3" 
device_type = "cpu" # Device to use for computation ("cpu", "cuda", "auto").

