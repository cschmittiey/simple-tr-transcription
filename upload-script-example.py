#! /usr/bin/python3


import os
import sys
import boto3
from botocore.exceptions import NoCredentialsError
import paho.mqtt.publish as publish

# Configuration Settings
s3_config = {
    's3_endpoint': 's3.cleeb.net',  # e.g., 's3.amazonaws.com'
    's3_access_key': 'access key!',
    's3_secret_key': 'secret key!',
    's3_bucket': 'ONE BUCKET PER SYSTEM FOR NOW PLEASE THANKS',
}

mqtt_config = {
    'mqtt_host': 'ip address',
    'mqtt_port': 1883,  # Default MQTT port
    'mqtt_topic': 'your_topic/whatever',
    'mqtt_username': '',  # Optional
    'mqtt_password': '',  # Optional
}

# Function to upload a file to S3
def upload_to_s3(file_path, file_name):
    try:
        session = boto3.session.Session()
        s3 = session.client(service_name='s3',
                            aws_access_key_id=s3_config['s3_access_key'],
                            aws_secret_access_key=s3_config['s3_secret_key'],
                            endpoint_url='https://' + s3_config['s3_endpoint'])
        s3.upload_file(file_path, s3_config['s3_bucket'], file_name)
        print(f"File {file_name} uploaded to bucket {s3_config['s3_bucket']}")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

# Function to publish a message to MQTT
def publish_to_mqtt(file_name):
    auth = None
    if mqtt_config.get('mqtt_username') and mqtt_config.get('mqtt_password'):
        auth = {'username': mqtt_config['mqtt_username'], 'password': mqtt_config['mqtt_password']}
    try:
        publish.single(
            mqtt_config['mqtt_topic'],
            payload=f"{file_name}",
            hostname=mqtt_config['mqtt_host'],
            port=mqtt_config['mqtt_port'],
            auth=auth
        )
        print(f"MQTT message sent regarding {file_name}")
    except Exception as e:
        print(f"Failed to send MQTT message: {e}")

# Main execution
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    file_name = os.path.basename(file_path)

    successful_upload = upload_to_s3(file_path, file_name)
    if successful_upload:
        publish_to_mqtt(file_name)