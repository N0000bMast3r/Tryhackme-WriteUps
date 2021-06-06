> Hacking with powershell

# Credentials

Username: Administrator
Password: BHN2UVw0Q

xfreerdp /u:'Administrator' /p:'BHN2UVw0Q' /v:10.10.129.173 /f

1. What is the location of the file "interesting-file.txt"?

`Get-ChildItem -Path C:/ -Name interesting-file.txt -Recurse -File`
Didn't work. So `Get-ChildItem -Path C:/ -Include interesting-file.txt -Recurse -File`
`Get-ChildItem -Path C:/ -Include *interesting-file.txt* -Recurse -File -ErrorAction SilentlyContinue`

```
    Directory: C:\Program Files


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        10/3/2019  11:38 PM             23 interesting-file.txt.txt
```

2. Specify the contents of this file


# interesting-file.txt.txt

```
notsointerestingcontent
```

3. How many cmdlets are installed on the system(only cmdlets, not functions and aliases)?

We can use the `measure` command to get the count.

`Get-Command | measure`

```
Count    : 7935
Average  :
Sum      :
Maximum  :
Minimum  :
Property :
```

But only cmdlets and not fucntions/alias.
Let's get the forst parameter. `Get-Command Select-Object -First 1`

```
CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Cmdlet          Select-Object                                      3.1.0.0    Microsoft.PowerShell.Utility
```

`Get-Command | Where-Object -Property CommandType -eq Cmdlet | measure`

```
Count    : 6638
Average  :
Sum      :
Maximum  :
Minimum  :
Property :
```

4. Get the MD5 hash of interesting-file.txt

# PS C:\Program Files> Get-Command *hash*

```
CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Function        Get-BCHashCache                                    1.0.0.0    BranchCache
Function        Get-FileHash                                       3.1.0.0    Microsoft.PowerShell.Utility
Cmdlet          Get-DfsrFileHash                                   2.0.0.0    DFSR
```

# PS C:\Program Files> (Get-Command Get-FileHash).Parameters

```
Key                 Value
---                 -----
Path                System.Management.Automation.ParameterMetadata
LiteralPath         System.Management.Automation.ParameterMetadata
InputStream         System.Management.Automation.ParameterMetadata
Algorithm           System.Management.Automation.ParameterMetadata
Verbose             System.Management.Automation.ParameterMetadata
Debug               System.Management.Automation.ParameterMetadata
ErrorAction         System.Management.Automation.ParameterMetadata
WarningAction       System.Management.Automation.ParameterMetadata
InformationAction   System.Management.Automation.ParameterMetadata
ErrorVariable       System.Management.Automation.ParameterMetadata
WarningVariable     System.Management.Automation.ParameterMetadata
InformationVariable System.Management.Automation.ParameterMetadata
OutVariable         System.Management.Automation.ParameterMetadata
OutBuffer           System.Management.Automation.ParameterMetadata
PipelineVariable    System.Management.Automation.ParameterMetadata
```

# PS C:\Program Files> Get-FileHash -Path "C:\Program Files\interesting-file.txt.txt" -Algorithm MD5

```
Algorithm       Hash                                                                   Path
---------       ----                                                                   ----
MD5             49A586A2A9456226F8A1B4CEC6FAB329                                       C:\Program Files\interesting-...
```

5. What is the command to get the current working directory?

```
Get-Location
```

6. Does the path “C:\Users\Administrator\Documents\Passwords” Exist(Y/N)?

```
Get-Location -Path "C:\Users\Administrator\Documents\Passwords"
```

7. What command would you use to make a request to a web server?

```
Invoke-WebRequest
```

8. Base64 decode the file b64.txt on Windows.

We can see that it is in Desktop.

`certutil -decode "C:\Users\Administrator\Desktop\b64.txt" out.txt`

cat out.txt

```
ihopeyoudidthisonwindows
```

# Enumeration

1. How many users are there on the machine?

Get-LocalUser

```

Name           Enabled Description
----           ------- -----------
Administrator  True    Built-in account for administering the computer/domain
DefaultAccount False   A user account managed by the system.
duck           True
duck2          True
Guest          False   Built-in account for guest access to the computer/domain
```

