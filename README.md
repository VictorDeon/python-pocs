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

### TODO:

* Arrumar banco de dados sqlalchemy find_user
* Colocar o not_blocked_requests no mesmo modelo dos outros
* Endpoint com o CRUD de usuários (Criar, Listar, Visualizar, Deletar, Atualizar, Autenticar) - vwauth
* Desenvolver vários tipos de consumos de APIs usando corotines, threads e processos
* Inserir um sistema de logs inteligentes
* Finalizar o leitor de PDF
* Criar um interface com o tkinter para o CRUD de usuários.
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

***
### Visual Studio Code
***

Configura o autocomplete e analises, no arquivo `settings.json` faça:

```json
{
    "files.exclude": {
        ".pytest_cache": true,
        "**/__pycache__": true
    },
    "python.analysis.extraPaths": [
        ".ignore/site-packages"
    ],
    "python.autoComplete.extraPaths": [
        ".ignore/site-packages"
    ]
}
```