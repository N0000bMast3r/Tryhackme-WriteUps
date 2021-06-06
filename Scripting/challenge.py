#!/usr/bin/env python

from base64 import *

file = open("b64.txt", "r")
read_file = file.read()

for i in range(0,50):
	read_file = b64decode(read_file)

file.close()
print(read_file)