start:
	@docker-compose -f deploy/docker-compose.yml up -d
	@printf "Waiting for PostgreSQL."
	@until docker exec -it mgallery-postgres psql -U mgallery -c '\l' > /dev/null; do printf "."; sleep 1; done
	@printf " Connected!\n"

stop:
	@docker-compose -f deploy/docker-compose.yml stop

destroy:
	@docker-compose -f deploy/docker-compose.yml down


admin:
	docker exec -it mgallery-app python main.py -a

merge:
	docker exec -it mgallery-app python main.py -m

scan:
	docker exec -it mgallery-app python main.py -s

build:
	cd deploy/ && docker build -t mantiby/mgallery:latest .


reload-uwsgi:
	docker exec -it mgallery-app supervisorctl restart mgallery:uwsgi


venv:
	virtualenv -p $(shell which python3) --no-site-packages --prompt='mx-' ../venv

pip:
	pip install -Ur deploy/requirements.txt


bash:
	docker exec -it mgallery-app bash

ci:
	circleci build

check:
	black -t py37 app/
	isort app/*.py
	flake8


psql:
	docker exec -it mgallery-postgres psql -U mgallery

pg_dump:
	docker exec -it mgallery-postgres pg_dump -U mgallery -d mgallery > deploy/database/database.sql
	sudo chown -R ${USER}:${GROUP} deploy/database/

migrate:
	docker exec -it mgallery-app bash -c "cd ../deploy && alembic upgrade head"

makemigrations:
	docker exec -it mgallery-app bash -c "cd ../deploy && alembic revision --autogenerate"
	sudo chown -R ${USER}:${GROUP} deploy/database/
