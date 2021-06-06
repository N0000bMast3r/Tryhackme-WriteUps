> Upload Vulnerabilities

# Overwriting Files

When we inspect the page-source of `http://overwrite.uploadvulns.thm` we can find mountains.jpg. So let's upload an image with the same name and we did overwrite the file with our own.✨

# Flag

```
THM{OTBiODQ3YmNjYWZhM2UyMmYzZDNiZjI5}
```

# RCE => shell.uploadvulns.thm

Let's start with enumeration!

## gobuster

gobuster dir -u http://shell.uploadvulns.thm -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/initial

```
/resources            (Status: 301) [Size: 334] [--> http://shell.uploadvulns.thm/resources/]
/assets               (Status: 301) [Size: 331] [--> http://shell.uploadvulns.thm/assets/]
```

We can upload our shell.php file and get our reverse shell!!

# Flag

```
THM{YWFhY2U3ZGI4N2QxNmQzZjk0YjgzZDZk}
```

# Bypassing Client-Side Filter => java.uploadvulns.thm

While inspecting the page source we can find `client-side-filter.js`. And the MIME type is restricted to `image/png`.
Let's copy `shell.php` to `shell.png` and upload it then capture the request in Burp. We have to change the MIME type to `text/x-php` and filename to `shell.php`.

As usual we have to start with gobuster!

## Gobuster

gobuster dir -u http://java.uploadvulns.thm -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/java

```
/images               (Status: 301) [Size: 329] [--> http://java.uploadvulns.thm/images/]
/assets               (Status: 301) [Size: 329] [--> http://java.uploadvulns.thm/assets/]
```

And accessing `java.uploadvulns.thm/images/shell.php` gives us the shell!!🔥

# Flag.txt

```
THM{NDllZDQxNjJjOTE0YWNhZGY3YjljNmE2}
```

# Bypassing Server-Side Filtering - File Extension

Looks like our extensions are restricted. After trying many extensions looks like `.php5` works. But where is the file present now? Let's run gobuster....again!👽

## Gobuster

gobuster dir -u http://annex.uploadvulns.thm -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/annex

```
/privacy              (Status: 301) [Size: 332] [--> http://annex.uploadvulns.thm/privacy/]
/assets               (Status: 301) [Size: 331] [--> http://annex.uploadvulns.thm/assets/]
```

Now we can access them in `http://annex.uploadvulns.thm/privacy/2021-04-28-08-45-21-shell.php5`. And we have a shell!!🎉

# Flag.txt

```
THM{MGEyYzJiYmI3ODIyM2FlNTNkNjZjYjFl}
```

# Bypassing Server-Side Filtering - Magic Numbers

So here uploading a sample file saya only GIF files are accepted. So let's add six characters to the top of `shell.php`. Now opening it in hexedit we can add the hexa values for GIF in the places of random 6 characters. `47 49 46 38 37 61`.

## Gobuster

gobuster dir -u http://magic.uploadvulns.thm -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/magic

```
/graphics             (Status: 301) [Size: 333] [--> http://magic.uploadvulns.thm/graphics/]
/assets               (Status: 301) [Size: 331] [--> http://magic.uploadvulns.thm/assets/]
```

But accessing these directories we are prompted with 403 error. But we can access the complete path of our shell.php assuming it retrieves the name of the file while uploading.

Accessing `http://magic.uploadvulns.thm/graphics/shell.php` we can get a shell!

# Flag.txt

```
THM{MWY5ZGU4NzE0ZDlhNjE1NGM4ZThjZDJh}
```

# Challenege => http://jewel.uploadvulns.thm/

Looks like we can add image files but there are size limitatios too. But that's not it we can't add any other file types. Looks like flie extensions are restricted and magic numbers are checked too!!

# Enumeration

gobuster dir -u http://jewel.uploadvulns.thm -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 20 -o gobuster/jewel

```
/content              (Status: 301) [Size: 181] [--> /content/]
/modules              (Status: 301) [Size: 181] [--> /modules/]
/admin                (Status: 200) [Size: 1238]               
/assets               (Status: 301) [Size: 179] [--> /assets/] 
/Content              (Status: 301) [Size: 181] [--> /Content/]
/Assets               (Status: 301) [Size: 179] [--> /Assets/] 
/Modules              (Status: 301) [Size: 181] [--> /Modules/]
/Admin                (Status: 200) [Size: 1238] 
```

Inspecting `style.css` gives us the images location and naming schema `/content/ABH.jpg` and similar. Remember we are given a text file.

So, I uploaded a valid JPG file (small) and now we can fuzz to find our files location using gobuster.

# Gobuster

gobuster dir -u http://jewel.uploadvulns.thm -w wordlists.txt -x jpg -t 20 -o gobuster/jewel_myimage

```
/ABH.jpg              (Status: 200) [Size: 705442]
/LKQ.jpg              (Status: 200) [Size: 444808]
/SAD.jpg              (Status: 200) [Size: 247159]
/UAD.jpg              (Status: 200) [Size: 342033]
/WKY.jpg              (Status: 200) [Size: 159451]
/XQH.jpg              (Status: 200) [Size: 159451]
```

We can find a new file here! But we have to bypass the magic byte filter. So we can intercept js file by configuring our Burp. And we can comment out the magic byte filter extension. Now we have to run gobuster again to find our file and runnning it in `/admin` page gives us our shell!

# root.txt

```
THM{NzRlYTUwNTIzODMwMWZhMzBiY2JlZWU2}
```