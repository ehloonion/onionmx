# Set up a SRV record

Make a DNS record like the following (replacing your domain and .onion):

    _onion-mx._tcp.example.com. 3600 IN SRV 0 5 25 fofofmumububu.onion.

Test that it is working by doing a DNS query of your domain, it should return the record:

    $ host -t srv _onion-mx._tcp.example.net
    _onion-mx._tcp.example.net has SRV record 0 5 25 fofofmumububu.onion.

# Install a tcp transport script

You need to install a script which replies to [TCP table lookup queries](http://www.postfix.org/tcp_table.5.html). 

There are two implementations of a tcp transport script, each one with instructions on how to set them up and use them
- [one in Python](https://github.com/ehloonion/onionrouter)
- [one in Go](https://git.autistici.org/ale/postfix-onion-transport)

# Configure postfix

In main.cf:

    transport_maps = tcp:127.0.0.1:23000

Discussion:

If you want to "pin" some onion transports with a [static map](sources/map.yml), because you've confirmed addresses out-of-band and don't want to leak metadata through DNS requests, you can do that by setting the [generated transport](postfix.md) map before the tcp map, like this:

    transport_maps = hash:/etc/postfix/tor_transport, tcp:127.0.0.1:23000

This will lookup the entries in the static map and resolve them, but if they aren't there, it will try a DNS SRV lookup.

Now set the following in master.cf:

    127.0.0.1:23000 inet n n n - 0 spawn user=nobody argv=/usr/local/bin/<your-tcp-transport-script>

and restart postfix.

# Test things!

Send some mail and look at your headers to see if it worked.
