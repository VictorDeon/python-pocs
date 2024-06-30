# python-pocs

POCs criadas em python para testar scripts e libs em python usando a Clean Architecture.

### Clean Architecture

![clean-architecture](https://github.com/VictorDeon/python-notebook/assets/14116020/cd51c91a-a0cb-405a-b90c-5b47b54ba5b5)

#### Entities

A pasta **infrastructure** é a camada de **Entities** do clean architeture.
Ou seja, é a camada que encapsula as regras de negócio de toda a empresa. É o espelho de todos os dados da empresa
e a definição de todos os casos de uso a ser implementados.

#### User Cases

A pasta **domains** é a camada **User Cases** do clean architecture. Esse contém as regras
de negócios específicas do aplicativo. Ele encapsula e implementa todos os casos de uso do sistema definidos.

#### Interface Adapters

Nesta camada temos a pasta **adapters** com suas respectivas **controllers**. É a camada específica que a gente retira os dados de entrada, por exemplo, os dados HTTP trata eles para jogar nos casos de uso.

#### Frameworks & Drivers

A camada mais externa geralmente é composta por frameworks e ferramentas como banco de dados, arquivos, UI, entre outros tipos de entradas e dados que o usuário pode enviar. Essa camada está na pasta **application**

#### Ordem de criação

1. adapters/dtos
2. infrastructure/repositories ou daos
3. adapters/presenters
4. domains/user_cases
5. adapters/controllers
6. application/api/routes

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

* Endpoint com o CRUD de usuários e seus relacionamentos (Criar, Listar, Visualizar, Deletar, Atualizar)
    - Criar todos os presents + tests
    - Criar todos os user_cases + tests
    - Criar todos os controllers + tests
    - Criar todas as rotas + tests
* Autenticação e autorização - vwauth
* Desenvolver vários tipos de consumos de APIs usando corotines, queues, threads e processos
* Inserir um sistema de logs inteligentes
* Finalizar o leitor de PDF
* Criar um interface com o tkinter para o CRUD de usuários definir via header.
* Endpoints que faz o upload de um arquivo excel com dados de usuários.
* Script que consume todos os arquivos excel da pasta de upload, pegar os dados e armazenar em varios bancos de dados
e arquivos e enviar o excel para outra pasta de processados.
    - Mongodb
    - MySql
    - Postgres
    - SqLite
    - CSV
    - JSON
* Endpoints de consulta desses dados de usuários pelos diversos meios acima.
* Sistema de autenticação e autorização
* Testes automatizados
