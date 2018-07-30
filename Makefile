docker_compose_up:
	@docker-compose -f deploy/docker-compose.yml up -d
	@printf "Waiting for PostgreSQL."
	@until docker exec -it mgallery-postgres psql -U mgallery -c '\l' > /dev/null; do printf "."; sleep 1; done
	@until docker exec -it mgallery-postgres-test psql -U mgallery -c '\l' > /dev/null; do printf "."; sleep 1; done
	@printf " Connected!\n"

docker_compose_down:
	@docker-compose -f deploy/docker-compose.yml down


make_test:
	@docker exec -it mgallery-app pytest

test: docker_compose_up make_test docker_compose_down


admin:
	docker exec -it mgallery-app python main.py -a

compare:
	docker exec -it mgallery-app python main.py -c

merge:
	docker exec -it mgallery-app python main.py -m

search:
	docker exec -it mgallery-app python main.py -s


reload-sv:
	docker exec -it mgallery-app supervisorctl restart mgallery:

stop-sv:
	docker exec -it mgallery-app supervisorctl stop mgallery:

start-sv:
	docker exec -it mgallery-app supervisorctl start mgallery:


bash:
	docker exec -it mgallery-app bash

ci:
	circleci build

flake:
	flake8

build:
	cd deploy/ && docker build -t mantiby/mgallery:latest .



psql:
	docker exec -it mgallery-postgres psql -U mgallery

psql-test:
	docker exec -it mgallery-postgres-test psql -U mgallery

pg_dump:
	docker exec -it mgallery-postgres pg_dump -U mgallery -d mgallery > deploy/database/mgallery.sql

migrate:
	docker exec -it mgallery-app bash -c "cd ../deploy && alembic upgrade head"

makemigrations:
	docker exec -it mgallery-app bash -c "cd ../deploy && alembic revision --autogenerate"