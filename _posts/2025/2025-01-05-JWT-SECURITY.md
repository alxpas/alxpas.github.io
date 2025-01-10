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
Nesse artigo irei estudar e documentar, a aula disponível de JWT na plataforma TryHackMe.

[Aula disponível aqui.](https://tryhackme.com/r/room/jwtsecurity)


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

#### Perguntas
##### What is the common header used to transport the JWT in a request?

Para respondermos a pergunta acima, basta sabermos como é a estrutura de uma requisição JWT e qual é o seu cabeçalho.

Resposta: `Authorization: Bearer header`

## JSON Web Tokens

JWT é um padrão aberto, fornecendo informações para desenvolvedores ou criadores de bibliotecas que querem usar JWTs, a sua estrutura segue da seguinte maneira.

![Estrutura JWT](/assets/img/posts/2025/01/JWT-SCTRUCTURE.webp)

### Estrutura JWT

`Header`:  indica qual é o tipo de token e qual algoritmo está sendo utilizado.

`Payload`: corpo do token, contém informações  de reinvindicações, as reinvindicações são pré-definidas como sendo públicas ou privadas pelo padrão JWT.

`Signature`: a parte do token que fornece o método que será utilizado para garantir a autenticidade do token.

### Algoritmos de assinatura

Existem diversos algoritmos de assinatura, abaixo será explicado os principais.

`None`: significa que nenhum algoritmo de assinatura será utilizado, desta forma, JWT não será capaz de verificar a autenticidade do token.

`Symmetric Signing`: algoritmo simétrico, como HS265, criam uma assinatura e anexando um valor secreto para o cabeçalho e corpo do JWT antes de gerar um valor em hash. A verificação de assinatura, pode ser executada por qualquer sistema que tenha em posse o valor secreto.

`Asymmetric Signing`: algoritmo de assinatura assimétrica, como RS256, cria uma assinatura usando uma chave privada, para assinar o cabeçalho e o corpo do JWT, é criado gerando uma hash e depois criptografando a hash com a chave privada. A verificação pode ser realizada por qualquer sistema que tenha a chave pública.

### Segurança na assinatura

JWTs podem ser criptografados (chamadas  de JWEs), mas o poder principal dos JWTs vem da assinatura. Uma vez que um JWT é assinado, ele pode ser enviado ao cliente, que pode usar este JWT sempre que necessário, realizando dessa maneira um servidor centralizado de autenticação que cria JWT para diversas aplicações.

### Perguntas

#### HS256 is an example of what type of signing algorithm?

HS256 é utilizado para realizar assinaturas simétricas.

Resposta: `Symmetric`

#### RS256 is an example of what type of signing algorithm?

RS256 é utilizado para realizar assinaturas assimétricas.

Resposta: `Asymmetric`

#### What is the name used for encrypted JWTs?

O nome é JWEs

Resposta:`JWEs`

## Divulgação de informações confidenciais

O primeiro problema que iremos nos aprofundar é sobre a exposição de informações sensíveis dentro do JWT.

Em um gerenciamento de sessão baseado em `cookie` as informações são armazenadas em parâmetros do lado servidor, esses valores não são expostos do lado do cliente e podem ser recuperados somente do lado do servidor. Entretanto com tokens, as reinvindicações são expostas em JWT no lado do cliente, alguns exemplos de informações que podem ser expostas.

- Credenciais como senhas em hash, ou ainda pior, em texto claro.
- Exposição da rede interna, como endereços de hosts, hostname e servidores de autenticação.

### Exemplo 1:

```shell
┌──(root㉿kali)-[/home/alex]
└─# 
curl -H 'Content-Type: application/json' -X POST -d '{ "username" : "user", "password" : "password1" }' http://10.10.63.229/api/v1.0/example1
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJwYXNzd29yZCI6InBhc3N3b3JkMSIsImFkbWluIjowLCJmbGFnIjoiVEhNezljYzAzOWNjLWQ4NWYtNDVkMS1hYzNiLTgxOGM4MzgzYTU2MH0ifQ.TkIH_A1zu1mu-zu6_9w_R4FUlYadkyjmXWyD5sqWd5U"
} 
```


Acima vemos a resposta da nossa requisição `POST` a API, nossa estrutura em JWT é montada, com caracter "." sendo o delimitador de cada campo.

`header:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9`

`Payload:eyJ1c2VybmFtZSI6InVzZXIiLCJwYXNzd29yZCI6InBhc3N3b3JkMSIsImFkbWluIjowLCJmbGFnIjoiVEhNezljYzAzOWNjLWQ4NWYtNDVkMS1hYzNiLTgxOGM4MzgzYTU2MH0ifQ`

`Signature: TkIH_A1zu1mu-zu6_9w_R4FUlYadkyjmXWyD5sqWd5U`

A decodificação do token pode ser realizada manualmente ou com ferramentas, na lição é fornecido a ferramenta [jwt io](https://jwt.io/).
Outra solução, que podemos executar localmente, é a ferramenta [Cyber Chef](https://cyberchef.org/)

Resultado da nossa decodificação.

![JWT-IO](/assets/img/posts/2025/01/JWT-IO.webp)

### Erros de desenvolvimento

Exemplo de informações confidenciais sendo fornecidas após requisição.

```python
payload = { 
	"username" : username, 
	"password" : password, 
	"admin" : 0, 
	"flag" : "[redacted]" 
	} 

access_token = jwt.encode(payload, self.secret, algorithm="HS256")
```


#### Correção

Informações valiosas não podem ser adicionadas na resposta do JWT que será enviado para o lado do cliente, ao invés disso, esses valores devem ficar armazenados no lado do servidor, quando requisitados, o nome de usuário pode ser lido pelo JWT verificador , que realiza um lookup desses valores.

```python
payload = jwt.decode(token, self.secret, algorithms="HS256") 
username = payload['username'] 
flag = self.db_lookup(username, "flag")
```


**payload = jwt.decode(token, self.secret, algorithms="HS256")**:

- Decodifica o token JWT utilizando a chave secreta (`self.secret`) e o algoritmo HS256.
- O resultado da decodificação é um payload, que é um dicionário contendo as informações contidas no token.

**username = payload['username']**:

- Extrai o valor associado à chave 'username' do payload. Esse valor é armazenado na variável `username`.

**flag = self.db_lookup(username, "flag")**:

- Realiza uma busca na base de dados (`self.db_lookup`) utilizando o `username` e a chave "flag".
- O resultado dessa busca é armazenado na variável `flag`.

### Pergunta
#### What is the flag for example 1?

A resposta foi encontrada quando realizamos a requisição e decodificamos o JWT.

Resposta: `THM{9cc039cc-d85f-45d1-ac3b-818c8383a560}`