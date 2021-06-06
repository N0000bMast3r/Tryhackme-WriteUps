> Scripting

We are given a file `base64.txt` which contains a large string base64 encoded 50 times. Let's write a python script to complete the challnege.

# challenge.py

```python
#!/usr/bin/env python

from base64 import *

file = open("b64.txt", "r")
read_file = file.read()

for i in range(0,50):
	read_file = b64decode(read_file)

file.close()
print(read_file) 
```

# Output

```
b'HackBack2019='
```

# Task 2

You need to write a script that connects to this webserver on the correct port, do an operation on a number and then move onto the next port. Start your original number at 0. The format is: operation, number, next port.

For example the website might display, add 900 3212 which would be: add 900 and move onto port 3212.
Then if it was minus 212 3499, you'd minus 212 (from the previous number which was 900) and move onto the next port 3499
Do this until you the page response is STOP (or you hit port 9765).
Each port is also only live for 4 seconds. After that it goes to the next port. You might have to wait until port 1337 becomes live again...
Start from http://10.10.21.180:3010 to start...

