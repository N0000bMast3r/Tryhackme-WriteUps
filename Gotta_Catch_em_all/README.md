> Gotta Catch'em All | Pokemon Series

**export IP=10.10.48.196**

# Nmap

sudo nmap -A -sC -sV -T4 -Pn -vv -p- -oN nmap/initial $IP

```
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
```

**NOTE:  We find a hine in page source `<pokemon>:<hack_the_pokemon>` => SSH Credntials `<!--(Check console for extra surprise!)-->`**

# Gobuster

sudo gobuster -u http://$IP -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt -x txt,php,zip,bak,csv -t 20 -o gobuster/initial

```
Nil
```

# SSH Session 

We find an interseting file in pokemon's home directory `P0kEmOn.zip`. Unzipping it we get `grass-type.txt`

```
50 6f 4b 65 4d 6f 4e 7b 42 75 6c 62 61 73 61 75 72 7d => Hex to ASCII
```

## Flag 1:

`PoKeMoN{Bulbasaur}`

For finding flag2 we have a hint `website may help`. So looking at /var/www/html. Ane we have `water-type.txt`

```
Ecgudfxq_EcGmP{Ecgudfxq} => Caesar cipher
```

## Flag 2

`Squirtle_SqUaD{Squirtle}`

Next is fire-type. Searching using locate command gives us `locate fire-type` => `/etc/why_am_i_here?/fire-type.txt`

```
UDBrM20wbntDaGFybWFuZGVyfQ== => Base64
```

## Flag 3

`P0k3m0n{Charmander}`

In pokemon's video directory we have `/Videos/Gotta/Catch/Them/ALL!` and it contains a C++ file
`Could_this_be_what_Im_looking_for?.cplusplus`

```
# include <iostream>

int main() {
	std::cout << "ash : pikapika" => Has root credentials
	return 0;
}
```

Now SSH as Ash and we have the file `roots-pokemon.txt` in home directory. 

## Flag 4

`Pikachu!`