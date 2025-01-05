---
title: JWT - SECURITY
date: 2025-01-05 10:44:00
categories: [TRYHACKME, ROOMS, WEB APPLICATION PENTEST]
tags: [api,tryhackme,web,applicatio,jwt,pentest]      # TAG names should always be lowercase
image: 
 path: /assets/img/posts/2025/01/room-JWT.png

---

# Objetivos

1. Aprender sobre autenticação baseada em token.
2. Aprender sobre JSON web tokens (JWTs).
3. Aprender o porque JWT são populares.
4. Aprender sobre segurança no uso de JWT.
5. Aprender como atacar vulnerabilidade na implementação de JWT.


## Introdução

Um dos motivos  da popularidade das API (Application Programming Interfaces) é sua vantagem  de ser usada em diversas interfaces diferentes, com uma única API podemos conversar com uma aplicação web ou mobile, simultaneamente se necessário, além disso, pensando pelo lado da segurança, podemos implementar controles mais centralizados do lado do servidor.

## Gerenciamento de Sessão baseado em Token.

É algo relativamente novo, onde a aplicação web fornece um token dentro de uma requisição `body` , no lado do cliente o JavaScript lê essa informação e armazena o token localmente dentro da pasta do navegador. Quando o cliente realiza uma requisição o JavaScript carrega a informação do token armazenado localmente e anexa ao cabeçalho da requisição, o formato mais comum de token é o **JWT (JSON Web Token)**.

Formato do cabeçalho:
`Authorization: Bearer header`


### Projeto de API

A API para estudo e documentação foi desenvolvida em Python Flask, sendo assim os códigos dos exemplos serão em Python.

#### API Endpoints

O projeto de API tem um único endpoint, exemplo `http://HOST/api/v1.0/exampleX`, o `X` é substituído pelo exemplo que estamos estudando. O endpoint é acessado usando dois métodos HTTP.

 **POST**: Para autenticar e receber seu JWT você precisa realizar uma requisição POST, com as credenciais fornecidas em formato JSON.

 **GET**: Para obter detalhes sobre seu usuário e, executar a escalação de privilégios.

#### Credenciais de API

Para autenticar na API o corpo do formato JSON deve ser enviado da seguinte forma:

 **username**: nome de usuário
 **password**: senha**X**

#### Exemplos de API

Abaixo duas requisições, utilizando o `curl`.
Para autenticação utilizamos a requisição abaixo:

```shell
curl -H 'Content-Type: application/json' -X POST -d '{ "username" : "user", "password" : "passwordX" }' http://10.10.173.181/api/v1.0/exampleX
```


`Content-Type: application/json`:  cabeçalho utilizado para comunicação entre sistemas, por exemplo cliente servidor, ele informa para navegador como interpretar o conteúdo enviado.

Para verificação de usuário a requisição abaixo pode ser utilizada:

```shell
curl -H 'Authorization: Bearer [JWT token]' http://10.10.173.181/api/v1.0/example2?username=Y
```

Onde `Y` após parâmetro `username` pode ser `user` ou `admin`.

`JWT token` : deve ser substituído pela resposta da primeira requisição.


#### Exemplo de token

Quando realizamos uma requisição com usuário `user` recebemos um token, com usuário `admin` recebemos a mensagem de credenciais incorretas.

```shell
┌──(root㉿kali)-[/home/alex]
└─# 
curl -H 'Content-Type: application/json' -X POST -d '{ "username" : "user", "password" : "password1" }' http://10.10.173.181/api/v1.0/example1
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJwYXNzd29yZCI6InBhc3N3b3JkMSIsImFkbWluIjowLCJmbGFnIjoiVEhNezljYzAzOWNjLWQ4NWYtNDVkMS1hYzNiLTgxOGM4MzgzYTU2MH0ifQ.TkIH_A1zu1mu-zu6_9w_R4FUlYadkyjmXWyD5sqWd5U"
}

┌──(root㉿kali)-[/home/alex]
└─# 
curl -H 'Content-Type: application/json' -X POST -d '{ "username" : "admin", "password" : "password1" }' http://10.10.173.181/api/v1.0/example1
{
  "message": "Incorrect Username or Password"
}

```

#### What is the common header used to transport the JWT in a request?

Para respondermos a pergunta acima, basta sabermos como é a estrutura de uma requisição JWT e qual é o seu cabeçalho.

Resposta: `Authorization: Bearer header`