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

Download the [script](https://raw.githubusercontent.com/ehloonion/onionmx/master/scripts/postdns.py) and put it in /usr/local/bin and make it executable.

Install the needed dependency:

    # apt install python-dnspython

# Configure the script

Edit the script and change 'myself' variable with your local domain.

The script thinks you have a local resolver at 127.0.0.1:53 answering TCP queries. If not, make the necessary changes. 

Discussion:

The script queries the destination domain for a specific SRV record, '_onion-mx._tcp.' and if it finds a '.onion' address in the reply it gives it back to postfix to be used by the 'smtptor' service defined in master.cf. If no valid SRV record is found the mail is passed to 'smtp' service. This gives us dynamic SRV lookups that lead to SMTP over onion addresses!

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
