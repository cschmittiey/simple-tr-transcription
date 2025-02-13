FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY . /app/

RUN apt update && apt install libavcodec-dev libavdevice-dev libavfilter-dev libavformat-dev libavutil-dev libswscale-dev libswresample-dev -y
RUN uv pip install -r requirements.txt --break-system-packages

CMD python3 main.py