2. Which local user does this SID(S-1–5–21–1394777289–3961777894–1791813945–501) belong to?

# PS C:\Users\Administrator> (Get-Command Get-LocalUser).Parameters

```
Key                 Value
---                 -----
Name                System.Management.Automation.ParameterMetadata
SID                 System.Management.Automation.ParameterMetadata
Verbose             System.Management.Automation.ParameterMetadata
Debug               System.Management.Automation.ParameterMetadata
ErrorAction         System.Management.Automation.ParameterMetadata
WarningAction       System.Management.Automation.ParameterMetadata
InformationAction   System.Management.Automation.ParameterMetadata
ErrorVariable       System.Management.Automation.ParameterMetadata
WarningVariable     System.Management.Automation.ParameterMetadata
InformationVariable System.Management.Automation.ParameterMetadata
OutVariable         System.Management.Automation.ParameterMetadata
OutBuffer           System.Management.Automation.ParameterMetadata
PipelineVariable    System.Management.Automation.ParameterMetadata
```

# PS C:\Users\Administrator> Get-LocalUser -SID "S-1-5-21-1394777289-3961777894-1791813945-501"

```
Name  Enabled Description
----  ------- -----------
Guest False   Built-in account for guest access to the computer/domain
```

3. How many users have their password required values set to False?

# PS C:\Users\Administrator> Get-LocalUser | Get-Member

```
TypeName: Microsoft.PowerShell.Commands.LocalUser

Name                   MemberType Definition
----                   ---------- ----------
Clone                  Method     Microsoft.PowerShell.Commands.LocalUser Clone()
Equals                 Method     bool Equals(System.Object obj)
GetHashCode            Method     int GetHashCode()
GetType                Method     type GetType()
ToString               Method     string ToString()
AccountExpires         Property   System.Nullable[datetime] AccountExpires {get;set;}
Description            Property   string Description {get;set;}
Enabled                Property   bool Enabled {get;set;}
FullName               Property   string FullName {get;set;}
LastLogon              Property   System.Nullable[datetime] LastLogon {get;set;}
Name                   Property   string Name {get;set;}
ObjectClass            Property   string ObjectClass {get;set;}
PasswordChangeableDate Property   System.Nullable[datetime] PasswordChangeableDate {get;set;}
PasswordExpires        Property   System.Nullable[datetime] PasswordExpires {get;set;}
PasswordLastSet        Property   System.Nullable[datetime] PasswordLastSet {get;set;}
PasswordRequired       Property   bool PasswordRequired {get;set;}
PrincipalSource        Property   System.Nullable[Microsoft.PowerShell.Commands.PrincipalSource] PrincipalSource {ge...
SID                    Property   System.Security.Principal.SecurityIdentifier SID {get;set;}
UserMayChangePassword  Property   bool UserMayChangePassword {get;set;}
```

# PS C:\Users\Administrator> Get-LocalUser | Where-Object -Property PasswordRequired -Match false

```
Name           Enabled Description
----           ------- -----------
DefaultAccount False   A user account managed by the system.
duck           True
duck2          True
Guest          False   Built-in account for guest access to the computer/domain
```

4. How many local groups exist?

# PS C:\Users\Administrator> Get-LocalGroup | measure

```
Count    : 24
Average  :
Sum      :
Maximum  :
Minimum  :
Property :
```

5. What command did you use to get the IP address info?

# PS C:\Users\Administrator> Get-NetIPAddress

