up:
	# Roda a ferramenta em de desenvolvimento
	docker compose --profile api up -d && docker attach api

down:
	# Desliga a ferramente em desenvolvimento
	docker compose --profile api down

locust:
	# Rodar o locust para teste de carga com 4 workers
	docker compose --profile locust up --scale locust-worker=${workers} -d

locust-down:
	# Derrubando o locust e seus workers
	docker compose --profile locust down

install:
	# Instala uma dependencia dentro do container remove flag user do docker compose
	docker compose exec --user root api pip install ${pkg}

remove:
	# Remove uma dependencia dentro do container remove flag user do docker compose
	docker compose exec --user root api pip uninstall ${pkg}

requirements:
	# Lista os requirements do projeto
	docker compose exec api pip freeze

logs:
	# Verificar os logs
	docker compose logs -ft api

shell:
	# Entre no shell do ipython
	docker compose exec api ipython

bash:
	# Entrar no shell
	docker compose exec api bash

packages:
	# Inserir o site-packages dentro do .ignore
	sudo docker cp api:/opt/venv/lib/python3.10/site-packages .ignore/site-packages

### QUALIDADE ###############################################################

path := .

flake8:
	# Roda a folha de estilo
	docker compose exec api flake8 src --count

coverage:
	# Roda os testes no container
	docker compose exec api coverage run --source='src' -m pytest -s -vv --maxfail=1 -p no:warnings --cache-clear --log-cli-level=INFO ${path}

report:
	# Relatório da cobertura de testes
	docker compose exec api coverage report

html:
	# Relatório da cobertura de testes em html
	docker compose exec api coverage html


### MIGRATIONS ################################################################
id := head

migration:
	# Cria a migraçao para ser preenchida
	docker compose exec api alembic revision --autogenerate -m ${name}

migrate:
	# Insere a migração no banco de dados
	docker compose exec api alembic upgrade head

rollback:
	# Volta para a versão anterior
	docker compose exec api alembic downgrade -1