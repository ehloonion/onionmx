# Introduction

Onion mail delivery: so delicious!

## Why deliver mail over tor?

Even if you use TLS for your connections they are opportunistic. Even if you use OpenPGP for your connections, it is relatively easy for someone passively monitoring email traffic to correlate interesting metadata: who is communicating with whom, when and how much. Worse, it is trivial for a third party to know that two people are communicating. 

By joining our little caramelized onion party, we can deliver mail over tor onion services, and we can prevent this unauthorized privacy violation. 

Lets turn out the lights and cook some onions.

## Why do it over onion services, and not just use tor itself?

The problem with this approach is that most exit nodes are blacklisted by RBLs so it’s very probable that the emails sent will either not reach their target or will get marked as spam. 

Also with onion services you get to omit the potential of malicious exit nodes sniffing your traffic.

## Why not deliver to onion email addresses?

You could create hidden services and make users send emails to each other at their hidden service domains, eg. username@a2i4gzo2bmv9as3avx.onion. But no time in the near future will this ever get adopted by normal users, the onion address is too painful for people to remember.  The easiest approach to get things going is to setup a map of the real domains to the tor onion services so the delivery is transparent to the users.

However, there *is* a way to deliver to onion addresses also, we need to add this information.

## Does it work?

Yes. We've been doing this for over a year, and it works dandy. We would like to do this with more of the internet.

## What does it look like?

When things are working, it looks like this:

    Nov 23 09:05:39 mx1 postfix/smtp[27831]: AA7C9411DC: to=<emailaddress@inthetortransport.map>, relay=wy6zk3pmcwiyhiao.onion.onion[127.0.0.1]:25, delay=1414, delays=1160/249/3.2/1.5, dsn=2.0.0, status=sent (250 2.0.0 Ok: queued as E8798A0DE7)

# Lets do this.

Ok.

## Configure your MTA

We want to do this first, because if you don't get this setup right, you may become an open relay, that is bad.

[Postfix](postfix.md) instructions
[Exim](https://tech.immerda.ch/2016/12/ehlo-onion/)

## Make sure you aren't an open relay

Open relays are bad. Do not become one!

This is the hardest part, *and the most important*: do *not* fail to do this right.

Spend some time [making sure you aren't an open relay](open-relay.md).

## Get tor setup

Now get [Tor going](tor.md)

# Make a pull request

Now that you have configured your MTA, you've confirmed you aren't an open relay, and you've setup a tor onion service, why don't you submit a pull request for the [tor transport map](tor_transport) to add your domain. Giving some assurance that you control it would be good, or if it isn't yours, provide some details about how you determined this was a valid onion. 

This is a bit of a TOFU approach, and yes someone could mess with this. Its not perfect.

# Problems

Are there problems? [Why yes there are!](problems.md)

# A better way?

Scaling is painful, there are some ideas for improving this, such as a [SRV record](problems.md), or using the web-of-trust.

Maybe you have a better way?

# References

[This adventure started here](https://www.void.gr/kargig/blog/2014/05/10/smtp-over-hidden-services-with-postfix/)
[Single Onion Services](https://blog.torproject.org/blog/whats-new-tor-0298)