```
IPAddress         : fe80::8a0:2f63:f5f5:36c%7
InterfaceIndex    : 7
InterfaceAlias    : Local Area Connection* 3
AddressFamily     : IPv6
Type              : Unicast
PrefixLength      : 64
PrefixOrigin      : WellKnown
SuffixOrigin      : Link
AddressState      : Preferred
ValidLifetime     : Infinite ([TimeSpan]::MaxValue)
PreferredLifetime : Infinite ([TimeSpan]::MaxValue)
SkipAsSource      : False
PolicyStore       : ActiveStore

IPAddress         : 2001:0:2851:782c:8a0:2f63:f5f5:36c
InterfaceIndex    : 7
InterfaceAlias    : Local Area Connection* 3
AddressFamily     : IPv6
Type              : Unicast
PrefixLength      : 64
PrefixOrigin      : RouterAdvertisement
SuffixOrigin      : Link
AddressState      : Preferred
ValidLifetime     : Infinite ([TimeSpan]::MaxValue)
PreferredLifetime : Infinite ([TimeSpan]::MaxValue)
SkipAsSource      : False
PolicyStore       : ActiveStore

IPAddress         : fe80::75f1:4a2:b3b7:3fc3%5
InterfaceIndex    : 5
InterfaceAlias    : Ethernet
AddressFamily     : IPv6
Type              : Unicast
PrefixLength      : 64
PrefixOrigin      : WellKnown
SuffixOrigin      : Link
AddressState      : Preferred
ValidLifetime     : Infinite ([TimeSpan]::MaxValue)
PreferredLifetime : Infinite ([TimeSpan]::MaxValue)
SkipAsSource      : False
PolicyStore       : ActiveStore

IPAddress         : ::1
InterfaceIndex    : 1
InterfaceAlias    : Loopback Pseudo-Interface 1
AddressFamily     : IPv6
Type              : Unicast
PrefixLength      : 128
PrefixOrigin      : WellKnown
SuffixOrigin      : WellKnown
AddressState      : Preferred
ValidLifetime     : Infinite ([TimeSpan]::MaxValue)
PreferredLifetime : Infinite ([TimeSpan]::MaxValue)
SkipAsSource      : False
PolicyStore       : ActiveStore

IPAddress         : 10.10.252.147
InterfaceIndex    : 5
InterfaceAlias    : Ethernet
AddressFamily     : IPv4
Type              : Unicast
PrefixLength      : 16
PrefixOrigin      : Dhcp
SuffixOrigin      : Dhcp
AddressState      : Preferred
ValidLifetime     : 00:42:56
PreferredLifetime : 00:42:56
SkipAsSource      : False
PolicyStore       : ActiveStore

IPAddress         : 127.0.0.1
InterfaceIndex    : 1
InterfaceAlias    : Loopback Pseudo-Interface 1
AddressFamily     : IPv4
Type              : Unicast
PrefixLength      : 8
PrefixOrigin      : WellKnown
SuffixOrigin      : WellKnown
AddressState      : Preferred
ValidLifetime     : Infinite ([TimeSpan]::MaxValue)
PreferredLifetime : Infinite ([TimeSpan]::MaxValue)
SkipAsSource      : False
PolicyStore       : ActiveStore
```

6. How many ports are listed as listening?

# Get-NetTCPConnection

```
LocalAddress                        LocalPort RemoteAddress                       RemotePort State       AppliedSetting
------------                        --------- -------------                       ---------- -----       --------------
::                                  49677     ::                                  0          Listen
::                                  49674     ::                                  0          Listen
::                                  49667     ::                                  0          Listen
::                                  49666     ::                                  0          Listen
::                                  49665     ::                                  0          Listen
::                                  49664     ::                                  0          Listen
::                                  47001     ::                                  0          Listen
::                                  5985      ::                                  0          Listen
::                                  3389      ::                                  0          Listen
::                                  445       ::                                  0          Listen
::                                  135       ::                                  0          Listen
0.0.0.0                             49756     0.0.0.0                             0          Bound
10.10.252.147                       49756     52.242.101.226                      443        SynSent
0.0.0.0                             49677     0.0.0.0                             0          Listen
0.0.0.0                             49674     0.0.0.0                             0          Listen
0.0.0.0                             49667     0.0.0.0                             0          Listen
0.0.0.0                             49666     0.0.0.0                             0          Listen
0.0.0.0                             49665     0.0.0.0                             0          Listen
0.0.0.0                             49664     0.0.0.0                             0          Listen
10.10.252.147                       3389      10.8.107.21                         47944      Established Internet
0.0.0.0                             3389      0.0.0.0                             0          Listen
10.10.252.147                       139       0.0.0.0                             0          Listen
0.0.0.0                             135       0.0.0.0                             0          Listen
```

# Get-NetTCPConnection | Get-Member

