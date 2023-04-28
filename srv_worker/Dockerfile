FROM python:3.10.10

WORKDIR /opt/app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONPATH="/opt/app:$PYTHONPATH"


RUN apt-get update \
    && apt-get install -y netcat \
    && apt-get install -y gettext

COPY requirements.txt requirements.txt
COPY run.sh run.sh

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i 's/\r$//g' /opt/app/run.sh \
    && chmod +x  /opt/app/run.sh