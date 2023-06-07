FROM alpine

run apk add --no-cache tzdata

ENV TZ=Europe/Kiev

VOLUME /home/tg

WORKDIR /home/tg

COPY ./ /home/tg/

RUN apk add python3 \
        && python -m ensurepip --upgrade \
        && pip3 install -r requirements.txt


CMD python3 main.py
