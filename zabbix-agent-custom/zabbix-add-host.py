#!/usr/bin/python3.6

import argparse
import sys
from zabbix_api import ZabbixAPI, ZabbixAPIException


BY_IP = "by-ip"
BY_DNS = "by-dns"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--username', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--proxy')
    parser.add_argument('--hostname', required=True)
    parser.add_argument('--address', required=True)
    parser.add_argument('--register-mode', choices=[BY_IP, BY_DNS])
    parser.add_argument('--templates', nargs='+')
    parser.add_argument('--groups', nargs='+')
    args = parser.parse_args()

    try:
        zapi = ZabbixAPI(server=args.url, log_level=0)
        zapi.login(args.username, args.password)
    except ZabbixAPIException as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(1)

    template_ids = []
    group_ids = []
    proxy_id = None

    # Find template IDs
    for template_name in args.templates:
        templates = zapi.template.get({"filter": {"host": template_name}})
        if not templates:
            print("Template with name {template_name} not found.".format(template_name=template_name), file=sys.stderr)
            sys.exit(1)
        elif len(templates) > 1:
            print("Multiple templates found with name {template_name}.".format(template_name=template_name), file=sys.stderr)
            sys.exit(1)
        else:
            template_ids.append({"templateid": templates[0]["templateid"]})

    # Find group IDs
    for group_name in args.groups:
        groups = zapi.hostgroup.get({"filter": {"name": group_name}})
        if not groups:
            print("Group with name {group_name} not found.".format(group_name=group_name), file=sys.stderr)
            sys.exit(1)
        elif len(groups) > 1:
            print("Multiple groups found with name {group_name}.".format(group_name=group_name), file=sys.stderr)
            sys.exit(1)
        else:
            group_ids.append({"groupid": groups[0]["groupid"]})

    # Find proxy
    if args.proxy:
        proxies = zapi.proxy.get({"filter": {"host": args.proxy}})
        if not proxies:
            print("Proxy with name {proxy} not  ound.".format(proxy=args.proxy), file=sys.stderr)
            sys.exit(1)
        elif len(proxies) > 1:
            print("Multiple proxies found with name {proxy}.".format(proxy=args.proxy), file=sys.stderr)
            sys.exit(1)
        else:
            # Check host
            proxy_id = str(proxies[0]["proxyid"])

    host_data = {
        "host": args.hostname,
        "status": "0",
        "groups": group_ids,
        "templates": template_ids,
        "interfaces": [
            # Agent
            {
                "type": "1",
                "main": "1",
                "useip": "1" if args.register_mode == BY_IP else "0",
                "ip": args.address if args.register_mode == BY_IP else "",
                "dns": args.address if args.register_mode == BY_DNS else "",
                "port": "10050"
            },
            # SNMP
            {
                "type": "2",
                "main": "1",
                "useip": "1" if args.register_mode == BY_IP else "0",
                "ip": args.address if args.register_mode == BY_IP else "",
                "dns": args.address if args.register_mode == BY_DNS else "",
                "port": "161"
            },
        ]
    }
    if proxy_id:
        host_data["proxy_hostid"] = proxy_id

    # Find node
    hosts = zapi.host.get({"filter": {"host": args.hostname}})
    if hosts:
        print("Host already exists.", file=sys.stderr)
        sys.exit(1)

    res = zapi.host.create(host_data)
    print("Host created.")
