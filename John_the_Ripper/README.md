> John The Ripper

# Hash 1 : 2e728dd31fb5949bc39cac5a9f066498

hash-id.py : MD5

# John

john --list=formats | grep -iF md5

john --format=Raw-MD5 --wordlist=/usr/share/wordlists/rockyou.txt hash1.txt

```
biscuit
```

# Hash 2 : 1A732667F3917C0F4AA98BB13011B9090C6F8065

hash-id.py : SHA-1

# John

john --format=Raw-SHA1 --wordlist=/usr/share/wordlists/rockyou.txt hash2.txt

```
kangeroo
```

# Hash 3 : D7F4D3CCEE7ACD3DD7FAD3AC2BE2AAE9C44F4E9B7FB802D73136D4C53920140A

hash-id.py : SHA-256

# John

john --format=Raw-SHA256 --wordlist=/usr/share/wordlists/rockyou.txt hash3.txt

```
microphone
```

# Hash 4 : c5a60cc6bbba781c601c5402755ae1044bbf45b78d1183cbf2ca1c865b6c792cf3c6b87791344986c8a832a0f9ca8d0b4afd3d9421a149d57075e1b4e93f90bf

hash-id.py : whirlpool

# John

john --format=whirlpool --wordlist=/usr/share/wordlists/rockyou.txt hash4.txt

```
colossal
```

# NTLM Hash Cracking : 5460C85BD858A11475115D2DD3A82333

john --list=formats | grep -iF NT

john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt ntlm.txt

```
mushroom 
```

# Cracking hashes from /etc/shadow

```
root:x:0:0::/root:/bin/bash
root:$6$Ha.d5nGupBm29pYr$yugXSk24ZljLTAZZagtGwpSQhb3F2DOJtnHrvk7HI2ma4GsuioHp8sm3LJiRJpKfIf7lZQ29qgtH17Q/JDpYM/:18576::::::
```

unshadow local_passwd local_shadow > unshadowed.txt

```
root:$6$Ha.d5nGupBm29pYr$yugXSk24ZljLTAZZagtGwpSQhb3F2DOJtnHrvk7HI2ma4GsuioHp8sm3LJiRJpKfIf7lZQ29qgtH17Q/JDpYM/:0:0::/root:/bin/bash
```

john --format=sha512crypt --wordlist=/usr/share/wordlists/rockyou.txt unshadowed.txt

```
1234             (root)
```

# Single Crack Mode : 7bf6d9bb82bed1302f331fc6b816aada

Task: Download the attached hash and crack it, assuming that the user it belongs to is called "Joker".

Let's prepend the username in the beginning.

## hash.txt

```
joker:7bf6d9bb82bed1302f331fc6b816aada 
```

**Note: Here : is geco field**

john --single --format=Raw-MD5 hash.txt 

```
Jok3r
```

# Custom Rules

## The first line:

[List.Rules:THMRules] - Is used to define the name of your rule, this is what you will use to call your custom rule as a John argument.

We then use a regex style pattern match to define where in the word will be modified, again- we will only cover the basic and most common modifiers here:

Az - Takes the word and appends it with the characters you define

A0 - Takes the word and prepends it with the characters you define

c - Capitalises the character positionally


These can be used in combination to define where and what in the word you want to modify.

Lastly, we then need to define what characters should be appended, prepended or otherwise included, we do this by adding character sets in square brackets [ ] in the order they should be used. These directly follow the modifier patterns inside of double quotes " ". Here are some common examples:


[0-9] - Will include numbers 0-9

[0] - Will include only the number 0

[A-z] - Will include both upper and lowercase

[A-Z] - Will include only uppercase letters

[a-z] - Will include only lowercase letters

[a] - Will include only a

[!£$%@] - Will include the symbols !£$%@


Putting this all together, in order to generate a wordlist from the rules that would match the example password "Polopassword1!" (assuming the word polopassword was in our wordlist) we would create a rule entry that looks like this:

```
[List.Rules:PoloPassword]

cAz"[0-9] [!£$%@]"
```

In order to:

Capitalise the first  letter - c

Append to the end of the word - Az

A number in the range 0-9 - [0-9]

Followed by a symbol that is one of [!£$%@]


## Using Custom Rules

We could then call this custom rule as a John argument using the  --rule=PoloPassword flag.

As a full command: `john --wordlist=[path to wordlist] --rule=PoloPassword [path to file]`


As a note I find it helpful to talk out the patterns if you're writing a rule- as shown above, the same applies to writing RegEx patterns too.

# Cracking a Password Protected Zip File 

zip2john task.zip > zip_hash.txt

```
task.zip/zippy/flag.txt:$pkzip2$1*2*2*0*26*1a*849ab5a6*0*48*0*26*849a*b689*964fa5a31f8cefe8e6b3456b578d66a08489def78128450ccf07c28dfa6c197fd148f696e3a2*$/pkzip2$:zippy/flag.txt:task.zip::task.zip
```

