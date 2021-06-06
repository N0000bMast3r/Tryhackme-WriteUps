Port 8000 || beta.
Port 80 || dev

What I got?

Monitorr - montiors both sites

We can change the settings for monitor here.

```
Data directory present:
/var/www/monitorr/data
Database file present:
/var/www/monitorr/datausers.db
```

robyns-petshop.thm 
monitorr.robyns-petshop.thm 
beta.robyns-petshop.thm 
dev.robyns-petshop.thm

```
==> DIRECTORY: https://dev.robyns-petshop.thm/assets/
+ https://dev.robyns-petshop.thm/business (CODE:401|SIZE:470)       
==> DIRECTORY: https://dev.robyns-petshop.thm/config/
==> DIRECTORY: https://dev.robyns-petshop.thm/content/
+ https://dev.robyns-petshop.thm/index.php (CODE:200|SIZE:3703)        
+ https://dev.robyns-petshop.thm/LICENSE (CODE:200|SIZE:1085)          
==> DIRECTORY: https://dev.robyns-petshop.thm/plugins/
+ https://dev.robyns-petshop.thm/server-status (CODE:403|SIZE:288)     
==> DIRECTORY: https://dev.robyns-petshop.thm/themes/
==> DIRECTORY: https://dev.robyns-petshop.thm/vendor/
---- Entering directory: https://dev.robyns-petshop.thm/assets/ ----
---- Entering directory: https://dev.robyns-petshop.thm/config/ ----  
---- Entering directory: https://dev.robyns-petshop.thm/content/ ----  
---- Entering directory: https://dev.robyns-petshop.thm/plugins/ ----   
---- Entering directory: https://dev.robyns-petshop.thm/themes/ ----   
---- Entering directory: https://dev.robyns-petshop.thm/vendor/ ----
```

---
+ SSL Info:        Subject:  /C=GB/ST=South West/L=Bristol/O=Robyns Petshop/CN=robyns-petshop.thm/emailAddress=robyn@robyns-petshop.thm
                   Ciphers:  TLS_AES_256_GCM_SHA384
                   Issuer:   /C=GB/ST=South West/L=Bristol/O=Robyns Petshop/CN=robyns-petshop.thm/emailAddress=robyn@robyns-petshop.thm
+ Start Time:         2021-04-25 07:27:32 (GMT-4)
---------------------------------------------------------------------------
+ Server: Apache/2.4.29 (Ubuntu)
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The site uses SSL and the Strict-Transport-Security HTTP header is not defined.
+ The site uses SSL and Expect-CT header is not present.
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ Cookie isHuman created without the secure flag
+ Cookie isHuman created without the httponly flag
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ The Content-Encoding header is set to "deflate" this may mean that the server is vulnerable to the BREACH attack.
+ Hostname 'monitorr.robyns-petshop.thm' does not match certificate's names: robyns-petshop.thm
+ Apache/2.4.29 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ Web Server returns a valid response with junk HTTP methods, this may cause false positives.
+ DEBUG HTTP verb may show server debugging information. See http://msdn.microsoft.com/en-us/library/e8z01xdh%28VS.80%29.aspx for details.


## Jellyfin

/etc/jellyfin/users/ => Contains lists of users
An API call to /Users/Public provides a list of available users.

## FTP => Is vulnerable but has no exploit .

## Valid Emails (Maybee)

robyn@robyns-petshop.thm
staff@robyns-petshop.thm

Do checkout /business