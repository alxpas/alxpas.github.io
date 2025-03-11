---
title: Injectics
date: 2025-03-11 11:41:00
categories: [TRYHACKME, CTF]
tags: [web,sql,ssti,enumeration,php]      # TAG names should always be lowercase
image: 
 path: /assets/img/posts/2025/03/injectics/room-image.webp

---

A CTF focused on injection and enumeration attacks, where we first identify the field vulnerable to `SQL injection`. After that, we must use obfuscation techniques to bypass the verification of `special characters`. Once access is obtained, we need to understand the behavior of the update feature to carry out a `second-order SQL` attack, thereby deleting the table and triggering the default credentials registration. In the administrative panel, we should analyze which `server template` is in use to perform the SSTI attack.


## Recon

First, scan TCP SYN with the Nmap tool.

```shell
┌──(root㉿estudos)-[/home/alex]
└─# nmap -Pn -sS --open  10.10.131.224 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-03-07 18:33 -03
Nmap scan report for 10.10.131.224
Host is up (0.36s latency).
Not shown: 991 closed tcp ports (reset), 7 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 5.98 seconds
                           
┌──(root㉿estudos)-[/home/alex]
└─# nmap -Pn -sS --open  -p- 10.10.131.224
Starting Nmap 7.95 ( https://nmap.org ) at 2025-03-07 18:33 -03
Nmap scan report for 10.10.131.224
Host is up (0.32s latency).
Not shown: 65456 closed tcp ports (reset), 77 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 100.55 seconds
```


Comment on the source code's home page.

```html
<!-- Website developed by John Tim - dev@injectics.thm-->
```

With the `ffuf` tool, we discover directories.

![injectics-ctf-ffuf-initial](/assets/img/posts/2025/03/injectics/injectics-ctf-ffuf-initial.png)

In the **vendor** directory, we discover the `twig` directory.

![injectics-ctf-ffuf-vendor](/assets/img/posts/2025/03/injectics/injectics-ctf-ffuf-vendor.png)

Directories discovers in the `phpmyadmin`

![injectics-ctf-ffuf-phpmyadmin](/assets/img/posts/2025/03/injectics/injectics-ctf-ffuf-phpmyadmin.png)

On the login page, there is an option to log in as admin.

```
.../login.php
.../adminLogin007.php
```

The behavior of the two pages when authentication fails is the same.

![injectics-ctf-login-authentication](/assets/img/posts/2025/03/injectics/injectics-ctf-login-authentication.png)

Special character (`'`) is detected in `login.php`.

![injectics-ctf-apostrophe](/assets/img/posts/2025/03/injectics/injectics-ctf-apostrophe.png)

In the file `script.js`, we saw how authentication works and the keywords are detected.

![injectics-ctf-sourcecode-keywords](/assets/img/posts/2025/03/injectics/injectics-ctf-sourcecode-keywords.png)

Back on the source's homepage, there's another comment about the file named `mail.log`.

![injectics-ctf-maillog](/assets/img/posts/2025/03/injectics/injectics-ctf-maillog.png)

`"automatically insert default credentials into the "users" table if it is ever deleted...`  

## Exploring

For authentication bypass, we should first use URL encoding to prevent the detection of our special characters.

Wordlist to perform an SQL injection:

```
https://github.com/payloadbox/sql-injection-payload-list/blob/master/Intruder/exploit/Auth_Bypass.txt
```

That payload was successful: `' OR 'x'='x'#;`

![injectics-ctf-burp-bypass](/assets/img/posts/2025/03/injectics/injectics-ctf-burp-bypass.png)

Access obtained.

![injectics-ctf-leaderboards](/assets/img/posts/2025/03/injectics/injectics-ctf-leaderboards.png)

We can update the leaderboards of medals. When we insert an apostrophe `'`, we encounter an error: `Error updating data.` To use the apostrophe, we should convert it to URL encode `%27`. If we use a semicolon `;` right after updating, we will update the number of gold medals for all countries.

![injectics-ctf-update-leaderboard](/assets/img/posts/2025/03/injectics/injectics-ctf-leaderboards.png)

![injectics-ctf-update-medals](/assets/img/posts/2025/03/injectics/injectics-ctf-update-medals.png)

## Obtaining Administrative Access

The SQL update statement is likely written as follows.

`UPDATE Leaderboard SET gold=10; WHERE country = 'USA'`

When we insert a semicolon, we ignore the `WHERE` clause, thus updating all the other countries.

We will use `; DROP TABLES users -- -` to delete the table and create the default credentials for the `mail.log` file.

![injectics-ctf-droptable](/assets/img/posts/2025/03/injectics/injectics-ctf-droptable.png)

On the `Login as Admin` page, we log in using the administrator credentials.

![injectics-ctf-panel-admin](/assets/img/posts/2025/03/injectics/injectics-ctf-panel-admin.png)

## CVE-2022-23614

We can update certain user data in `Update Profile`.

![injectics-ctf-update-profile](/assets/img/posts/2025/03/injectics/injectics-ctf-update-profile.png)

The changed `first name` is displayed in `dashboard.php`.

![injectics-ctf-panel-name-update](/assets/img/posts/2025/03/injectics/injectics-ctf-panel-name-update.png)

We know that there is a `Twig` server template on the server. We still don't know its version, so we will search for `JSON` files.

![injectics-ctf-ffuf-composer](/assets/img/posts/2025/03/injectics/injectics-ctf-ffuf-composer.png)

![injectics-ctf-twig-version](/assets/img/posts/2025/03/injectics/injectics-ctf-twig-version.png)

Flow of the SSTI test.

![injectics-ctf-flow-ssti](/assets/img/posts/2025/03/injectics/injectics-ctf-flow-ssti.png)

Testing an SSTI attack on the name field.

![injectics-ctf-attack-ssti](/assets/img/posts/2025/03/injectics/injectics-ctf-attack-ssti.png)

The application is vulnerable to SSTI attacks.

![injectics-ctf-49](/assets/img/posts/2025/03/injectics/injectics-ctf-49.png)

While researching on the internet, I found a proof of concept for this vulnerability.

PoC: `https://github.com/4rtamis/CVE-2022-23614`

The payload executes successfully.

I took some time to figure out how to use the `sort` filter to display the command output. I found the link above and decided to test `passthru`.

`https://www.yeswehack.com/learn-bug-bounty/server-side-template-injection-exploitation`

{: .prompt-info }
> passthru() is a function used to execute an external command and display its raw output directly to the browser or terminal, often without buffering. It's commonly used for executing system-level commands.

![injectics-ctf-id](/assets/img/posts/2025/03/injectics/injectics-ctf-id.png)

The payload was executed successfully. Now we can prepare our command to obtain a reverse shell.

![injectics-ctf-reverse](/assets/img/posts/2025/03/injectics/injectics-ctf-reverse.png)

The reverse shell was obtained. We can retrieve the last flag.

![injectics-ctf-flag](/assets/img/posts/2025/03/injectics/injectics-ctf-flag.png)






     

