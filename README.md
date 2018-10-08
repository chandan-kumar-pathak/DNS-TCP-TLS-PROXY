# DNS to DNS over TLS proxy

## Implementation

Listens for DNS queries on port 9999/udp and proxies them to Cloudfare's 1.0.0.1 nameserver through DNS over TLS, then sends the response back to the client.

Used the following projects as reference:

https://github.com/shuque/pydig

https://github.com/amckenna/DNSChef


## DNS security concerns 

DNS queries are sent in the clear and can be sniffed. They can also be used by some internet providers to sell data about internet activity.


## Usage in microservice architecture

Configure dnsmasq's nameserver on every microservice's host to point to the dnsproxy service.


## Possible improvements

- Currently it is single threaded, multithreading can be implemented through the ThreadingMixIn class: https://docs.python.org/3.4/library/socketserver.html#asynchronous-mixins

- Cloudfare values hardcoded, in a real world scenario we'd have several nameservers to query.

- Only listens on UDP, we could make it listen on both UDP and TCP.

- Improve error logging.


## Installation

1. Build the Docker image:

```
docker build -t dnsproxy .
```

2. Run the container:

```
docker run -p 9999:9999/udp dnsproxy
```

For testing purposes it is bound to port 9999 by default, it can be published on any other port if desired.

For local testing run with:

```
docker run --network="host" dnsproxy
```

Then it can be tested with a query to localhost:9999 nameserver:

```
$ dig @localhost -p 9999 example.com

; <<>> DiG 9.11.3-1ubuntu1.2-Ubuntu <<>> @localhost -p 9999 example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 31464
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1452
; PAD: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ("........................................................................................................................................................................................................................................................................................................................................................................................................................")
;; QUESTION SECTION:
;example.com.			IN	A

;; ANSWER SECTION:
example.com.		707	IN	A	93.184.216.34

;; Query time: 59 msec
;; SERVER: 127.0.0.1#9999(127.0.0.1)
;; WHEN: Sat Sep 29 16:18:16 CEST 2018
;; MSG SIZE  rcvd: 468
```


