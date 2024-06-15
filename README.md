# python-pocs

POCs criadas em python para testar scripts e libs em python usando a Clean Architecture.

### Clean Architecture



#### Entities

A pasta **models** e **interfaces** do domínio do nosso projeto é a camada de **Entities** do clean architeture.
Ou seja, é a camada que encapsula as regras de negócio de toda a empresa. É o espelho de todos os dados da empresa
e a definição de todos os casos de uso a ser implementados.

#### User Cases

A pasta **user_cases** do domínio do nosso projeto é a camada **User Cases** do clean architecture. Esse contém as regras
de negócios específicas do aplicativo. Ele encapsula e implementa todos os casos de uso do sistema definidos na camada de
**Entities** pelas **interfaces**.


### TODO:

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
* Endpoint com o CRUD de usuários (Criar, Listar, Visualizar, Deletar, Atualizar, Autenticar) - vwauth
* Testes automatizados
* Desenvolver vários tipos de consumos de APIs usando corotines, threads e processos
* Inserir um sistema de logs inteligentes
* Criar um interface com o tkinter para o CRUD de usuários.

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