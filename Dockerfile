FROM python:3.11
# really wanted to use fedora, but oh well
# 3.12 doesn't work with pyAV

WORKDIR /app

COPY ./main.py /app/
COPY ./config/config_example.py /app/
COPY ./requirements.txt /app/

RUN apt update && apt install libavcodec-dev libavdevice-dev libavfilter-dev libavformat-dev libavutil-dev libswscale-dev libswresample-dev -y

RUN pip install -r requirements.txt

CMD python3 main.py