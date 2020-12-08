#!/bin/bash

cat wordlist.txt | while read -r line; do printf %s "$line" | md5sum | cut -f1 -d' '; done > password.lst