```
Name                      MemberType     Definition
----                      ----------     ----------
Clone                     Method         System.Object ICloneable.Clone()
Dispose                   Method         void Dispose(), void IDisposable.Dispose()
Equals                    Method         bool Equals(System.Object obj)
GetCimSessionComputerName Method         string GetCimSessionComputerName()
GetCimSessionInstanceId   Method         guid GetCimSessionInstanceId()
GetHashCode               Method         int GetHashCode()
GetObjectData             Method         void GetObjectData(System.Runtime.Serialization.SerializationInfo info, Sys...
GetType                   Method         type GetType()
ToString                  Method         string ToString()
AggregationBehavior       Property       uint16 AggregationBehavior {get;set;}
AvailableRequestedStates  Property       uint16[] AvailableRequestedStates {get;set;}
Caption                   Property       string Caption {get;set;}
CommunicationStatus       Property       uint16 CommunicationStatus {get;set;}
CreationTime              Property       CimInstance#DateTime CreationTime {get;}
Description               Property       string Description {get;set;}
DetailedStatus            Property       uint16 DetailedStatus {get;set;}
Directionality            Property       uint16 Directionality {get;set;}
ElementName               Property       string ElementName {get;set;}
EnabledDefault            Property       uint16 EnabledDefault {get;set;}
EnabledState              Property       uint16 EnabledState {get;set;}
HealthState               Property       uint16 HealthState {get;set;}
InstallDate               Property       CimInstance#DateTime InstallDate {get;set;}
InstanceID                Property       string InstanceID {get;set;}
LocalAddress              Property       string LocalAddress {get;}
LocalPort                 Property       uint16 LocalPort {get;}
Name                      Property       string Name {get;set;}
OperatingStatus           Property       uint16 OperatingStatus {get;set;}
OperationalStatus         Property       uint16[] OperationalStatus {get;set;}
OtherEnabledState         Property       string OtherEnabledState {get;set;}
OwningProcess             Property       uint32 OwningProcess {get;}
PrimaryStatus             Property       uint16 PrimaryStatus {get;set;}
PSComputerName            Property       string PSComputerName {get;}
RemoteAddress             Property       string RemoteAddress {get;}
RemotePort                Property       uint16 RemotePort {get;}
RequestedState            Property       uint16 RequestedState {get;set;}
Status                    Property       string Status {get;set;}
StatusDescriptions        Property       string[] StatusDescriptions {get;set;}
TimeOfLastStateChange     Property       CimInstance#DateTime TimeOfLastStateChange {get;set;}
TransitioningToState      Property       uint16 TransitioningToState {get;set;}
AppliedSetting            ScriptProperty System.Object AppliedSetting {get=[Microsoft.PowerShell.Cmdletization.Gener...
OffloadState              ScriptProperty System.Object OffloadState {get=[Microsoft.PowerShell.Cmdletization.Generat...
State                     ScriptProperty System.Object State {get=[Microsoft.PowerShell.Cmdletization.GeneratedTypes...
```

# PS C:\Users\Administrator> Get-NetTCPConnection | Format-List -Property State

```
State : Listen

State : Listen

State : Listen

State : Listen

State : Listen

State : Listen

State : Listen

State : Listen

State : Listen

State : Listen

State : Listen

State : Bound

State : SynSent

State : Listen

State : Listen

State : Listen

State : Listen

State : Listen

State : Listen

State : Established

State : Listen

State : Listen

State : Listen
```

# PS C:\Users\Administrator> Get-NetTCPConnection | Where-Object -Property State -Match Listen

```
LocalAddress                        LocalPort RemoteAddress                       RemotePort State       AppliedSetting
------------                        --------- -------------                       ---------- -----       --------------
::                                  49677     ::                                  0          Listen
::                                  49674     ::                                  0          Listen
::                                  49667     ::                                  0          Listen
::                                  49666     ::                                  0          Listen
::                                  49665     ::                                  0          Listen
::                                  49664     ::                                  0          Listen
::                                  47001     ::                                  0          Listen
::                                  5985      ::                                  0          Listen
::                                  3389      ::                                  0          Listen
::                                  445       ::                                  0          Listen
::                                  135       ::                                  0          Listen
0.0.0.0                             49677     0.0.0.0                             0          Listen
0.0.0.0                             49674     0.0.0.0                             0          Listen
0.0.0.0                             49667     0.0.0.0                             0          Listen
0.0.0.0                             49666     0.0.0.0                             0          Listen
0.0.0.0                             49665     0.0.0.0                             0          Listen
0.0.0.0                             49664     0.0.0.0                             0          Listen
0.0.0.0                             3389      0.0.0.0                             0          Listen
10.10.252.147                       139       0.0.0.0                             0          Listen
0.0.0.0                             135       0.0.0.0                             0          Listen
```

