# simple-tr-transcription

This project aims to provide a simple(r) alternative to trunk-transcribe for people who want to transcribe just a couple talkgroups. 

> [!IMPORTANT]
> Please note that until I get an extra nvidia GPU to test with, this project has only been tested with CPU transcription.

## Requirements
- A working trunk-recorder setup
- s3 storage, for your calls you want to transcribe
- an mqtt broker. if you are already using the trunk-recorder mqtt status plugin, you can re-use the same broker
- python3, pip (note that 3.12 seems to have issues - try 3.10 or 3.11)

## Usage

Create `config.py`  in config/ using the `config_example.py` as your guide.

Install the needed python libraries:
`pip install -r requirements.txt`

Then give `python3 main.py` a shot!

Once that is running, edit `upload-script-example.py` to point at the right s3 bucket and mqtt broker, and configure your trunk-recorder instance to run this script when systems you want to transcribe have calls:

```json
      "uploadScript": "python3 whatever-you-name-the-script.py"
```

> [!NOTE]
> if the upload script is not running on the same host, you will need to run `pip3 install boto3 paho_mqtt` or else the script will complain.

## docker usage
I recommend making a folder to run this in but it's up to you.
for example:
```sh 
mkdir transcription
cd transcription
wget https://github.com/cschmittiey/simple-tr-transcription/blob/main/docker-compose.yml
mkdir config
wget https://github.com/cschmittiey/simple-tr-transcription/blob/main/config/config_example.py -o config/config.py

## edit your config file at this point

docker compose up -d # start up the container in the background
docker compose logs -f # to watch the logs

```

Docker compose example if you know what you're doing:
```
services:
  transcription:
    #build: .
    image: gchr.io/cschmittiey/simple-tr-transcription:latest
    restart: unless-stopped
    volumes:
      - ./config:/app/config
```

## 
> [!IMPORTANT]
> for multiple systems, as the script is written now you will want multiple copies of the script with a different S3 bucket for each system. sorry. maybe someday i'll fix that 🤷

## TODO List:

- multi-system support
- figure out how to have multiple workers work nicely
- rate limit transcriptions so the system doesn't get over-whelmed?
- maybe only upload talkgroups that we want transcribed? this should be configurable, maybe someone wants all the calls in s3? 
- upload script add minimum/maximum length limits for the file maybe
- better readme, lol
