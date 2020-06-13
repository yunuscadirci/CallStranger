FROM python:3-buster

RUN apt update && apt install git 

RUN git clone https://github.com/yunuscadirci/CallStranger.git /opt/CallStranger

RUN cd /opt/CallStranger && pip3 install -r requirements.txt

RUN groupadd -r callstranger && useradd --no-log-init -r -g callstranger callstranger \
  && chown -R callstranger:callstranger /opt/CallStranger/

USER callstranger

CMD python3 /opt/CallStranger/CallStranger.py
