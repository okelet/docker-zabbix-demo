#!/bin/bash

while ! nc -z -w 1 zabbix-server 10051 ; do 
    echo 'Zabbix Server not ready; waiting...'
    sleep 5
done

while ! curl --noproxy '*' -sSfL http://zabbix-web > /dev/null 2>&1 ; do 
    echo 'Zabbix Web not ready; waiting...'
    sleep 5
done

echo "Registering agent..."
http_proxy="" https_proxy="" python3 /zabbix-add-host.py --url=http://zabbix-web --username=Admin --password=zabbix --hostname=$(hostname) --address=$(hostname) --register-mode=by-dns --templates "Template OS Linux" --groups "Linux servers"

echo "Starting entry point..."
docker-entrypoint.sh
