#!/usr/bin/env python3

# Check if hostname mappings in provided map.yml matches the domain's
# `_onion-mx._tcp.domain.tld.` SRV records. (see SRV.md for details)
#
# Returns errorcode corresponding to number of failed checks. (max 255 because
# we can only return unsigned byte and we don't want to accidentally wrap
# around and return success)
#
# requirements: dnspython pyyaml

import sys
import yaml, dns.resolver


if len(sys.argv) != 2:
    print("usage: {} path/to/map.yml".format(sys.argv[0]))
    exit(1)

mapfilename = sys.argv[1]
resolver = dns.resolver.Resolver()
fails = 0

with open(mapfilename, 'r') as mapfile:
    mapdata = yaml.load(mapfile)
total = sum((len(v) for k,v in mapdata.items()))

for onion,domains in mapdata.items():
    for domain in domains:
        name = "_onion-mx._tcp.{}".format(domain)
        try:
            response = resolver.query(name, "SRV")
            result = [str(x).rstrip(".").split(" ")[-1] for x in response]
            print
            if onion in result:
                print("OKAY {} -> {}".format(domain, onion))
            else:
                print("FAIL {} -> {}".format(domain, onion))
                fails += 1
        except Exception as e:
            print("FAIL {} -> {} ({})".format(domain, onion, e))
            fails += 1

# report back to the user
if total == fails:
    print("WARN no successful queries. "
          "Your DNS resolver may not work as expected.", file=sys.stderr)
else:
    print("INFO {} of {} queries failed".format(fails, total), file=sys.stderr)

exit(min(fails, 255))
