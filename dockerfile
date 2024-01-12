FROM python:3.6.8

COPY ./requirements.txt /requirements.txt
COPY ./ransom /ransom
COPY ./extractor /extractor
COPY ./pip.conf /pip.conf
RUN mkdir /root/.pip && \
    mv /pip.conf /root/.pip/pip.conf && \
    python3 -m pip install -r /requirements.txt