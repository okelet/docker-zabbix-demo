#!/bin/bash

while ! nc -z -w 1 zabbix-server 10051 ; do 
    echo 'Zabbix Server not ready; waiting...'
    sleep 5
done

while ! curl -sSfL http://zabbix-web >/dev/null 2>&1 ; do 
    echo 'Zabbix Web not ready; waiting...'
    sleep 5
done

echo "Registering agent 1..."
python3.6 /zabbix-add-host.py --url=http://zabbix-web --username=Admin --password=zabbix --hostname=agent1 --address=agent1 --register-mode=by-dns --templates "Template OS Linux" --groups "Linux servers"

echo "Registering agent 2..."
python3.6 /zabbix-add-host.py --url=http://zabbix-web --username=Admin --password=zabbix --hostname=agent2 --address=agent2 --register-mode=by-dns --templates "Template OS Linux" --groups "Linux servers"

echo "Everything is OK."
