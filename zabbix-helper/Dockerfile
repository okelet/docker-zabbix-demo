FROM ubuntu:artful

COPY docker-entrypoint.sh /
COPY zabbix-add-host.py /

RUN set -ex \
    && apt-get update -qq && \
    apt-get install -y -qq \
    netcat-openbsd curl wget python3-pip python3.6

RUN python3.6 -m pip install zabbix_api

ENTRYPOINT ["bash", "/docker-entrypoint.sh"]
