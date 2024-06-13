# python-pocs

POCs criadas em python para testar scripts e libs em python

TODO:

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