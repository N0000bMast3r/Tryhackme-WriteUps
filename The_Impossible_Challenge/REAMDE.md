> The Impossible Challenge

-

qo qt q` r6 ro su pn s_ rn r6 p6 s_ q2 ps qq rs rp ps rt r4 pu pt qn r4 rq pt q` so pu ps r4 sq pu ps q2 su rn on oq o_ pu ps ou r5 pu pt r4 sr rp qt pu rs q2 qt r4 r4 ro su pq o5

Decoding from rot13 -> rot47 -> hex -> base64 `It's inside the text, in front of your eyes!`

On inspecting the challenge page we have an intersting point `Hmm` and it's attributes are `"‌‌‌‌‍\ufeff‌‌Hmm‌‌‌‌‍‌‍‌‌‌‌‍\ufeff‌\ufeff‌‌‌‌‍\ufeff‌\ufeff‌‌‌‌‍\ufeff‍\ufeff‌‌‌‌‍\ufeff\ufeff‌‌‌‌‍\ufeff‌‌‌‌‌‍‍‌‌‌‌‌‌‌‌‌‌‌‌‍‍‌‌‌‌‍\ufeff‌\ufeff‌‌‌‌‌‌‌‌‌‌‌‍‌‌‌‌‌‍‌‍‌‌‌‌‍‌‌‌‌‌‍‌‍‌‌‌‌‍‍‍‌‌‌‌‍\ufeff‌‌‌‌‍\ufeff‌‌‌‌‌‌‍\ufeff"`. Looks like Unicode Zero-Width Characters. And we have Unicode Steganography with Zero Width characters.

Copy pasting the Hmm in `https://330k.github.io/misc_tools/unicode_steganography.html` we have `password is hahaezpz`.

And entering the password for the zip we find the flag.

# flag.txt

```
THM{Zero_Width_Characters_EZPZ}
```