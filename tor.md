# Install tor

Do it the way that make you happiest.

# Configure an onion service for mail delivery

In your torrc (/etc/tor/torrc), add something like the following:

    # hidden service: hidden_mx
    HiddenServiceDir /var/lib/tor/hidden_mx
    HiddenServicePort 25

Now restart tor, and look in /var/lib/tor/hidden_mx/hostname, you will see your new onion domain name.

# Optional: Make it a Single Onion Service

We made an 'onion service' in the previous step, they used to be called 'hidden services', but we are not making this hidden. We want to make it known that this is associated with our domain, so if we want to optionally speed things up, we can make this onion service a 'Single Onion Service'. 

Single Onion Services are "fast, but not hidden" services. Normal onion services offer anonymity on the client *and* the service side, they take 6 hops and are slower than regular Tor connections, which are 3 hops. In our case we do not want anonymity on the service side, which cuts down the hops and speeds up the connection.

To do this you need version 0.2.9 or greater of tor, and then you set the following in your torrc:

    HiddenServiceNonAnonymousMode 1
    HiddenServiceSingleHopMode 1
    
*WARNING* If you do this, *only* single onion services are configured for this tor daemon. They can't coexist with a regular onion 
services. That means that if you are using this tor daemon for something that *does* require anonymity, do *not* use this!
    
Restart tor to get the change.

# Install and configure torsocks

Make sure you are using >2.0 (in 2.0 there was a getaddrinfo() bug that would make things not work).

The old version of torsocks (pre version 2) has a lot of security problems. You can use the older torsocks, it works, but it is not recommended. 

Edit /etc/tor/torsocks.conf and set the following:

    AllowInbound 1
