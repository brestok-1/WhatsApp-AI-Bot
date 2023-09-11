FROM python:3.10

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONBUFFERED 1

WORKDIR /WhatsApAIBot

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN chmod 755 .

COPY . .