john zip_hash.txt --wordlist=/usr/share/wordlists/rockyou.txt

```
pass123
```

# Flag.txt

```
THM{w3ll_d0n3_h4sh_r0y4l}
```

# Cracking a Password Protected RAR Archive

rar2john task.rar > rar_hash.txt

```
task.rar:$rar5$16$b7b0ffc959b2bc55ffb712fc0293159b$15$4f7de6eb8d17078f4b3c0ce650de32ff$8$ebd10bb79dbfb9f8
```

john rar_hash.txt --wordlist=/usr/share/wordlists/rockyou.txt

```
password
```

unrar e task.rar

# flag.txt 

```
THM{r4r_4rch1ve5_th15_t1m3}
```

# Cracking SSH Key Passwords

python /usr/share/john/ssh2john.py id_rsa > ssh_hash.txt

```
id_rsa:$sshng$1$16$3A98F468854BB3836BF689310D864CE9$1200$08ca19b68bc606b07875701174131b9220d23ef968befc1230eeff0d7c0f904e6734765fe562e8671972e409091f32c80b754ab248976228a5f2c38e8ac63572d7452e75669aeda932275989ce4c077d43287ed227b8f9053e53f2b1c9bb9dfe876378a32e87e7be4e91a845ae8ee4073bf7ac5aad8414253c97cfb73b083107712907da8c704678f46d0b006f7a77b13a04305a988c8e17d83abd2449ed5c3defc8203d7c5f70cef3470b0bbe3fa5a2e957ac55a57ea08b1de4d3fa5436c6160a14b461ac7bc4a3052ddf858de657ecb210989507beb96f7219ac3c3790e89f3af71f7f61ebe23570284a482b1504b067fb1e03ed62201c6db71dab65e5f1577751ddb006fe14ceed4525965fce19f8141373094d1aedbb58cb903f58f6d80695be0382c31e61baaf366d4f2e722316e91ff4dcb3df15702008b5be3c0b2a81b3f452ef3257c425dd26119324b4de3652e90b91afd87ca2bc41c70abd0d97557d4037952b63c0a0d7c7ab6ed538c3d76bdf488683213e8d8e897ab51c4990b137d04e5044ccbf8cadbdce9eeec5e50f3d487b1f21e86a2b2785caedbf9503d2d8585b2138d82b35e70d1da03c9c574962cdb6e4d2de761a594ab8c082d88b43a027649012feb28b6a022c0ab49cf05e8b91e36bda935f188c1bb05925da2168dd15af917ba20a8532010892853da5cb1a8ff80cc5d3aa1dd3fe66543bf14d9b44d082261fd61976718bb5eea1d911ddb7fb0cc0505b39cec36ef7bd8e8d9d826eda5f7e1a5a51067ead2f78cf69f85de97be5a8f371174356788554b6bf134072b93bf6728ec26fe19c2485be9e7428208a66cc1e79329ac16f3034605c63550a424ed8cac39f965b6ffe83240c6709607eaef99b189100ef33e000b4195e07ec5c67bdaf2ca1acbd08327f0c4dcfae322883f7be964cb22393541e883c8c5b748237a900aab709b6286cea66a214a9fe4e3a1203f999fd995aa049767355e2658828c4a82d58ca15343f0abe6b2779e880ed2682b4730103a84a3410e6c822098d82b04d665b8bf98bc3b69cae0c8d8c9d140dc99056279d5f330bc439bfdceaf38a56fd1362ce78e96deb49a9f6756ec9b64eeba8f4725ec056ab206e37823d052d539d38016abf792858a169cbbe0f6f0d0049c6d49228833aa8ec10ede0c183ac737e54346949485e5ffc1bc3105e5686c8b1f6fb8cdb14949aa97b833757d02b970e96cb1281c472a5cb26cfa7cfda0be5bd45cf14d4bc28ccd2be4dd09c6a2ce0cf668035d2aa39a8345ea154543491436bf8f5e605d86e266d40227f48684e696a225877624ddddf0afe05d0aeec29ad28edb0f8cda0f341ddbbd454bd3c238d1c499effa6bf6f796dae0983182f36fae4781552cb8d9426fc57132c27a735c5365a5d355a4c4f21d5d7ed2ea11bb2ed856156390673545418f47359fd1092767f6dfb3321ee14a0043352fdbaa5cb0e75fde2ec5909c0533251f30bd56ad7e34a8a31b009b53c64e9f2de9fd57a0f561564e6a961158cc0b54fcfc43046d9641788ac5e25b89bdb7890c4e6532d1bfabd4d49ae7d3740506c4ecb6bc5cb6a12bc24ed2e0f913338c7dfa08ada66a6128e7de56794d1d2170d6324af0cd72bc8abcff177f0942d9df5d99d48c8f946fd856d9ccb424966835aa06c94996abcc169aef6f246bbbd7489ec026a
```

john ssh_hash.txt --wordlist=/usr/share/wordlists/rockyou.txt

```
mango            (id_rsa)
```