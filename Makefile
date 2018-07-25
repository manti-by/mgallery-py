admin:
	docker exec -it mgallery-app python main.py -a

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

test:
	docker exec -it mgallery-app pytest

flake:
	flake8

build:
	cd deploy/ && docker build -f Dockerfile -t mantiby/mgallery:latest .



psql:
	docker exec -it mgallery-postgres psql -U mgallery

psql-test:
	docker exec -it mgallery-postgres-test psql -U mgallery

pg_dump:
	docker exec -it mgallery-postgres pg_dump -U mgallery -d mgallery > deploy/database/mgallery.sql

migrate:
	docker exec -it mgallery-app cd ../deploy && alembic upgrade head