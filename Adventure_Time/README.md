> Adventure Time

**export IP=10.10.46.65**

# Nmap

nmap -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
21/tcp    open     ftp      syn-ack     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -r--r--r--    1 ftp      ftp       1401357 Sep 21  2019 1.jpg
| -r--r--r--    1 ftp      ftp        233977 Sep 21  2019 2.jpg
| -r--r--r--    1 ftp      ftp        524615 Sep 21  2019 3.jpg
| -r--r--r--    1 ftp      ftp        771076 Sep 21  2019 4.jpg
| -r--r--r--    1 ftp      ftp       1644395 Sep 21  2019 5.jpg
|_-r--r--r--    1 ftp      ftp         40355 Sep 21  2019 6.jpg
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.8.107.21
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp    open     ssh      syn-ack     OpenSSH 7.6p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
80/tcp    open     http     syn-ack     Apache httpd 2.4.29
| http-methods: 
|_  Supported Methods: POST OPTIONS HEAD GET
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: 404 Not Found
443/tcp   open     ssl/http syn-ack     Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: POST OPTIONS HEAD GET
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: You found Finn
| ssl-cert: Subject: commonName=adventure-time.com/organizationName=Candy Corporate Inc./stateOrProvinceName=Candy Kingdom/countryName=CK/emailAddress=bubblegum@land-of-ooo.com/organizationalUnitName=CC
| Issuer: commonName=adventure-time.com/organizationName=Candy Corporate Inc./stateOrProvinceName=Candy Kingdom/countryName=CK/emailAddress=bubblegum@land-of-ooo.com/organizationalUnitName=CC
31337/tcp open     Elite?   syn-ack
| fingerprint-strings: 
|   DNSStatusRequestTCP, RPCCheck, SSLSessionReq: 
|     Hello Princess Bubblegum. What is the magic word?
|     magic word is not
|   DNSVersionBindReqTCP: 
|     Hello Princess Bubblegum. What is the magic word?
|     magic word is not 
|     version
|     bind
|   GenericLines, NULL: 
|     Hello Princess Bubblegum. What is the magic word?
|   GetRequest: 
|     Hello Princess Bubblegum. What is the magic word?
|     magic word is not GET / HTTP/1.0
|   HTTPOptions: 
|     Hello Princess Bubblegum. What is the magic word?
|     magic word is not OPTIONS / HTTP/1.0
|   Help: 
|     Hello Princess Bubblegum. What is the magic word?
|     magic word is not HELP
|   RTSPRequest: 
|     Hello Princess Bubblegum. What is the magic word?
|     magic word is not OPTIONS / RTSP/1.0
|   SIPOptions: 
|     Hello Princess Bubblegum. What is the magic word?
|     magic word is not OPTIONS sip:nm SIP/2.0
|     Via: SIP/2.0/TCP nm;branch=foo
|     From: <sip:nm@nm>;tag=root
|     <sip:nm2@nm2>
|     Call-ID: 50000
|     CSeq: 42 OPTIONS
|     Max-Forwards: 70
|     Content-Length: 0
|     Contact: <sip:nm@nm>
|_    Accept: application/sdp
```

# Nikto

nikto -h http://$IP

```
+ Apache/2.4.29 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ Allowed HTTP Methods: POST, OPTIONS, HEAD, GET 
+ OSVDB-3233: /icons/README: Apache default file found.
```

# Gobuster

sudo gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial -x php,txt,sql,bak,cgi,js,bin,tar,zip

```
Looks like we can't access http
``` 

## Gobuster for HTTPS

sudo gobuster dir -u https://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial -x php,txt,sql,bak,cgi,js,bin,tar,zip -k


```
/candybar (Status: 301)
```
We got ftp open and Anonymous login is allowed. And we can get all the images using mget. Looking though all the images we can find metadata `XP Comment` where we have biary data. And collecting it we can find that it's a rabbit hole!

for i in {1..6}; do exiftool $i.jpg | grep "XP Comment" ; done


```
01111001 01101111 01110101 00100000 01110010 01100101 01100001 01101100 01101100 01111001 00100000 01101100 01101001 01101011 01100101 00100000 01110100 01101111 00100000 01110000 01110101 01111010 01111010 01101100 01100101 00100000 01100100 01101111 01101110 00100111 01110100 00100000 01111001 01100001

