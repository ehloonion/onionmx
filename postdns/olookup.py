import dns.exception
import dns.resolver
import re


class OnionServiceLookup(object):
    def __init__(self, config):
        self.config = config
        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = self.config.get("RESOLVER",
                                                    "resolver_ip").split(",")
        self.resolver.port = int(self.config.get("RESOLVER", "resolver_port"))

    @property
    def srv_record(self):
        return self.config.get("DNS", "srv_record")

    @property
    def use_tcp(self):
        return self.config.get("RESOLVER", "tcp") == "True"

    @staticmethod
    def is_onion(response):
        return re.search(r"onion\.$", response) is not None

    def _craft_format_record(self, domain):
        return "{0}{1}".format(self.srv_record, domain)

    def _map_answers(self, answers):
        return tuple(filter(self.is_onion, (str(x.target) for x in answers)))

    @staticmethod
    def _craft_output(answers):
        if answers:
            return tuple("{data}".format(data=str(x).rstrip('.'))
                         for x in answers)
        else:
            return tuple("")

    def lookup(self, domain):
        try:
            query = self.resolver.query(self._craft_format_record(domain),
                                        "SRV", tcp=self.use_tcp)
            return self._craft_output(self._map_answers(query))
        except dns.exception.DNSException:
            return tuple("")
