# Volatiity Notes

## Task 1

Deploy the machine.

## Task 2

1. What memory format is the most common?

```
.raw
```

2. What file contains Windows compressed memory image?

```
hiberfil.sys
```

3. How about if we wanted to perform memory forensics on a VMware-based virtual machine?

```
.vmem
```

## Task 3

1. Examining the file.

volatility -f cridex.vmem imageinfo
```
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : WinXPSP2x86, WinXPSP3x86 (Instantiated with WinXPSP2x86)
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/n00bmas3r/Harsha/THM/Volatility/memory_image/cridex.vmem)
                      PAE type : PAE
                           DTB : 0x2fe000L
                          KDBG : 0x80545ae0L
          Number of Processors : 1
     Image Type (Service Pack) : 3
                KPCR for CPU 0 : 0xffdff000L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2012-07-22 02:45:08 UTC+0000
     Image local date and time : 2012-07-21 22:45:08 -0400
```

2. What profile is correct for our image?

```
sudo volatility -f cridex.vmem --profile=WinXPSP2x86 pslist 
Volatility Foundation Volatility Framework 2.6.1
Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0x823c89c8 System                    4      0     53      240 ------      0                                                              
0x822f1020 smss.exe                368      4      3       19 ------      0 2012-07-22 02:42:31 UTC+0000                                 
0x822a0598 csrss.exe               584    368      9      326      0      0 2012-07-22 02:42:32 UTC+0000                                 
0x82298700 winlogon.exe            608    368     23      519      0      0 2012-07-22 02:42:32 UTC+0000                                 
0x81e2ab28 services.exe            652    608     16      243      0      0 2012-07-22 02:42:32 UTC+0000                                 
0x81e2a3b8 lsass.exe               664    608     24      330      0      0 2012-07-22 02:42:32 UTC+0000                                 
0x82311360 svchost.exe             824    652     20      194      0      0 2012-07-22 02:42:33 UTC+0000                                 
0x81e29ab8 svchost.exe             908    652      9      226      0      0 2012-07-22 02:42:33 UTC+0000                                 
0x823001d0 svchost.exe            1004    652     64     1118      0      0 2012-07-22 02:42:33 UTC+0000                                 
0x821dfda0 svchost.exe            1056    652      5       60      0      0 2012-07-22 02:42:33 UTC+0000                                 
0x82295650 svchost.exe            1220    652     15      197      0      0 2012-07-22 02:42:35 UTC+0000                                 
0x821dea70 explorer.exe           1484   1464     17      415      0      0 2012-07-22 02:42:36 UTC+0000                                 
0x81eb17b8 spoolsv.exe            1512    652     14      113      0      0 2012-07-22 02:42:36 UTC+0000                                 
0x81e7bda0 reader_sl.exe          1640   1484      5       39      0      0 2012-07-22 02:42:36 UTC+0000                                 
0x820e8da0 alg.exe                 788    652      7      104      0      0 2012-07-22 02:43:01 UTC+0000                                 
0x821fcda0 wuauclt.exe            1136   1004      8      173      0      0 2012-07-22 02:43:46 UTC+0000                                 
0x8205bda0 wuauclt.exe            1588   1004      5      132      0      0 2012-07-22 02:44:01 UTC+0000 
```

3. What is the PID of smss.exe?

```
368
```
 
 4. Scan the network

 ```
 No answer needed
 ``` 

 5. View hidden processes using psxview command. What process has only 1 false?

```
sudo volatility -f cridex.vmem --profile=WinXPSP2x86 psxview | grep -i "False"Volatility Foundation Volatility Framework 2.6.1
0x024f1020 smss.exe                368 True   True   True     True   False False   False    
0x025c89c8 System                    4 True   True   True     True   False False   False    
0x024a0598 csrss.exe               584 True   True   True     True   False True    True     
```

6. Find hidden proccesses using ldrmodules and find which process is hidden?

sudo volatility -f cridex.vmem --profile=WinXPSP2x86 ldrmodules | grep -i "False"


```
csrss.exe
```

7. Use the apihooks command to view unexpected patches in standard DLLs.

```
apihooks_result.txt
```

8. Use `malfind` to find the dump the injected code.

```
sudo volatility -f cridex.vmem --profile=WinXPSP2x86 malfind -D /tmp

And 12 files have been generated.
```

9. Listing all DLLS in memoory.

```
sudo volatility -f ../cridex.vmem --profile=WinXPSP2x86 dlllist
```

10. Dump the DLL's.

```
sudo volatility -f ../cridex.vmem --profile=WinXPSP2x86 --pid=584 dlldump
```

## Task 4

1. What is the malware?

```
Cridex
```