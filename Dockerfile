FROM python:3.10 
# really wanted to use fedora, but oh well
# 3.12 doesn't work with pyAV

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD python3 main.py