> ZTH Web 2

# IDOR

IDOR, or Insecure Direct Object Reference, is the act of exploiting a misconfiguration in the way user input is handled, to access resources you wouldn't ordinarily be able to access.

For example, let's say we're logging into our bank account, and after correctly authenticating ourselves, we get taken to a URL like this https://example.com/bank?account_number=1234. On that page we can see all our important bank details, and a user would do whatever they needed to do and move along their way thinking nothing is wrong.

There is however a potentially huge problem here, a hacker may be able to change the account_number parameter to something else like 1235, and if the site is incorrectly configured, then he would have access to someone else's bank information.

We can login to `http://10.10.134.226` using creds `noot` :`test1234`. And we have an URL as `http://10.10.134.226/note.php?note=1`. Of we change the URL parameter `note` to 0 we are given the flag. 

# Flag

```
flag{fivefourthree} 
```

# Forced Browsing

Forced browsing is the art of using logic to find resources on the website that you would not normally be able to access. For example let's say we have a note taking site, that is structured like this. http://example.com/user1/note.txt. It stands to reason that if we did http://example.com/user2/note.txt we may be able to access user2's note. 

Taking this a step further, if we ran wfuzz on that url, we could enumerate users we don't know about, as well as get their notes. This is quite devastating, because we can then run further attacks on the users we find, for example bruteforcing each user we find, to see if they have weak passwords.

# Target : Port 81

We can login using the same credentials and we have the link as `http://10.10.134.226:81/noot/note.txt`. Let's fuzz to find the flag.

wfuzz -c -z file,/usr/share/wordlists/dirb/big.txt --hw 57 http://10.10.134.226:81/FUZZ/note.txt

```
password
```

Accessing `http://10.10.134.226:81/password/note.txt` we got the flag!

# Flag

```
flag{forcednooting}
```

# API Bypassing

# Target URL : http://10.10.134.226:82/

Accessing `http://10.10.134.226:82/flag.txt` we got the flag.

```
flag{test1234}
```