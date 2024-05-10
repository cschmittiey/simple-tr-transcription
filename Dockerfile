FROM python:3.12
# really wanted to use fedora, but oh well

WORKDIR /app

COPY . /app/

RUN apt update && apt install libavcodec-dev libavdevice-dev libavfilter-dev libavformat-dev libavutil-dev libswscale-dev libswresample-dev -y

RUN pip install -r requirements.txt

CMD python3 main.py