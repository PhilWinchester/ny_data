IMAGE_VERSION = latest
RAND_BUILD_ID != head -c10 /dev/urandom | base32

COMPOSE = docker-compose -p ny_data


# ----- Local Development -----

up: FORCE
	${COMPOSE} up -d web

down: FORCE
	${COMPOSE} down -v

sh: FORCE
	${COMPOSE} run --rm web /bin/bash

web: FORCE
	docker exec -it ny_data-web-1 /bin/bash

db: FORCE
	docker exec -it ny_data-db-1 psql -U postgres -w postgres

restart-web: FORCE
	${COMPOSE} restart web

docker-build-web: FORCE
	docker build -t "code/web:${IMAGE_VERSION}" -f "conf/web/Dockerfile" \
		--build-arg "BUILD_VERSION=${IMAGE_VERSION}" .

# docker exec -it ny_data-db-1 psql -U postgres -w postgres
# docker exec -it ny_data-web-1 /bin/bash

# docker-build-mysql: FORCE
# 	docker build -t code/mysql:${IMAGE_VERSION} conf/mysql

# # Login to the mysql server currently connected to the running app server
# mysql-login: FORCE
# 	docker exec --interactive --tty `$(COMPOSE) ps -q mysql` bash -c 'export TERM=xterm; mysql -u root -proot --default-character-set=utf8 ny_data'

# --- Dunno ---

# ref: http://www.gnu.org/software/make/manual/html_node/Force-Targets.html#Force-Targets
FORCE:
