#!/usr/bin/env python

import re
import sys
import dns.resolver
from scripts import libs

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
myresolver.nameservers = ['127.0.0.1']
myresolver.port = 53
srv_lookup = '_onion-mx._tcp.'
onion_transport = 'smtptor'
myself = r'MYDOMAIN.net'

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