Converted: you really like to puzzle don't ya
``` 

Looking at the nmap result in port 443 we can see 2 emails. And in gobuster we got a result `/candybar`.

Looking there we got an encoded string. `<!-- KBQWY4DONAQHE53UOJ5CA2LXOQQEQSCBEBZHIZ3JPB2XQ4TQNF2CA5LEM4QHEYLKORUC4=== -->`

It's encoded in Base32 and again we got to check caesar cipher to get the output.

echo "KBQWY4DONAQHE53UOJ5CA2LXOQQEQSCBEBZHIZ3JPB2XQ4TQNF2CA5LEM4QHEYLKORUC4===" | base32 -d  = cipher; for i in {0..25}; do echo $cipher | caesar $i; done


```
Palpnh rwtrz iwt HHA rtgixuxrpit udg rajth.
Qbmqoi sxusa jxu IIB suhjyvysqju veh sbkui.
Rcnrpj tyvtb kyv JJC tvikzwztrkv wfi tclvj.
Sdosqk uzwuc lzw KKD uwjlaxauslw xgj udmwk.
Teptrl vaxvd max LLE vxkmbybvtmx yhk venxl.
Ufqusm wbywe nby MMF wylnczcwuny zil wfoym.
Vgrvtn xczxf ocz NNG xzmodadxvoz ajm xgpzn.
Whswuo ydayg pda OOH yanpebeywpa bkn yhqao.
Xitxvp zebzh qeb PPI zboqfcfzxqb clo zirbp.
Yjuywq afcai rfc QQJ acprgdgayrc dmp ajscq.
Zkvzxr bgdbj sgd RRK bdqshehbzsd enq bktdr.
Always check the SSL certificate for clues. => We got the answer!!!
Bmxbzt difdl uif TTM dfsujgjdbuf gps dmvft.
Cnycau ejgem vjg UUN egtvkhkecvg hqt enwgu.
Dozdbv fkhfn wkh VVO fhuwlilfdwh iru foxhv.
Epaecw gligo xli WWP givxmjmgexi jsv gpyiw.
Fqbfdx hmjhp ymj XXQ hjwynknhfyj ktw hqzjx.
Grcgey inkiq znk YYR ikxzoloigzk lux iraky.
Hsdhfz joljr aol ZZS jlyapmpjhal mvy jsblz.
Iteiga kpmks bpm AAT kmzbqnqkibm nwz ktcma.
Jufjhb lqnlt cqn BBU lnacrorljcn oxa ludnb.
Kvgkic mromu dro CCV mobdspsmkdo pyb mveoc.
Lwhljd nspnv esp DDW npcetqtnlep qzc nwfpd.
Mximke otqow ftq EEX oqdfuruomfq rad oxgqe.
Nyjnlf purpx gur FFY pregvsvpngr sbe pyhrf.
Ozkomg qvsqy hvs GGZ qsfhwtwqohs tcf qzisg.
```

According to the clue looking at the SSL Certificate's issuer we can find the same 2 mail ids . Let's try to add them to our /etc/hosts file. 

```
E = bubblegum@land-of-ooo.com
CN = adventure-time.com
OU = CC
O = Candy Corporate Inc.
ST = Candy Kingdom
C = CK
```

And accessing `https://land-of-ooo.com/` gives us the next hint!! 

# Again Enumeration

sudo gobuster dir -u https://land-of-ooo.com/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/land_of_ooo -k

```
/yellowdog
```

sudo gobuster dir -u https://land-of-ooo.com/yellowdog/ -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -t 20 -o gobuster/land_of_ooo/yellowdog -k

```
/bananastock
```