# PS C:\Users\Administrator> Get-NetTCPConnection | Where-Object -Property State -Match Listen | measure

```
Count    : 20
Average  :
Sum      :
Maximum  :
Minimum  :
Property :
```

7. What is the remote address of the local port listening on port 445?

::

8. How many patches have been applied?

# PS C:\Users\Administrator> Get-Hotfix

```
Source        Description      HotFixID      InstalledBy          InstalledOn
------        -----------      --------      -----------          -----------
EC2AMAZ-5M... Update           KB3176936                          10/18/2016 12:00:00 AM
EC2AMAZ-5M... Update           KB3186568     NT AUTHORITY\SYSTEM  6/15/2017 12:00:00 AM
EC2AMAZ-5M... Update           KB3192137     NT AUTHORITY\SYSTEM  9/12/2016 12:00:00 AM
EC2AMAZ-5M... Update           KB3199209     NT AUTHORITY\SYSTEM  10/18/2016 12:00:00 AM
EC2AMAZ-5M... Update           KB3199986     EC2AMAZ-5M13VM2\A... 11/15/2016 12:00:00 AM
EC2AMAZ-5M... Update           KB4013418     EC2AMAZ-5M13VM2\A... 3/16/2017 12:00:00 AM
EC2AMAZ-5M... Update           KB4023834     EC2AMAZ-5M13VM2\A... 6/15/2017 12:00:00 AM
EC2AMAZ-5M... Update           KB4035631     NT AUTHORITY\SYSTEM  8/9/2017 12:00:00 AM
EC2AMAZ-5M... Update           KB4049065     NT AUTHORITY\SYSTEM  11/17/2017 12:00:00 AM
EC2AMAZ-5M... Update           KB4089510     NT AUTHORITY\SYSTEM  3/24/2018 12:00:00 AM
EC2AMAZ-5M... Update           KB4091664     NT AUTHORITY\SYSTEM  1/10/2019 12:00:00 AM
EC2AMAZ-5M... Update           KB4093137     NT AUTHORITY\SYSTEM  4/11/2018 12:00:00 AM
EC2AMAZ-5M... Update           KB4132216     NT AUTHORITY\SYSTEM  6/13/2018 12:00:00 AM
EC2AMAZ-5M... Security Update  KB4465659     NT AUTHORITY\SYSTEM  11/19/2018 12:00:00 AM
EC2AMAZ-5M... Security Update  KB4485447     NT AUTHORITY\SYSTEM  2/13/2019 12:00:00 AM
EC2AMAZ-5M... Security Update  KB4498947     NT AUTHORITY\SYSTEM  5/15/2019 12:00:00 AM
EC2AMAZ-5M... Security Update  KB4503537     NT AUTHORITY\SYSTEM  6/12/2019 12:00:00 AM
EC2AMAZ-5M... Security Update  KB4509091     NT AUTHORITY\SYSTEM  9/6/2019 12:00:00 AM
EC2AMAZ-5M... Security Update  KB4512574     NT AUTHORITY\SYSTEM  9/11/2019 12:00:00 AM
EC2AMAZ-5M... Security Update  KB4516044     NT AUTHORITY\SYSTEM  9/11/2019 12:00:00 AM
```

# PS C:\Users\Administrator> Get-Hotfix | measure

```
Count    : 20
Average  :
Sum      :
Maximum  :
Minimum  :
Property :
```

9. When was the patch with ID KB4023834 installed?

# PS C:\Users\Administrator> (Get-Command Get-Hotfix).Parameters

