IMAGE_VERSION = latest
RAND_BUILD_ID != head -c10 /dev/urandom | base32

COMPOSE = docker-compose -p "${PROJECT}"

HOST_UID = `id -u`
HOST_GID = `id -g`


# ----- Local Development -----

up: FORCE
	${COMPOSE} up -d web

down: FORCE
	${COMPOSE} down -v

sh: FORCE
	${COMPOSE} run --rm web /bin/bash

docker-build-web: FORCE
	docker build --no-cache -t "code/web:${IMAGE_VERSION}" -f "conf/$*/Dockerfile" \
		--build-arg "BAMX_BUILD_VERSION=${IMAGE_VERSION}" .

docker-build-mysql: FORCE
	docker build -t code/mysql:${IMAGE_VERSION} conf/mysql

# Login to the mysql server currently connected to the running app server
mysql-login: FORCE
	docker exec --interactive --tty `$(COMPOSE) ps -q mysql` bash -c 'export TERM=xterm; mysql -u root -proot --default-character-set=utf8 nyc'

# --- Dunno ---

# ref: http://www.gnu.org/software/make/manual/html_node/Force-Targets.html#Force-Targets
FORCE: