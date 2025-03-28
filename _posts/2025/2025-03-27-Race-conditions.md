---
title: Race Conditions
date: 2025-03-27 21:35:00
categories: [TRYHACKME, ROOMS]
tags: [web,application,server side,burp]      # TAG names should always be lowercase
image: 
 path: /assets/img/posts/2025/03/race-conditions/room_image.webp
---

Uma race condition é uma situação em programas de computador onde o tempo dos eventos influencia o comportamento e o resultado do programa. Normalmente acontece quando uma variável é acessada e modificada por vários threads. Devido à falta de mecanismos de bloqueio adequados e sincronização entre os diferentes threads, um invasor pode abusar do sistema e aplicar um desconto várias vezes ou fazer transações de dinheiro além do seu saldo.

O link da aula [aqui](https://tryhackme.com/room/raceconditionsattacks)

## Multi-Threading

**. Processos:**

- Um processo é uma instância de um programa em execução.
    
- Cada processo possui seu próprio espaço de memória, ou seja, eles são independentes e isolados uns dos outros.
    
- A comunicação entre processos (chamada de IPC, _Inter-Process Communication_) pode ser complexa e consumir mais recursos.
    
- Criar e gerenciar processos geralmente tem um custo maior em termos de tempo e recursos do sistema.

**2. Threads:**

- Uma thread é o menor fluxo de execução dentro de um processo.
    
- Threads dentro de um mesmo processo compartilham o mesmo espaço de memória e recursos, o que facilita a troca de informações entre elas.
    
- Threads são mais leves em termos de consumo de recursos do sistema, e a criação/gerenciamento é mais eficiente do que processos.
    
- Porém, como compartilham a memória, há risco de problemas como _race conditions_ e necessidade de sincronização cuidadosa.
    
**Resumo prático:**

- Use processos para tarefas independentes e isoladas.
    
- Use threads para dividir tarefas dentro de um mesmo processo, especialmente quando elas precisam compartilhar dados entre si.


Abaixo aplicação uitlizando **Flask**, um servidor que atende sequencialmente cada solicitação.

```python
# Import the Flask class from the flask module
from flask import Flask

# Create an instance of the Flask class representing the application
app = Flask(__name__)

# Define a route for the root URL ('/')
@app.route('/')
def hello_world():
    # This function will be executed when the root URL is accessed
    # It returns a string containing HTML code for a simple web page
    return '<html><head><title>Greeting</title></head><body><h1>Hello, World!</h1></body></html>'

# This checks if the script is being run directly (as the main program)
# and not being imported as a module
if __name__ == '__main__':
    # Run the Flask application
    # The host='0.0.0.0' allows the server to be accessible from any IP address
    # The port=8080 specifies the port number on which the server will listen
    app.run(host='0.0.0.0', port=8080)
```

![requests](/assets/img/posts/2025/03/race-conditions/race-conditions-requests.png)

O aplicativo mencionado anteriormente pode ser executado com quatro threads usando o Gunicorn. Gunicorn, também chamado de “Green Unicorn” (Unicórnio Verde), é um servidor HTTP WSGI para Python. WSGI significa *Web Server Gateway Interface*, que serve como uma ponte entre servidores web e aplicações web Python. Especificamente, o Gunicorn pode gerar múltiplos processos de trabalho (*workers*) para lidar com requisições simultaneamente. Ao executar o Gunicorn com a opção `--workers=4`, estamos especificando que queremos quatro *workers* prontos para processar requisições dos clientes; além disso, `--threads=2` indica que cada processo de trabalho pode gerar duas threads.

![PID](/assets/img/posts/2025/03/race-conditions/race-conditions-pids.png)

**You downloaded an instruction booklet on how to make an origami crane. What would this instruction booklet resemble in computer terms?**  
R: `Program`

**What is the name of the state where a process is waiting for an I/O event?**  
R: `Waiting`

## Real World Analogy

Vamos considerar este cenário:

- Uma conta bancária tem $100. 
- Duas threads tentam sacar dinheiro ao mesmo tempo. 
- A Thread 1 verifica o saldo (vê $100) e saca $45. 
- Antes que a Thread 1 atualize o saldo, a Thread 2 também verifica o saldo (incorretamente vê $100) e saca $35.

Não podemos ter 100% de certeza sobre qual thread atualizará o saldo restante primeiro; entretanto, vamos supor que seja a Thread 1. A Thread 1 definirá o saldo restante como $55. Depois disso, a Thread 2 pode definir o saldo restante como $65, caso o problema não seja tratado corretamente. (A Thread 2 calculou que $65 deveria permanecer na conta após o saque porque o saldo era $100 quando ela o verificou.)

Em outras palavras, o usuário fez dois saques, mas o saldo da conta foi descontado apenas pelo segundo saque, porque a Thread 2 sobrescreveu a atualização

Exemplo multi threads em Python:

```python
import threading
import time

def increase_by_10():
    for i in range(1, 11):
        print(f"Thread {threading.current_thread().name}: {i}0% complete")

# Create two threads
thread1 = threading.Thread(target=increase_by_10, name="Thread-1")
thread2 = threading.Thread(target=increase_by_10, name="Thread-2")

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

print("Both threads have finished completely.")
```

![multi threads](/assets/img/posts/2025/03/race-conditions/race-conditions-multi-thread.png)

Não podemos garantir qual thread completará 100% primeiro, executando duas vezes, ou até mais, podemos ter diversos outputs diferentes.

### Causas

De maneira geral, uma causa comum de condições de corrida (_race conditions_) está em recursos compartilhados. Por exemplo, quando várias threads acessam e modificam os mesmos dados compartilhados simultaneamente. Exemplos de dados compartilhados incluem registros de banco de dados e estruturas de dados na memória. Existem muitas causas sutis, mas mencionaremos três das mais comuns:

1. **Execução Paralela:** Servidores web podem executar várias requisições em paralelo para lidar com interações simultâneas de usuários. Se essas requisições acessarem e modificarem recursos compartilhados ou estados da aplicação sem a devida sincronização, isso pode levar a condições de corrida e comportamentos inesperados.
    
2. **Operações em Banco de Dados:** Operações simultâneas em banco de dados, como sequências de leitura-modificação-gravação, podem introduzir condições de corrida. Por exemplo, dois usuários tentando atualizar o mesmo registro ao mesmo tempo podem resultar em dados inconsistentes ou conflitos. A solução está em aplicar mecanismos adequados de bloqueio (_locking_) e isolamento de transações.
    
3. **Bibliotecas e Serviços de Terceiros:** Atualmente, aplicações web frequentemente integram bibliotecas de terceiros, APIs e outros serviços. Se esses componentes externos não forem projetados para lidar com acesso simultâneo de forma apropriada, condições de corrida podem ocorrer quando múltiplas requisições ou operações interagem com eles ao mesmo tempo.


**Does the presented Python script guarantee which thread will reach 100% first? (Yea/Nay)**  
R: `Nay`

**In the second execution of the Python script, what is the name of the thread that reached 100% first?**  
R: `Thread-1`

## Web Application Architecture

**Modelo Cliente-Servidor**
As aplicações web seguem um modelo cliente-servidor:

- **Cliente:** O cliente é o programa ou aplicação que inicia a solicitação de um serviço. Por exemplo, ao navegarmos em uma página da web, nosso navegador solicita a página (arquivo) a um servidor web.
- **Servidor:** O servidor é o programa ou sistema que fornece esses serviços em resposta às solicitações recebidas. Por exemplo, o servidor web responde a uma solicitação HTTP GET e envia uma página HTML (ou arquivo) para o navegador (cliente) que fez a solicitação.
De maneira geral, o modelo cliente-servidor opera por meio de uma rede. O cliente envia sua solicitação pela rede, e o servidor a recebe, processa e devolve o recurso solicitado.

**Aplicação Web Típica**
Uma aplicação web segue uma arquitetura em vários níveis. Tal arquitetura separa a lógica da aplicação em diferentes camadas ou níveis. O design mais comum utiliza três níveis:

- **Camada de Apresentação:** Em aplicações web, essa camada consiste no navegador web do lado do cliente. O navegador renderiza os códigos HTML, CSS e JavaScript.
- **Camada de Aplicação:** Esta camada contém a lógica e a funcionalidade da aplicação web. Ela recebe as solicitações do cliente, as processa e interage com a camada de dados. É implementada usando linguagens de programação do lado do servidor, como Node.js e PHP, entre outras.
- **Camada de Dados:** Esta camada é responsável por armazenar e manipular os dados da aplicação. As operações típicas incluem criar, atualizar, excluir e buscar registros existentes. Geralmente, isso é feito usando um sistema de gerenciamento de banco de dados (DBMS); exemplos de DBMS incluem MySQL e PostgreSQL.

**How many states did the original state diagram of “validating and conducting money transfer” have?**  
R: `2`

**How many states did the **updated** state diagram of “validating and conducting money transfer” have?**  
R: `3`

**How many states did the final state diagram of “validating coupon codes and applying discounts” have?**  
R: `5`

## Exploiting Race Conditions

 A aplicação web possui um sistema de transferência de crédito, entre números de celulares.
 Podemos assim transferir créditos entre duas contas.

Número 1: `07799991337`
Balanço: `5.03`

Número 2: `07113371111`
Balanço: `8.80`

Transferimos `$1` para a número 1 (`07799991337`).

![transfer](/assets/img/posts/2025/03/race-conditions/race-conditiions-transfer.png)

Interceptando a requisição no Burp vemos que é um HTTP `POST`.

![burp](/assets/img/posts/2025/03/race-conditions/race-conditions-burp.png)

Agora no Burp iremos duplicar a requisição 20 vezes e inserir no mesmo grupo de nome `Race conditions`.

![Burp group](/assets/img/posts/2025/03/race-conditions/race-conditions-burp-group.png)

### Diferenças entre os tipos de requisições.

**Enviar Grupo em Sequência por uma Única Conexão**

Esta opção estabelece uma única conexão com o servidor e envia todas as solicitações nas abas do grupo antes de fechar a conexão. Isso pode ser útil para testar possíveis vulnerabilidades de dessincronização no lado do cliente.

**Enviar Grupo em Sequência por Conexões Separadas**

**Como o nome sugere, essa opção estabelece uma conexão TCP, envia uma solicitação do grupo e fecha a conexão TCP antes de repetir o processo para a solicitação subsequente.**

Testamos essa opção para atacar a aplicação web. A captura de tela abaixo mostra 21 conexões TCP para as diferentes solicitações POST do grupo que enviamos.

- O primeiro grupo (rotulado como 1) compreende cinco solicitações bem-sucedidas. Pudemos confirmar que elas foram bem-sucedidas verificando as respectivas respostas. Além disso, notamos que cada uma levou cerca de 3 segundos, conforme indicado pela duração (rotulada como 3).
    
- O segundo grupo (rotulado como 2) mostra 16 solicitações negadas. A duração foi de cerca de 4 milissegundos. É interessante verificar também o **Relative Start Time** (Tempo de Início Relativo).

![Requests](/assets/img/posts/2025/03/race-conditions/race-conditions-request-difference.png)

**Enviar Grupo de Solicitações em Paralelo** 

Escolher enviar as solicitações do grupo em paralelo faria com que o Repeater enviasse todas as solicitações do grupo de uma vez. Nesse caso, notamos o seguinte, conforme mostrado na captura de tela abaixo:

![Requests 2](/assets/img/posts/2025/03/race-conditions/race-conditions-requests-difference2.png)

Ao observar atentamente a captura de tela, notamos que cada solicitação gerou 12 pacotes; no entanto, na tentativa anterior (enviar em sequência), vimos que cada solicitação exigiu apenas 10 pacotes. Por que isso aconteceu?

De acordo com a documentação de envio de solicitações HTTP agrupadas, ao enviar em paralelo, o Repeater implementa diferentes técnicas para sincronizar a chegada das solicitações ao destino, ou seja, elas chegam em um curto intervalo de tempo. A técnica de sincronização depende do protocolo HTTP em uso:

- No caso do HTTP/2+, o Repeater tenta enviar todo o grupo em um único pacote. Em outras palavras, um único pacote TCP transportaria várias solicitações.
    
- No caso do HTTP/1, o Repeater utiliza a sincronização pelo último byte. Este truque é alcançado retendo o último byte de cada solicitação. Somente depois que todos os pacotes são enviados sem o último byte, os últimos bytes de todas as solicitações são enviados. A captura de tela abaixo mostra nossa solicitação POST enviada em dois pacotes.

**You need to get either of the accounts to get more than $100 of credit to get the flag. What is the flag that you obtained?**

Iremos utilizar o envio em paralelo, os outros métodos não irão funcionar, conforma analise acima.

![burp sucess](/assets/img/posts/2025/03/race-conditions/race-conditions-burp-transfer-sucess.png)

## Detection and Mitigation

### Detecção

Detectar condições de corrida da perspectiva do proprietário do negócio pode ser desafiador. Se alguns usuários resgatarem o mesmo cartão-presente várias vezes, provavelmente isso passará despercebido, a menos que os registros sejam verificados ativamente em busca de certos comportamentos. Considerando que condições de corrida podem ser usadas para explorar vulnerabilidades ainda mais sutis, é claro que precisamos da ajuda de testadores de penetração e caçadores de bugs para tentar descobrir essas vulnerabilidades e relatar suas descobertas.

Os testadores de penetração devem entender como o sistema se comporta sob condições normais quando os controles aplicados estão vigentes. Esses controles podem ser: usar uma vez, votar uma vez, avaliar uma vez, limitar ao saldo disponível ou restringir para uso apenas uma vez a cada 5 minutos, entre outros. O próximo passo seria tentar contornar esse limite explorando condições de corrida. Descobrir os diferentes estados do sistema pode ajudar a fazer suposições educadas sobre as janelas de tempo onde uma condição de corrida pode ser explorada. Ferramentas como o Burp Suite Repeater podem ser um ótimo ponto de partida.

### Mitigação

1. **Mecanismos de Sincronização**: Linguagens de programação modernas fornecem mecanismos de sincronização, como bloqueios (locks). Apenas uma thread pode adquirir o bloqueio de cada vez, impedindo outras de acessar o recurso compartilhado até que ele seja liberado.
    
2. **Operações Atômicas**: Operações atômicas se referem a unidades de execução indivisíveis, um conjunto de instruções agrupadas e executadas sem interrupção. Essa abordagem garante que uma operação possa ser concluída sem ser interrompida por outra thread.
    
3. **Transações de Banco de Dados**: Transações agrupam várias operações de banco de dados em uma única unidade. Consequentemente, todas as operações dentro da transação ou são bem-sucedidas como um grupo ou falham como um grupo. Essa abordagem garante a consistência dos dados e previne condições de corrida decorrentes de múltiplos processos modificando o banco de dados simultaneamente.

## Challenge Web App


Aplicação web realiza transações bancárias entre contas.
Antes de explorarmos é essencial entender o comportamento da aplicação.

**Informações importantes percebidas.**

- Valores negativos são aceitos nas taxas, incrementando assim o balanço.

![amount Burp](/assets/img/posts/2025/03/race-conditions/race-conditions-burp-transfer-sucess.png)

- Não é verificado se a taxa é proporcional ao valor transferido.
- Valor recebido não pode ser maior que o fundo de quem está transferindo.

Podemos obter a `flag` somente alterando a taxa para `-1000` dessa forma será creditado `+1000`.

![Flag](/assets/img/posts/2025/03/race-conditions/race-conditions-flag.png)

