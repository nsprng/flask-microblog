FROM python:3.6-alpine

ENV FLASK_APP microblog.py
#ENV http_proxy=http://myproxy:port
#ENV https_proxy=http://myproxy:port

RUN adduser -D microblog

WORKDIR /home/microblog

COPY requirements.txt requirements.txt
COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./

RUN python -m venv venv && \
    venv/bin/pip install -r requirements.txt && \
    venv/bin/pip install gunicorn pymysql && \
    chown -R microblog:microblog ./ && \
    chmod +x boot.sh

EXPOSE 5000

USER microblog

#RUN unset http_proxy && unset https_proxy

ENTRYPOINT ["./boot.sh"]
