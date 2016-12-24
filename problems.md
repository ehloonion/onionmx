# Problems

There are much better ways to provide secure email, unfortunately none of them is ready to use yet. In an effort to not let the perfect be the enemy of the good, we will do this for a while, improve it and eventually we will switch to something better.

Do not be fooled, this is not a panacea. We do get a defense against traffic timing attackers who are watching one SMTP server, but not the other. It also doesn't hide your server.

Maintaining a transport map for the entire internet is not going to work. Scaling is a problem, a big problem. We could [setup a SRV record](SRV.md).

"But it's dns...". Well yes, but standard transport is now also over MX DNS lookups, so we don't improve the situation in terms of trustworthiness of the delivery destination, but we'll heavily improve the transport itself in the non tampered situation.

If the goal is to solely improve transport, then this does improve things. Exchanging .onion addresses on a non-secure channel out-of-band gives you no guarantee of authentication and endpoint validation. If you have no guarantee (for some values of trust) that the .onion I'm getting from the DNS server for any arbitrary domain is the real one, you can NOT rely on any  security properties that hidden service offers except e2e encryption and anonymity. The question is, is this an improvement over the clearnet?

When you send mail over the clearnet, you do a DNS resolution, then you connect and then you do SSL "validation". Where "validation" is some kind of TLS cert that is bound to the domain in the MX and is connected to an agreed on root chain (*cough*certificate mafia*cough*). If I'm an attacker, currently I need to do _two_ things, DNS hijack and have a valid SSL cert for that domain.

With OnionMX you DNS resolve your onion SRV, and then that is it, an attacker just needs to DNS hijack the MX resolution and send a different .onion address for delivery, and job done.

In the first case you have to do two things, but in the OnionMX SRV record lookup, you have to do only DNS hijacking.

In the clearnet situation, you can also do DNS hijack the MX resolution, but if you are an attacker that is able to tamper with clearnet connection betweek 2 MTAs, but not with the senders DNS forward lookups, you won't succeed with the OnionMX approach. So the attack still works when you somehow are able to control results for the sender's lookups.

With email, TLS is basically broken: nobody actually verifies fingerprints. If you do, you break most delivery on the internet, you have to allow NO ssl at all, or untrusted certs, or unverified certs, or broken chain certs, etc. As the postfix documentation says:

          You can ENFORCE the use of TLS, so that the Postfix SMTP server
          announces STARTTLS and accepts no mail without TLS encryption, by
          setting "smtpd_tls_security_level = encrypt". According to RFC
          2487 this MUST NOT be applied in case of a publicly-referenced
          Postfix SMTP server. This option is off by default and should
          only seldom be used.

So we are back to the same problem. The only way to be sure via TLS is that we pin TLS FPs (after some validation) and how do you maintain a growing list of cert fingerprints and distribute them among n number of participants? So, if the goal is to solely improve transport, then yes it does improve that, but you cannot rely on authentication or endpoint validation (as a Tor client I have a GUARANTEE that the endpoint is the service I want)... the question is if this is worse.

I'm not sure you get anything additional with clearnet+TLS. You *do* get cert validation, if you have one and the remote is configured to validate, but if you don't have one, it just will be fine with that. Also if the DNS is hijacked, the client wont care if the cert suddenly disappeared. The internet is designed not to do that...  on clearnet: i can make a TLS cert and set my MTA to use that, and then someone hijacks my DNS and redirects my mail somewhere else, and the remote MTAs will just happily continue delivering (unless they have pinned the FP of the cert and set the value to say it MUST be TLS and MUST be this cert).

For e2e we are talking about pinning .onion vs. pinning TLS fingerprints, but not hiding metadata/anonymity. You also have to do a DNS SRV record lookup in the clearnet, so you will leak something (although its pretty small and that result is cached. 

Pinning certificate key fingerprints on top of this would improve things. 
