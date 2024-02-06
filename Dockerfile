FROM python:3.10
# really wanted to use fedora, but oh well

WORKDIR /app

COPY ./main.py /app/
COPY ./config/config_example.py /app/
COPY ./requirements.txt /app/

RUN apt update && apt install libavcodec-dev libavdevice-dev libavfilter-dev libavformat-dev libavutil-dev libswscale-dev libswresample-dev -y

RUN pip install -r requirements.txt

CMD python3 main.py