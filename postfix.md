# Postfix

To configure Postfix, follow these steps:

## Setup a smtptor transport in /etc/postfix/master.cf:

    smtptor    unix  -       -       n       -       -      smtp_tor
        -o smtp_dns_support_level=disabled -o smtp_tls_security_level=none


Discussion:

* smtp_tls_security_level is set to 'none' because there is already an encrypted transport over Tor (it is end to end encrypted and authenticated), if we don't need to do a second TLS handshake, we speed things up.

* smtp_dns_support_level is set to disabled is because of torsocks and postfix. What postfix does is it does a little trick. It tries to “resolve” the .onion by passing it as a numerical IP address to getaddrinfo() in libc. It says "hey libc, can you try to do “something” with this string, which I think is a numerical address?" libc looks at it, and then spits back an error code and depending on the error code, postfix knows if it is an IP or a hostname. In our case with an onion address, it fails indicating it is a hostname. Because it fails like this, it then fallsback to a DNS lookup because at that point postfix thinks it’s a hostname. Then DNS lookup fails because its UDP and postfix bails out. So if we disable DNS lookups then postfix fallsback to the libc call if it’s a hostname, which is what we want because torsocks hijacks the libc call for that and that last call was correct call to getaddrinfo(), and then torsocks works. This was changed in torsocks 2.1.0~8^2 when it started enforcing the AI_NUMERICHOST flag that is passed to getaddrinfo(), and now it does.

## Create the smtp_tor transport

Find out where your postfix daemon directory is:

    # postconf daemon_directory

Place the following into your `daemon_directory`, changing `/usr/lib/postfix` to be the `daemon_directory` you found above (with `smtp` at the end):

     #!/bin/sh

    /usr/bin/torsocks -i /usr/lib/postfix/smtp $@

Make it executable. 

Discussion:

* The `-i` flag to torsocks makes it use a different circuit for each attempt, hopefully recovering faster from Tor network errors. Unfortunately, using the `-i` flag makes torsocks *not* re-use the HS circuit, so performance will go down at the cost of delivery recovery.

## Setup a Tor transport map

In your /etc/postfix/main.cf, add a transport map:

    transport_maps = hash:/etc/postfix/tor_transport

You may already have transport maps, just add this one, separated by commas.

Then, create the transport map file by taking [the file you can find in this repository](tor_transport) and putting it in /etc/postfix/tor_transport (or the directory where you configured it above).

Then hash the map:

    postmap hash:/etc/postfix/tor_transport

## Get SOCKS5 native support in postfix!

What would be nice is if someone went to postfix and asked them to add native SOCKS5 support. Ideally, postfix would handle a .onion address to go through a SOCKS proxy by default.

Depending on torsocks is not an elegant solution, and if we are going to scale this it probably is better to do it more "native" than some duct-taped script.

Can you help us get SOCKS5 support in postfix?
