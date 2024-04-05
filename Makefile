install:
	# Instala uma dependencia dentro do container
	docker compose exec pocs pip3 install ${pkg}

remove:
	# Remove uma dependencia dentro do container
	docker compose exec pocs pip3 uninstall ${pkg}

requirements:
	# Lista os requirements do projeto
	docker compose exec pocs pip3 freeze

logs:
	# Verificar os logs
	docker compose logs -ft pocs

shell:
	# Entre no shell do ipython
	docker compose exec pocs ipython

bash:
	# Entrar no shell
	docker compose exec pocs bash

packages:
	# Inserir o site-packages dentro do .ignore
	sudo docker cp pocs:/usr/local/lib/python3.10/site-packages .ignore/site-packages

rmi:
	# Remove as imagens none
	docker rmi $(docker images --filter "dangling=true" -q --no-trunc)

debug:
	# Inserir o pdb no codigo e o método pdb.set_trace() (n, s, l)
	docker attach pocs

### QUALIDADE ###############################################################

path := .

flake8:
	# Roda a folha de estilo
	docker compose exec pocs flake8 . --count

coverage:
	# Roda os testes no container
	docker compose exec pocs coverage run --source='.' -m pytest -s -vv --maxfail=1 -p no:warnings test/${path}

report:
	# Relatório da cobertura de testes
	docker compose exec pocs coverage report

html:
	# Relatório da cobertura de testes em html
	docker compose exec pocs coverage html
