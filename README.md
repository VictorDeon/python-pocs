# python-pocs

POCs criadas em python para testar scripts e libs em python.

***
### Como subir a aplicação
***

1. Suba os emuladores que deseja usar com `docker compose --profile <emulators> up -d` e crie o network se necessário `docker network create vksoftware`.

2. Antes de subir pela primeira vez **comente o volume como abaixo** e crie uma pasta chamada `.ignore` e suba a aplicação com `docker compose --profile api up`

```yml
volumes:
    - .:/software
    # - .ignore/site-packages:/opt/venv/lib/python3.10/site-packages
```

3. Ao subir execute `make packages` para criar os pacotes dentro do `.ignore/site-packages` e desligue o servidor `docker compose --profile api down`

4. Descomente o volume e rode novamente o `docker compose --profile api up`.

5. No vscode vai na aba `Executar` e clique em `Iniciar Depuração`, com isso o servidor vai subir e vc vai poder usar os
breakpoints para realizar o debug da aplicação.

```yml
volumes:
    - .:/software
    - .ignore/site-packages:/opt/venv/lib/python3.10/site-packages
```

Nas proximas vezes só precisa executar os emuladores `docker compose --profile <emulators> up -d` e depois a api `docker compose --profile api up` com isso é só ir na aba `Executar` e clique em `Iniciar Depuração`.

### TODO:

#### Requests
* Web Scraping

#### Engines
* 3º Instrumentalização com o new relic
* Tarefas distribuidas com celery e habbitmq

#### Outputs
* Finalizar o leitor de PDF
* Implementar inserçao de arquivos PDF, XML, PNG, TXT, CSV, YAML, ZIP e etc via endpoint, ler seus dados e retornar via JSON
* Receber dados de registro de usuários por SOAP, GRAPHQL e outros protocolos

#### Scripts
* Criar um interface com o tkinter para o CRUD de usuários definir via header.
* Script que recebe os dados dos usuários por fila, valida os dados e enviar para outra fila para armazenamento no banco de dados (pubsub, rabitmq, sqs, local).
* Script que consume todos os arquivos CSV da pasta de upload, pegar os dados de usuários valida os dados, salva no banco e enviar o excel para outra pasta de processados (cloud storage, S3, local).
* Mudar de serviços pubsub/storage só pela instanciação do singleton.

#### CRUD
* Autenticação e Autorização - vwauth
* Criar no repository os CRUD usando NoSQL MongoDb
* Deleção lógica:
    - Na criação, se o objeto já existir ao inves de criar, coloque is_deleted False e atualize os dados
    - Na criação/atualização de qualquer modelo não pode se relacionar com outra model com is_deleted True
    - Na busca e listagem, remover os que tem o is_deleted True
    - Na atualização não atualizar se is_delete for True (mensagem de error)
    - Na remoção não deletar e inserir o is_deleted como True se não tiver, se ja tiver não faz nada. Fazer o is_deleted True em todos os relacionamentos
    - Em ambiente de teste deixar a deleção normal

#### Projects
* Implementar blockchain
* Desenvolver padrões de projetos
* Criando estruturas de dados
* Projeto com SFTP
* Gerar lib python
* Chatbot com openAI
* Criar um jogo com pygames
* Visão computacional
* Machine learning
* Data-Science

#### Quality
* Testes automatizados
* Incrementar o locust com novos clients (SFTP, AMQP) e novos handlers inserindo novos dados nos eventos de sucesso e falha
usar como base o curso de locust da udemy