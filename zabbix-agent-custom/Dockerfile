FROM zabbix/zabbix-agent:alpine-3.4-latest

COPY docker-entrypoint-custom.sh /
COPY zabbix-add-host.py /

RUN set -ex && \
    apk update && \
    apk add curl python3 coreutils && \
    python3 -m pip install zabbix_api && \
    curl --insecure --retry 5 --max-time 5 -sSfL -o ./wait-for-it.sh https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh && \
    chmod +x ./wait-for-it.sh

ENTRYPOINT ["./wait-for-it.sh", "zabbix-web:80", "--timeout=0", "--strict", "--", "bash", "/docker-entrypoint-custom.sh"]
