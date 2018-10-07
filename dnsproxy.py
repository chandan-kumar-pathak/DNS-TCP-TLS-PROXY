#!/usr/bin/python3

import socket, threading, socketserver
from dnslib import *
import ssl, struct


class UDPHandler(socketserver.BaseRequestHandler):

    # --- echo test
    #def handle(self):
    #    data = self.request[0].strip()
    #    socket = self.request[1]
    #    print("{} wrote:".format(self.client_address[0]))
    #    print(data)
    #    socket.sendto(data.upper(), self.client_address)

    def handle(self):
        (req_data,req_socket) = self.request
        try:
            # dnslib parsing
            d = DNSRecord.parse(req_data)
 
        except Exception:
            print("%s: ERROR: Invalid DNS request" % self.client_address[0])
        else:
            # --- proxy regular dns request (test)
            #print(d)
            #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #sock.sendto(req_data, ("8.8.8.8", 53))
            #response = sock.recv(1024)
            #sock.close()
            #req_socket.sendto(response, self.client_address)
            # --- send dns over tls query
            upstream_response = dns_over_tls_query(req_data, "1.0.0.1", 853, "cloudflare-dns.com")
            req_socket.sendto(upstream_response, self.client_address)


def dns_over_tls_query(request, host, port, hostname):
    # prepend 2-byte length
    request = struct.pack("!H", len(request)) + request
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response = ""
    conn = ssl.wrap_socket(s)

    try:
        conn.connect((host, port))
    except socket.error as e:
        print("socket error: %s" % e)
    except ssl.SSLError as e:
        print("TLS error: %s" % e)
    else:
        conn.sendall(request)
        lbytes = recvSocket(conn, 2)
        if (len(lbytes) != 2):
            raise ErrorMessage("recv() on socket failed.")
        # unpack returns a tuple (https://docs.python.org/3/library/struct.html)
        resp_len, = struct.unpack('!H', lbytes)
        response = recvSocket(conn, resp_len)
        #print(response)
    finally:
        conn.close()

    return response


def recvSocket(s, numOctets):
    """Read and return numOctets of data from a connected socket"""
    response = b""
    octetsRead = 0
    while (octetsRead < numOctets):
        chunk = s.recv(numOctets-octetsRead)
        chunklen = len(chunk)
        if chunklen == 0:
            return b""
        octetsRead += chunklen
        response += chunk
    return response





if __name__ == "__main__":

  HOST, PORT = "localhost", 9999
  server = socketserver.UDPServer((HOST, PORT), UDPHandler)
  server.serve_forever()

