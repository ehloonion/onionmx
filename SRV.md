# Set up a SRV record

It could be like the following:

    _onionmx.tcp.example.com. 3600 IN SRV 0 5 25 fofofmumububu.onion.


One way is with the [python script](scripts/postdns.py) which replies to tcp_table lookup [1] queries by postfix. It queries the destination domain for a specific SRV record, '_onion-mx._tcp.' and if it finds a '.onion' address in the reply it gives it back to postfix to be used by the 'smtptor' service defined in master.cf. If no valid SRV record is found the mail is passed to 'smtp' service.

This gives us dynamic SRV lookups that lead to SMTP over onion addresses!

This is in a "works for me" state. DON'T use it on your production servers! 

Still Todo:

1. better handling of local destinations ('myself' variable), figure out some better way to prevent sending emails to smtptor that should actually be delivered locally.

2. add the ability to read a static map of domains to onion addresses like we were doing so far that would override, or even better, prevent doing the SRV lookup query. Has the benefit of "pinning" addresses and minimizing metadata leaked by DNS requests.

3. Tor's DNSPort does NOT support SRV record lookups. So we can't use it to hide our DNS queries directly. What we can do though is writeinstruction on how people can setup unbound that would forward TCP queries over Tor. That is easily doable with some iptables magic. What would be even better to do is to find Tor people at congress and explain to them what we're doing and why we need to be able to use SRV queries over DNSPort. 

4. make this a standalone daemon listening for TCP connections and use it directly from transport_maps instead of using postfix's 'spawn' hack.

5. rewrite the script in some more "performant" language

# Here is how

## Setup the script

Take the [postdns.py](scripts/postdns.py) script and put it in /usr/local/bin.

The script thinks you have a local resolver at 127.0.0.1:53 answering TCP queries. If not make the necessary changes. Edit the script and change 'myself' variable with your local domain. Yeah, I know you have multiple domains, look at point (a) above.


## Configure postfix

In main.cf:
   transport_maps = tcp:127.0.0.1:23000

In master.cf:
   127.0.0.1:23000 inet n n n - 0 spawn user=nobody argv=/usr/local/bin/postdns.py

