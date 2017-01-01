#!/usr/bin/env python

import re
import sys
import os
import dns.resolver
from scripts import libs


config_path = "{0}/config".format(os.path.dirname(os.path.dirname(__file__)))

myresolver = dns.resolver.Resolver()

name = libs.cross_input("")
if name == 'get *':
    print("200 :")
    sys.exit(0)
try:
    domain = name.split("@")[1]
except:
    print("200 :")
    sys.exit(0)

# VARIABLES
config = libs.config_reader(libs.find_conffile(config_path, prefix="postdns"))
myresolver.nameservers = config["RESOLVER"]["resolver_ip"].split(",")
myresolver.port = int(config["RESOLVER"]["resolver_port"])
srv_lookup = config["DNS"]["srv_record"]
onion_transport = config["REROUTE"]["onion_transport"]
myself = config["DOMAIN"]["hostname"]

# magic
record = srv_lookup + domain

if not re.search(myself, record):
    try:
        answers = myresolver.query(record, 'SRV', tcp=True)
        for rdata in answers:
            if re.search(r'onion\.$', str(rdata.target)):
                print("200 {onion_tp}:[{data}]"
                      .format(onion_tp=onion_transport,
                              data=str(rdata.target).rstrip('.')))
            else:
                print("200 smtp:")
    except:
        print("200 smtp:")
else:
    print("200 :")
    sys.exit(0)
