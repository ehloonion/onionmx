# Install tor

Do it the way that make you happiest.

# Configure an onion service for mail delivery

In your torrc (/etc/tor/torrc), add something like the following:

    # hidden service: hidden_mx
    HiddenServiceDir /var/lib/tor/hidden_mx
    HiddenServicePort 25

Now restart tor, and look in /var/lib/tor/hidden_mx/hostname, you will see your new onion domain name.

# Install and configure torsocks

Make sure you are using >2.0 (in 2.0 there was a getaddrinfo() bug that would make things not work).

The old version of torsocks (pre version 2) has a lot of security problems. You can use the older torsocks, it works, but it is not recommended. 

Edit /etc/tor/torsocks.conf and set the following:

    AllowInbound 1
