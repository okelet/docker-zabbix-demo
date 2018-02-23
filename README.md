
# Docker Zabbix Demo

Full Zabbix environment (MySQL server, Zabbix server, Zabbix web UI, 2 clients and a helper).

The function of the helper is to register and configure the 2 clients in the Zabbix server, using a Python script.


## How to use

Clone the repo:

```
git clone https://github.com/okelet/docker-zabbix-demo
cd docker-zabbix-demo
```

Create the environment:

```
docker-compose up -d --build
```

Or overriding the time zone:

```
PHP_TZ=Europe/Madrid docker-compose up -d --build
```

The provision can take some minutes (mostly setting up the database); you can monitor the LOGs using the command below.

Once finished, you can access the Zabbix Web UI using the URL [http://localhost:8080](http://localhost:8080), and the username `Admin` and the password `zabbix`.

To view the LOGs:

```
docker-compose logs -f
```

Stop the environment:

```
docker-compose stop
```

Destroy the environment:

```
docker-compose rm
```


## Problems

### bash: docker-entrypoint.sh: command not found

Please ensure you don't already have an image for that container (its entrypoint has changed recently). To force the download of the new images, delete the old ones:

```
docker-compose rm -f -s
docker rmi zabbix/zabbix-server-mysql:ubuntu-3.4-latest zabbix/zabbix-web-apache-mysql:ubuntu-3.4-latest zabbix/zabbix-agent:ubuntu-3.4-latest
```