```
Key                 Value
---                 -----
Id                  System.Management.Automation.ParameterMetadata
Description         System.Management.Automation.ParameterMetadata
ComputerName        System.Management.Automation.ParameterMetadata
Credential          System.Management.Automation.ParameterMetadata
Verbose             System.Management.Automation.ParameterMetadata
Debug               System.Management.Automation.ParameterMetadata
ErrorAction         System.Management.Automation.ParameterMetadata
WarningAction       System.Management.Automation.ParameterMetadata
InformationAction   System.Management.Automation.ParameterMetadata
ErrorVariable       System.Management.Automation.ParameterMetadata
WarningVariable     System.Management.Automation.ParameterMetadata
InformationVariable System.Management.Automation.ParameterMetadata
OutVariable         System.Management.Automation.ParameterMetadata
OutBuffer           System.Management.Automation.ParameterMetadata
PipelineVariable    System.Management.Automation.ParameterMetadata
```

# PS C:\Users\Administrator> Get-Hotfix -Id KB4023834

```
Source        Description      HotFixID      InstalledBy          InstalledOn
------        -----------      --------      -----------          -----------
EC2AMAZ-5M... Update           KB4023834     EC2AMAZ-5M13VM2\A... 6/15/2017 12:00:00 AM
```

10. Find the contents of a backup file.

# PS C:\Users\Administrator> Get-ChildItem -Path C:\ -Include *.bak* -File -Recurse -ErrorAction SilentlyContinue

```
Directory: C:\Program Files (x86)\Internet Explorer


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        10/4/2019  12:42 AM             12 passwords.bak.txt
```

cat "C:\Program Files (x86)\Internet Explorer\passwords.bak.txt"

```
backpassflag
```

11. Search for all files containing API_KEY

# PS C:\Users\Administrator> Get-ChildItem C:\ * -Recurse | Select-String -Pattern API_KEY

```
C:\Users\Public\Music\config.xml:1:API_KEY=fakekey123
```

12. What command do you do to list all the running processes?

Get-Process

13. What is the path of the scheduled task called new-sched-task?

Get-ScheduledTask

```
TaskPath                                       TaskName                          State
--------                                       --------                          -----
\                                              Amazon Ec2 Launch - Instance I... Disabled
\                                              new-sched-task                    Ready
```

Get-ScheduledTask -TaskName new-sched-task

```
\                                              new-sched-task                    Ready
```

14. Who is the owner of the C:\

# PS C:\Users\Administrator> Get-Acl C:\

```
    Directory:


Path Owner                       Access
---- -----                       ------
C:\  NT SERVICE\TrustedInstaller CREATOR OWNER Allow  268435456...
```

# Basic Scripting Challenge

1. What file contains the password?

## Command

# PS C:\Users\Administrator> Get-ChildItem -Path "C:\Users\Administrator\Desktop\emails\*" -Recurse | Select-String -Pattern Password

```
Desktop\emails\john\Doc3.txt:6:I got some errors trying to access my passwords file - is there any way you can help?
Here is the output I got
Desktop\emails\martha\Doc3M.txt:6:I managed to fix the corrupted file to get the output, but the password is buried
somewhere in these logs:
Desktop\emails\martha\Doc3M.txt:106:password is johnisalegend99
```

## Script

```
$path = "C:\Users\Administrator\Desktop\emails\*"
$string_pattern = "password"
$command = Get-ChildItem -Path $path -Recurse | Select-String -Pattern $string_pattern
echo $command
```

3. What files contains an HTTPS link?

```
$path = "C:\Users\Administrator\Desktop\emails\*"
$string_pattern = "https://"
$command = Get-ChildItem -Path $path -Recurse | Select-String -Pattern $string_pattern
echo $command
```

# Intermediate Scripting

How many open ports did you find between 130 and 140(inclusive of those two)?

```
for($i=130; $i -le 140; $i++){
    Test-NetConnection localhost -Port $i
}
```

# Resources

https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comparison_operators?view=powershell-7.1&viewFallbackFrom=powershell-6
https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/where-object?view=powershell-7.1&viewFallbackFrom=powershell-6
https://docs.microsoft.com/en-us/powershell/scripting/developer/cmdlet/approved-verbs-for-windows-powershell-commands?view=powershell-7
https://learnxinyminutes.com/docs/powershell/