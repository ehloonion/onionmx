#!/usr/bin/env python

from collections import namedtuple
from os.path import dirname, abspath
import libs
import postfixrerouter
from olookup import OnionServiceLookup


class PostDNS(object):
    root_folder = dirname(dirname(abspath(__file__)))
    _default_config = "{0}/config".format(root_folder)
    _mappings_file = "{0}/sources".format(root_folder)

    def __init__(self, config_path=_default_config, map_path=_mappings_file):
        self.config = libs.config_reader(libs.find_conffile(config_path,
                                                            prefix="postdns"))
        self.mappings_path = map_path
        self.rerouters = namedtuple('rerouters', ('lazy', 'onion'))

    @property
    def myname(self):
        return self.config.get("DOMAIN", "hostname")

    @staticmethod
    def get_domain(name):
        return name.split("@")[1]

    def configure(self):
        onion_resolver = OnionServiceLookup(self.config)
        self.rerouters.lazy = postfixrerouter.LazyPostfixRerouter(
            self.config, self.mappings_path)
        self.rerouters.onion = postfixrerouter.OnionPostfixRerouter(
            self.config, onion_resolver)

    def _reroute(self, domain):
        if self.myname == domain:
            return tuple(["200 :"])
        else:
            return (self.rerouters.lazy.reroute(domain)
                    or self.rerouters.onion.reroute(domain))

    def run(self, address):
        domain = self.get_domain(address)
        routing = self._reroute(domain)
        print("\n".join(routing) if routing else "200 smtp:")


try:
    postdns = PostDNS()
    addr = libs.cross_input("")
    if addr == 'get *':
        print("200 :")
    postdns.configure()
    postdns.run(addr)
except (KeyboardInterrupt, Exception):
    print("200 :")
