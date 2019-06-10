# DNS to DNS over TLS proxy

## Implementation

Listens for DNS queries on port 53/tcp (In case you not able to run it on 53 try on high end ports like 9000, please change the expose port in Dockerfile and in port code) and proxies them to Cloudfare's 1.0.0.1 nameserver through DNS over TLS, then sends the response back to the client.

Used the following projects as reference:

https://github.com/shuque/pydig

https://github.com/amckenna/DNSChef

https://github.com/PowerScript/KatanaFramework/blob/master/files/dnschef/dnschef.py

https://github.com/fireeye/flare-fakenet-ng/blob/master/fakenet/listeners/DNSListener.py

https://docs.python.org/2/library/socketserver.html#SocketServer.BaseRequestHandler


## DNS security concerns 

DNS queries are sent in the clear and can be sniffed. They can also be used by some internet providers to sell data about internet activity.


## Usage in microservice architecture

Configure dnsmasq's nameserver on every microservice's host to point to the dnsproxy service.

Change the /etc/resolv.conf accordingly.

## Possible improvements

- Currently it is single threaded, multithreading can be implemented through the ThreadingMixIn class: https://docs.python.org/3.4/library/socketserver.html#asynchronous-mixins

- Currently it only work in case of TCP. It can be extended to support in case of TCP/UDP. Also we can have a check to validate the request. If it is already tls rapped forward the request as it is. 

- Cloudfare values hardcoded, in a real world scenario we'd have several nameservers to query.

- Improve error logging.


## Installation

1. Build the Docker image:

```
docker build -t dnstcpproxy_to_cf .
```

2. Run the container:

```
docker run -p 53:53/tcp dnstcpproxy_to_cf
```

For local testing run with:

```
docker run --network="host" dnsproxy
```

Then it can be tested with a query to localhost:53 nameserver:

```
$ dig +tcp @localhost -p 53 google.com

; <<>> DiG 9.11.3-1ubuntu1.7-Ubuntu <<>> +tcp @localhost -p 53 google.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 26509
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1452
; PAD: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 (".....................................................................")
;; QUESTION SECTION:
;google.com.			IN	A

;; ANSWER SECTION:
google.com.		92	IN	A	216.58.197.78

;; Query time: 97 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Mon Jun 10 09:32:47 IST 2019
;; MSG SIZE  rcvd: 128


