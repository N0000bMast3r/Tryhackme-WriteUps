> Cicada-3301 | Steganography, Crypto

We have an audio `3301.wav` and adding a spectogram layer we have a QRcode and on scanning it we have a link `https://pastebin.com/wphPq0Aa`

```
Passphrase: SG01Ul80X1A0NTVtaHA0NTMh
Key: Q2ljYWRh
```

# Decrypted Passphrase and key

```
Hm5R_4_P455mhp453!
Cicada
```

And encoding `Hm5R_4_P455mhp453!` with the key `cicada` gives us `Ju5T_4_P455phr453!`.

# Gathering Metadata

steghide extract -sf welcome.jpg => `https://imgur.com/a/c0ZSZga`

ANd we have another image and we can't find anything using steghide. Let's use another tool outguess. 

./outguess -r /home/n00bmas3r/Harsha/THM/Cicada-3301/Original_cicade.jpg /home/n00bmas3r/Harsha/THM/Cicada-3301/output. We have a hash.

```
b6a233fb9b2d8772b636ab581169b58c98bd4b8df25e452911ef75561df649edc8852846e81837136840f3aa453e83d86323082d5b6002a16bc20c1560828348
```

We identify the hash as `SHA512` and decoding it we have `https://pastebin.com/6FNiVLh5`.


```
Use positive integers to go forward in the text use negative integers to go backwards in the text.

I:1:6
I:2:15
I:3:26
I:5:4 
I:6:15
I:10:26
/
/
I:13:5
I:13:1
I:14:7
I:3:29
I:19:8 
I:22:25
/
I:23:-1
I:19:-1
I:2:21
I:5:9
I:24:-2
I:22:1 
I:38:1

```

We have a link `https://bit.ly/39pw2NH`

What is the song linked?

```
The Instar Emergence
```