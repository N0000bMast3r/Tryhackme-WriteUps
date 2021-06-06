> Active Directory Basics

# Active Directory Domain Services (AD DS)

The Active Directory Data Store holds the databases and processes needed to store and manage directory information such as users, groups, and services. Below is an outline of some of the contents and characteristics of the AD DS Data Store:

1. Contains the NTDS.dit - a database that contains all of the information of an Active Directory domain controller as well as password hashes for domain users
2. Stored by default in %SystemRoot%\NTDS
3. accessible only by the domain controller

# Forest

A forest is a collection of one or more domain trees inside of an Active Directory network. It is what categorizes the parts of the network as a whole.

The Forest consists of these parts which we will go into farther detail with later:

1. Trees - A hierarchy of domains in Active Directory Domain Services
2. Domains - Used to group and manage objects 
3. Organizational Units (OUs) - Containers for groups, computers, users, printers and other OUs
4. Trusts - Allows users to access resources in other domains
5. Objects - users, groups, printers, computers, shares
6. Domain Services - DNS Server, LLMNR, IPv6
7. Domain Schema - Rules for object creation

# Types of users in AD

1. Domain Admins - This is the big boss: they control the domains and are the only ones with access to the domain controller.
2. Service Accounts (Can be Domain Admins) - These are for the most part never used except for service maintenance, they are required by Windows for services such as SQL to pair a service with a service account
3. Local Administrators - These users can make changes to local machines as an administrator and may even be able to control other normal users, but they cannot access the domain controller
4. Domain Users - These are your everyday users. They can log in on the machines they have the authorization to access and may have local administrator rights to machines depending on the organization.

# Types of groups in AD

1. Security Groups - These groups are used to specify permissions for a large number of users
2. Distribution Groups - These groups are used to specify email distribution lists. As an attacker these groups are less beneficial to us but can still be beneficial in enumeration

# Default Security Groups - 

﻿There are a lot of default security groups so I won't be going into too much detail of each past a brief description of the permissions that they offer to the assigned group. Here is a brief outline of the security groups:

1. Domain Controllers - All domain controllers in the domain
2. Domain Guests - All domain guests
3. Domain Users - All domain users
4. Domain Computers - All workstations and servers joined to the domain
5. Domain Admins - Designated administrators of the domain
6. Enterprise Admins - Designated administrators of the enterprise
7. Schema Admins - Designated administrators of the schema
8. DNS Admins - DNS Administrators Group
9. DNS Update Proxy - DNS clients who are permitted to perform dynamic updates on behalf of some other clients (such as DHCP servers).
10. Allowed RODC Password Replication Group - Members in this group can have their passwords replicated to all read-only domain controllers in the domain
11. Group Policy Creator Owners - Members in this group can modify group policy for the domain
12. Denied RODC Password Replication Group - Members in this group cannot have their passwords replicated to any read-only domain controllers in the domain
13. Protected Users - Members of this group are afforded additional protections against authentication security threats.
14. Cert Publishers - Members of this group are permitted to publish certificates to the directory
15. Read-Only Domain Controllers - Members of this group are Read-Only Domain Controllers in the domain
16. Enterprise Read-Only Domain Controllers - Members of this group are Read-Only Domain Controllers in the enterprise
17. Key Admins - Members of this group can perform administrative actions on key objects within the domain.
18. Enterprise Key Admins - Members of this group can perform administrative actions on key objects within the forest.
19. Cloneable Domain Controllers - Members of this group that are domain controllers may be cloned.
20. RAS and IAS Servers - Servers in this group can access remote access properties of users

# Trusts and Policies

Trusts and policies go hand in hand to help the domain and trees communicate with each other and maintain "security" inside of the network. They put the rules in place of how the domains inside of a forest can interact with each other, how an external forest can interact with the forest, and the overall domain rules or policies that a domain must follow.

# Types of Trust

1. Directional - The direction of the trust flows from a trusting domain to a trusted domain
2. Transitive - The trust relationship expands beyond just two domains to include other trusted domains

# Default domain services 

1. LDAP - Lightweight Directory Access Protocol; provides communication between applications and directory services
2. Certificate Services - allows the domain controller to create, validate, and revoke public key certificates
3. DNS, LLMNR, NBT-NS - Domain Name Services for identifying IP hostnames

# Domain Authentication

1. Kerberos - The default authentication service for Active Directory uses ticket-granting tickets and service tickets to authenticate users and give users access to other resources across the domain.
2. NTLM - default Windows authentication protocol uses an encrypted challenge/response protocol

# Azure AD

