FROM zabbix/zabbix-server-mysql:alpine-3.4-latest

RUN set -ex && \
    apk update && \
    apk add curl && \
    curl --insecure --retry 5 --max-time 5 -sSfL -o ./wait-for-it.sh https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh && \
    chmod +x ./wait-for-it.sh

ENTRYPOINT ["./wait-for-it.sh", "zabbix-mariadb:3306", "--timeout=0", "--strict", "--", "docker-entrypoint.sh"]
