
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
docker-compose up -d
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