|==================================================|
|Windows Server AD	   |		Azure AD  		   |
|==================================================|
|LDAP				   |		Rest APIs          |
|NTLM				   |	OAuth/SAML  		   |
|Kerberos			   |	OpenID                 |
|OU Tree			   |		Flat Structure     |
|Domains and Forests   |		Tenants			   |
|Trusts				   |	Guests				   |
|==================================================|

# Credentials

Username: Administrator
Password: password123@
Domain: CONTROLLER.local

I used SSH to enter the box!

## Steps

1. cd Downloads
2. powershell -ep bypass
3. . .\PowerView.ps1

# Powerview Tricks

https://gist.github.com/HarmJ0y/184f9822b195c52dd50c379ed3117993

1. Get a list a OS 

Get-NetComputer -fulldata | select operatingsystem


```
operatingsystem
---------------
Windows Server 2019 Standard     
Windows 10 Enterprise Evaluation
Windows 10 Enterprise Evaluation
```

2. List of all users in domain.

Get-NetUser | select cn


```
cn
--
Administrator
Guest
krbtgt
Machine-1
Admin2
Machine-2
SQL Service
POST{P0W3RV13W_FTW}
sshd
```

3. List groups 

Get-NetGroup -GroupName *

```
Administrators 
Users
Guests
Print Operators 
Backup Operators 
Replicator 
Remote Desktop Users
Network Configuration Operators
Performance Monitor Users 
Performance Log Users
Distributed COM Users 
IIS_IUSRS
Cryptographic Operators 
RDS Remote Access Servers
RDS Endpoint Servers
RDS Management Servers
Hyper-V Administrators
Access Control Assistance Operators
Remote Management Users
Storage Replica Administrators
Domain Computers
Domain Controllers
Schema Admins
Enterprise Admins
Cert Publishers
Domain Admins
Domain Users
Domain Guests
Group Policy Creator Owners
RAS and IAS Servers
Server Operators
Account Operators
Pre-Windows 2000 Compatible Access
Incoming Forest Trust Builders
Windows Authorization Access Group
Terminal Server License Servers
Allowed RODC Password Replication Group
Denied RODC Password Replication Group
Read-only Domain Controllers
Enterprise Read-only Domain Controllers
Cloneable Domain Controllers
Protected Users
Key Admins
Enterprise Key Admins
DnsAdmins
DnsUpdateProxy
```

4. When was the password last set for the SQLService user?

`Get-NetUser -SPN | ?{$_.memberof -match 'Domain Admins'}`

```
logoncount            : 0
badpasswordtime       : 12/31/1600 4:00:00 PM
description           : My password is MYpassword123#
distinguishedname     : CN=SQL Service,CN=Users,DC=CONTROLLER,DC=local
objectclass           : {top, person, organizationalPerson, user}
displayname           : SQL Service
userprincipalname     : SQLService@CONTROLLER.local
name                  : SQL Service
objectsid             : S-1-5-21-849420856-2351964222-986696166-1107 
samaccountname        : SQLService
lastlogon             : 12/31/1600 4:00:00 PM
codepage              : 0
samaccounttype        : 805306368
whenchanged           : 5/14/2020 3:42:53 AM
accountexpires        : 9223372036854775807
countrycode           : 0
adspath               : LDAP://CN=SQL Service,CN=Users,DC=CONTROLLER,DC=local
instancetype          : 4
objectguid            : 1c3f20d7-c383-466a-9a67-92a774650cb8
sn                    : Service
lastlogoff            : 12/31/1600 4:00:00 PM
objectcategory        : CN=Person,CN=Schema,CN=Configuration,DC=CONTROLLER,DC=local
dscorepropagationdata : {5/14/2020 3:29:56 AM, 1/1/1601 12:00:00 AM}
serviceprincipalname  : DOMAIN-CONTROLLER/SQLService.CONTROLLER.local:60111
givenname             : SQL
admincount            : 1
memberof              : {CN=Group Policy Creator Owners,OU=Groups,DC=CONTROLLER,DC=local, CN=Domain Admins,OU=Groups,DC=CONTROLLER,DC=local,      
                        CN=Enterprise Admins,OU=Groups,DC=CONTROLLER,DC=local, CN=Schema Admins,OU=Groups,DC=CONTROLLER,DC=local...}
whencreated           : 5/14/2020 3:26:57 AM
badpwdcount           : 0
cn                    : SQL Service
useraccountcontrol    : 66048
usncreated            : 12820
primarygroupid        : 513
pwdlastset            : 5/13/2020 8:26:58 PM
usnchanged            : 12890
```