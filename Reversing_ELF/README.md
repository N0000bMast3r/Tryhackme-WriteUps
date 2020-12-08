> Reversing Elf | radare2

# Crackme1

Executing the file gives us the flag

```
flag{not_that_kind_of_elf}
```

# Crackme2

Running strings gives us a password `super_secret_password`

And running the binary with the password ./Crackme2 super_secret_password gives us the flag

```
flag{if_i_submit_this_flag_then_i_will_get_points}
```

# Crackme3

Running strings we get a base64 encoded string and on decoding it we get the flag.

ZjByX3kwdXJfNWVjMG5kX2xlNTVvbl91bmJhc2U2NF80bGxfN2gzXzdoMW5nNQ==

```
f0r_y0ur_5ec0nd_le55on_unbase64_4ll_7h3_7h1ng5
```

# Crackme4

Analysing using radare2.

## Steps

```
r2 -d Crackme4
aaa => Testing the fnction with random strings
afl
pdf @main => to view the main function
# We find an interesting function there 
pdf @sym.compare_pwd
# In that function our password is tored in the register 'rdi' and compared with our input which is stored at the register 'rax' 
oop 'random' => Passing random arguments
db 0x004006d2 => Setting breakpoint before the comparing point.
dc => Run the program until breakpoint
px @rdi => view the contents of the register 'rdi'
```
my_m0r3_secur3_pwd

# Crackme5

Debug the binary with r2 and viewing the main function has different characters and assembling them gives us the input.

```
OfdlDSA|3tXb32~X3tX@sX`4tXtz
```

Steps in r2

```
r2 -d Crackme5
aaa
pdf @main
db 0x0040082c => Setting the brakpoint before strcmp
dc
Enter your input:
aaa
OfdlDSA|3tXb32~X3tX@sX`4tXtz
```

# Crackme6

Steps in r2

```
r2 -d Crackme6
aaa
afl
pdf @main
pdf @sym.compare_pwd 
# We find another function
pdf @sym.my_secure_test
# And the compare here is in another function
# It seems that it compares our string with hex value 1 by 1
# Taking the cmp values and making them as a string
# 313333375f707764
``` 

## Decoding the string

bytes.fromhex('313333375f707764').decode('utf8')

```
1337_pwd
```

# Crackme7

When we view the main function we find a string `"Wow such h4x0r!"`
And it compared to 0x7a69

And on decoding to ASCII didn't work!
But then decoding the ASCII as a decimal works

bytes.fromhex('7a69').decode('utf8') => zi #didn't work

string = '7a69'
dec = int(string, 16)
print(dec)

```
flag{much_reversing_very_ida_wow}
```

# Crackme8

Looking at the main function we have a hex value `0xcafef00d`
And on decoding it to decimal we get a decimal value but passing it in the binary gives us a message `access denied`.

But since the value is actuall negative, we supply `-88926206` to the binary

```
flag{at_least_this_cafe_wont_leak_your_credit_card_numbers}
```