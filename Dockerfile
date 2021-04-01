FROM python:alpine

ENV FLASK_APP microblog.py
#ENV http_proxy=http://myproxy:port
#ENV https_proxy=http://myproxy:port

RUN apk --no-cache add gcc g++ musl-dev

RUN adduser -D microblog

WORKDIR /home/microblog

COPY requirements.txt requirements.txt
COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./

RUN pip install -r requirements.txt && \
    pip install gunicorn pymysql && \
    chown -R microblog:microblog ./ && \
    chmod +x boot.sh

EXPOSE 5000

USER microblog

#RUN unset http_proxy https_proxy

ENTRYPOINT ["./boot.sh"]
