# Introduction

Onion mail delivery: *so* delicious!

## Why deliver mail over Tor?

Even if you use TLS for your connections they are opportunistic. Even if you use OpenPGP for your connections, it is relatively easy for someone passively monitoring email traffic to correlate interesting metadata: who is communicating with whom, when and how much. Worse, it is trivial for a third party to know that two people are communicating. 

By joining our little caramelized onion party, we can deliver mail over Tor onion services, and we can prevent this unauthorized privacy violation.

Let's turn out the lights and cook some onions.

## Why do it over onion services, and not just use Tor itself?

The problem with this approach is that most exit nodes are blacklisted by RBLs so it’s very probable that the emails sent will either not reach their target or will get marked as spam. 

Also with onion services you get to omit the potential of malicious exit nodes sniffing your traffic.

## Why not deliver to onion email addresses?

You could create hidden services and make users send emails to each other at their hidden service domains, eg. username@a2i4gzo2bmv9as3avx.onion. But no time in the near future will this ever get adopted by normal users, the onion address is too painful for people to remember.  The easiest approach to get things going is to setup a map of the real domains to the Tor onion services so the delivery is transparent to the users.

However, there *is* a way to deliver to onion addresses also, we need to add this information.

## Does it work?

Yes! There are many organizations that are delivering mail over onions for over 5 years now. It works dandy. We would like to do this with more of the internet.

## What does it look like?

When things are working, it looks like this:

    Nov 23 09:05:39 mx1 postfix/smtp[27831]: AA7C9411DC: to=<emailaddress@inthetortransport.map>, relay=wy6zk3pmcwiyhiao.onion[127.0.0.1]:25, delay=1414, delays=1160/249/3.2/1.5, dsn=2.0.0, status=sent (250 2.0.0 Ok: queued as E8798A0DE7)

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

## Get Tor setup

Now get [Tor going](tor.md)

# Problems

Are there problems? [Why yes there are!](problems.md)

# Help this effort

## Participate

There is a [mailing list](https://lists.immerda.ch/mailman/listinfo/onionmx) to discuss the development of this proposal.

or an IRC channel #onionmx on irc.indymedia.org

Maybe you have a better way? Create issues or pull requests!

## Advocate

Get your favorite email provider to do this, tweet at them, file a support request, get them off the clearnet!

## Get SOCKS5 native support in postfix!

What would be nice is if someone went to postfix and asked them to add native SOCKS5 support. Ideally, postfix would handle a .onion address to go through a SOCKS proxy by default.

Depending on torsocks is not an elegant solution, and if we are going to scale this it probably is better to do it more "native" than some duct-taped script.

Can you help us get SOCKS5 support in postfix?

# FAQ

## How can I test my setup

Send a mail to blackhole@onionmx.org. Delivery through onionmx will be blackholed whereas normal delivery bounces.

## How do I get on this static tor transport map?

If you got things setup, you aren't an open relay, then you should [publish a SRV record in DNS](SRV.md) and people can use that. Otherwise scaling is hard. 

However, if you can't do that, and you can prove the onion you have is valid, then make pull request for the [onion service map](sources/map.yml) to add your domain and onion service.

The ones in this file we have verified, you can trust us on that, or not.

# References

[This adventure started here](https://www.void.gr/kargig/blog/2014/05/10/smtp-over-hidden-services-with-postfix/)