Here we got morse code and decoding it we get a password!! `THE BANANAS ARE THE BEST!!!`

sudo gobuster dir -u https://land-of-ooo.com/yellowdog/bananastock/ -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -t 20 -o gobuster/land_of_ooo/yellowdog -k

```
/princess
```

    <!--
    Secrettext = 0008f1a92d287b48dccb5079eac18ad2a0c59c22fbc7827295842f670cdb3cb645de3de794320af132ab341fe0d667a85368d0df5a3b731122ef97299acc3849cc9d8aac8c3acb647483103b5ee44166
    Key = my cool password
    IV = abcdefghijklmanopqrstuvwxyz
    Mode = CBC
    Input = hex
    Output = raw
    -->

Looks like it is AES. And decoding it we get `the magic safe is accessibel at port 31337. the magic word is: ricardio`

nc $IP 31337

`The new username is: apple-guards`

Now we can SSH in as apple-guards. We got flag 1.

# Flag 1

```

```

We can find a file mbox.

```
From marceline@at  Fri Sep 20 16:39:54 2019
Return-Path: <marceline@at>
X-Original-To: apple-guards@at
Delivered-To: apple-guards@at
Received: by at.localdomain (Postfix, from userid 1004)
	id 6737B24261C; Fri, 20 Sep 2019 16:39:54 +0200 (CEST)
Subject: Need help???
To: <apple-guards@at>
X-Mailer: mail (GNU Mailutils 3.4)
Message-Id: <20190920143954.6737B24261C@at.localdomain>
Date: Fri, 20 Sep 2019 16:39:54 +0200 (CEST)
From: marceline@at

Hi there bananaheads!!!
I heard Princess B revoked your access to the system. Bummer!
But I'll help you guys out.....doesn't cost you a thing.....well almost nothing.

I hid a file for you guys. If you get the answer right, you'll get better access.
Good luck!!!!
```

So we want to find a file owned by marceline.

find / -user marceline -type f 2>/dev/null

```
/etc/fonts/helper
```

It is an ELF 63 file. And executing it we got a message

```
Hi there bananaheads!!!
So you found my file?
But it won't help you if you can't answer this question correct.
What? I told you guys I would help and that it wouldn't cost you a thing....
Well I lied hahahaha

Ready for the question?

The key to solve this puzzle is gone
And you need the key to get this readable: Gpnhkse

Did you solve the puzzle? yes

What is the word I'm looking for?Abadeer => This is Viginere cipher Key: gone and Cipher: Gpnhkse

That's it!!!! You solved my puzzle
Don't tell princess B I helped you guys!!!
My password is 'My friend Finn'
```

# Flag 2

```
tryhackme{N1c30n3Sp0rt}
```

We got a file `I-got-a-secret.txt`. Looks like binary but it ain't. It is Spoon language. Decoding it we got `The magic word you are looking for is ApplePie`

Again connecting through nc we got a message `The password of peppermint-butler is: That Black Magic`.

# Flag 3

```
tryhackme{N0Bl4ckM4g1cH3r3}
```

We got an image and let's move it to our local system. 

We can't crack it using steghide using no password. So let's search for files owned by `peppermint-butler`.

find / -user peppermint-butler -type f 2>/dev/null

```
/usr/share/xml/steg.txt
/etc/php/zip.txt
```

## Contents of steg.txt

```
I need to keep my secrets safe.
There are people in this castle who can't be trusted.
Those banana guards are not the smartest of guards.
And that Marceline is a friend of princess Bubblegum,
but I don't trust her.

So I need to keep this safe.

The password of my secret file is 'ToKeepASecretSafe'
``` 

## Conetents of zip.txt

```
I need to keep my secrets safe.
There are people in this castle who can't be trusted.
Those banana guards are not the smartest of guards.
And that Marceline is a friend of princess Bubblegum,
but I don't trust her.

So I need to keep this safe.

The password of my secret file is 'ThisIsReallySave'
```

steghide extract -sf butler-1.jpg => password: `ToKeepASecretSafe`