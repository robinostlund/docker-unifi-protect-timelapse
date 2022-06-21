FROM alpine:latest

LABEL org.opencontainers.image.authors="Robin Ostlund <me@robinostlund.name>"

ENV CRON=

RUN apk -U add ca-certificates wget dcron tzdata bash python3 \
    && rm -rf /var/cache/apk/* \
    && cd /tmp

COPY scripts/entrypoint.sh /entrypoint.sh
COPY scripts/app.sh /root/app.sh
COPY source/app.py /root/app.py

# pip
COPY source/requirements.txt /tmp/requirements.txt
RUN python3 -m ensurepip \
    && pip3 install --upgrade pip \
    && pip3 install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

VOLUME ["/storage"]

ENTRYPOINT ["/entrypoint.sh"]

CMD [""]