# Open relay

When you setup a Tor hidden service to accept connections to your SMTP server, you need to be careful that you aren't opening your mail server up to be an open relay on the Tor network (double plus bad).  You need to very carefully inspect your configuration to see if you are allowing 127.0.0.1 connections to relay mail, and if you are.

Here are a couple ways to stop it in Postfix:

By default, in postfix, you are allowing `127.0.0.1/8` in `mynetworks` and `smtpd_recipient_restrictions` set to `permit_mynetworks`. The Tor hidden service will connect via 127.0.0.1, so if you allow that to send without authentication, you are an open mail relay on the Tor network: fun times.

There are a few ways of dealing with this. 

### Option 1: Remove 127.0.0.1 from mynetworks and remove mynetworks from smtpd_relay_restrictions

We looked at our setup and determined that any local process that needs to send mail should use sendmail/maildrop and not SMTP via the loopback address. We were originally worried that this wasn't the case, but after disabling this, we have not found any problems.

So we removed 127.0.0.1 from mynetworks, and then used the newer postfix variable that was designed for restricting relays:

~~~
smtpd_relay_restrictions = permit_sasl_authenticated,
        reject_unauth_destination

smtpd_recipient_restrictions =
        reject_unknown_recipient_domain,
        check_recipient_access /etc/postfix/recipient_access,
        permit_sasl_authenticated,
        permit_mynetworks,
        permit
~~~

*Do not* just copy and paste the above, you should carefully review your restrictions to make sure they are right for you.

### Option 2: Use a secondary postfix transport with a different set of restrictions

Another way is to send all mail through a secondary transport that has a different set of restrictions:

~~~
/etc/postfix/master.cf
2525      inet  n       -       -       -       -       smtpd

2587 inet n - - - - smtpd
        -o smtpd_enforce_tls=yes
        -o smtpd_tls_security_level=encrypt
        -o smtpd_sasl_auth_enable=yes
        -o smtpd_client_restrictions=permit_sasl_authenticated,reject
        -o smtpd_sender_restrictions=
~~~

Next specify that Tor should redirect connections to .onion:25 to 2525, .onion:587 to 2587 like so in tor/torrc:

    HiddenServiceDir /var/lib/tor/mailserver
    HiddenServicePort 25 2525
    HiddenServicePort 587 2587

### Option 3: Use different IP endpoint for Tor and exclude this IP from mynetworks

Another way to solve this is by:

1. Adding 127.0.0.25 to inet_interfaces in main.cf.
2. Use 127.0.0.1 in mynetworks in main.cf and not 127.0.0.1/8
3. Changing torrc to point to 127.0.0.25.
4. Adding 127.0.0.25 to lo in /etc/network/interfaces:
   auto lo
   iface lo inet loopback
     up ip addr add 127.0.0.25 dev $IFACE || true

### Option 4: Use different port for submission through Tor and prohibit mail transmission to port 25 with extra variable 

Another way is to let postfix listen to a different port than 25 for submission through Tor while not permitting localhost sending through that port: 

1. Configure 2525 in postfix/master.cf

~~~
    2525      inet  n       -       -       -       -       smtpd
        -o smtpd_recipient_restrictions=permit_sasl_authenticated,reject_unauth_destination,reject_non_fqdn_recipient,reject_unknown_recipient_domain,$custom_value2,$custom_value3,permit
        -o smtpd_sender_restrictions=permit_sasl_authenticated,reject_non_fqdn_sender,reject_unknown_sender_domain,reject_unauth_pipelining,reject_sender_login_mismatch,reject_unlisted_sender,$custom_value1,permit
~~~

*NOTE:* sender restrictions matter here! *Beware*: there can't be whitespace in the argument passed to -o, so if you need spaces in there, better define a variable in main.cf (eg. $tor_smtpd_relay_restrictions) and use it in master.cf. 

Next specify that Tor should redirect connections to .onion:25 to 2525 like so in tor/torrc:

    HiddenServiceDir /var/lib/tor/mailserver
    HiddenServicePort 25 2525


# Test it!

Check out [swaks](http://www.jetmore.org/john/code/swaks/) to test you are good. Needed a step-by-step here to make this easier.
