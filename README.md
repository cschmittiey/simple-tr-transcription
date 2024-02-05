# simple-tr-transcription

this upload script and python file work together to do simple transcription using faster-whisper on trunk-recorder talkgroups. if you're using the MQTT trunk-recorder plugin, you can re-use the same broker you already have set up.

Note: for multiple systems, as the script is written now you will want multiple copies of the script with a different bucket for each system. sorry. maybe someday i'll fix that 🤷

in the trunk-recorder system config, you will want to have:
```json
      "uploadScript": "python3 whatever-you-name-the-script.py"
```

then you can run main.py on the host you want to do transcription on

TODO List:

- better multi-system support
- maybe some kind of config file
- dockerize main.py
- figure out how to have multiple workers work nicely
- rate limit transcriptions so the system doesn't get over-whelmed?
- maybe only upload talkgroups that we want transcribed? this should be configurable, maybe someone wants all the calls in s3? 
- send transcriptions over mqtt (for trunk-logger, which i'll be writing next. hoping it'll be beaver themed or something with that name)
- upload script add minimum/maximum length limits for the file maybe
