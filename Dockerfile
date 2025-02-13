FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Install system dependencies
RUN apt update && \
    apt install -y libavcodec-dev libavdevice-dev libavfilter-dev libavformat-dev libavutil-dev libswscale-dev libswresample-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN uv pip install -r requirements.txt --break-system-packages --system

# Copy the rest of the application code
COPY . .

# Set the default command
CMD ["python3", "main.py"]
