# Set up a SRV record

Make a DNS record like the following (replacing your domain and .onion):

    _onion-mx._tcp.example.com. 3600 IN SRV 0 5 25 fofofmumububu.onion.

Test that it is working by doing a DNS query of your domain, it should return the record:

    $ host -t srv _onion-mx._tcp.example.net
    _onion-mx._tcp.example.net has SRV record 0 5 25 fofofmumububu.onion.

# Install a tcp transport script

You need to install a script which replies to [TCP table lookup queries](http://www.postfix.org/tcp_table.5.html). 

This will detail how to get the python script working, but there is also
a [go implementation](https://git.autistici.org/ale/postfix-onion-transport), which is probably more performant.

Download the [script](https://raw.githubusercontent.com/ehloonion/onionmx/master/postdns/postdns.py) and put it in /usr/local/bin and make it executable.

Install the needed dependency:

    # apt install python-dnspython
    # apt install python-yaml
If working with virtualenvs, `pip install -r <project_path>/requirements.txt`

# Configure the script

Create a copy of the postdns.ini file and rename it postdns.local.ini to avoid tampering with the reference config (if no postdns.local.ini exists, the reference config will be used)

Edit the config file and change

- under the `DOMAIN` section the `hostname` field with your local domain
- under the `RESOLVER` section the `resolver_ip` field with your resolver (default is 127.0.0.1)
    - to use multiple resolvers, seperate them with comma `,`
- under the `RESOLVER` section the `resolver_port` field with the port your resolver listens (default is 53)

The script queries the destination domain for a specific SRV record, `_onion-mx._tcp.` and if it finds a `.onion` address in the reply it gives it back to postfix to be used by the `smtptor` service defined in `master.cf`. If no valid SRV record is found the mail is passed to `smtp` service. This gives us dynamic SRV lookups that lead to SMTP over onion addresses!

- To change the SRV record the scripts looks for, edit the config file mentioned above and change under the `DNS` section the `srv_record` field with the SRV record you have setup (default is `_onion-mx._tcp.`)
- To change the service that will be used when a `.onion` address is found,  edit the config file mentioned above and change under the `REROUTE` section the `onion_transport` field with the service you want to be used (default is `smtptor`)


## Static resolution option

Static lookups are supported with two different ways:

1. Through the [postdns script](postdns/postdns.py)
    - In yaml format in the `sources` folder
        - Project already contains [a yaml file](sources/map.yml) which has some predefined mappings
    - Anything in the `sources` folder will be treated as a yaml file serving the static resolution (multiple files supported)
    - To add your own mappings, you can create your own yaml file in the `sources` folder either manually or by running [the generation script you can find
    in this repository](scripts/map2postfix-transport.rb)
2. [Directly in the postfix level](#configure-postfix)

# Configure postfix

In main.cf:

    transport_maps = tcp:127.0.0.1:23000

Discussion:

If you want to "pin" some onion transports with a [static map](sources/map.yml), because you've confirmed addresses out-of-band and don't want to leak metadata through DNS requests, you can do that by setting the [generated transport](postfix.md) map before the tcp map, like this:

    transport_maps = hash:/etc/postfix/tor_transport, tcp:127.0.0.1:23000

This will lookup the entries in the static map and resolve them, but if they aren't there, it will try a DNS SRV lookup.

Now set the following in master.cf:

    127.0.0.1:23000 inet n n n - 0 spawn user=nobody argv=/usr/local/bin/postdns.py

and restart postfix.

# Test things!

Send some mail and look at your headers to see if it worked.
