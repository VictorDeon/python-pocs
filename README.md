# python-pocs

POCs criadas em python para testar scripts e libs em python

TODO:

* CRUD de usuários (Criar, Listar, Visualizar, Deletar, Atualizar, Autenticar) - vwauth
* CRUD de usuários usando mongodb
* CRUD de usuários usando mysql
* CRUD de usuários usando postgres
* CRUD de usuários usando sqlite
* Testes automatizados do CRUD de usuários


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