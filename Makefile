GREEN   = \033[0;32m
RED     = \033[0;31m
YELLOW  = \033[0;33m
BLUE    = \033[0;34m
MAGENTA = \033[0;35m
CYAN    = \033[0;36m
RESET   = \033[0m

IS_SCHOOL := $(shell \
	if [ -n "$$SESSION_MANAGER" ] && echo "$$SESSION_MANAGER" | grep -q "42mulhouse.fr"; then \
		echo true; \
	else \
		echo false; \
	fi \
)

ifeq ($(IS_SCHOOL), true)
	DB_VOLUME := $(HOME)/goinfre/db.volume
	APP_VOLUME := $(HOME)/goinfre/app.volume
else
	DB_VOLUME := $(HOME)/42/Docker_volume/db
	APP_VOLUME := $(HOME)/42/Docker_volume/app
endif

.PHONY: all fclean clean stop down start re restart create-dir resume

all: create-dir down
	@bash -c 'source .env && exec docker compose up -d'

prod: create-dir down
	@bash -c 'source .env && exec docker compose -f ./docker-compose.yml -f ./docker-compose.prod.yml up --build -d'

fclean: stop clean
	@printf "${YELLOW}Withdrawal of Docker images...${RESET}\n"
	@docker rmi -f my_app postgres:17 dpage/pgadmin4 busybox || true
	@printf "${GREEN}Images deleted.${RESET}\n"

fclean2: stop clean
	@printf "${YELLOW}Removing containers, images, and volumes from docker-compose...${RESET}\n"
	@docker compose down --volumes --rmi all || echo "${RED}Could not fully clean with docker compose down${RESET}"
	@docker rmi -f busybox || echo "${CYAN}busybox image not found or already removed.${RESET}"
	@printf "${GREEN}All docker-compose resources have been removed.${RESET}\n"

stop:
	@docker compose stop

down:
	@docker compose down -v

start: create-dir
	@bash -c 'source .env && docker compose up -d'
	@printf "${BLUE}Waiting for my_app...${RESET}\n"
	@until docker ps | grep -q "my_app"; do sleep 1; done
	@docker exec -it my_app bash

resume:
	@printf "${BLUE}Restarting all stopped containers...${RESET}\n"
	@docker ps -a -f "status=exited" --format '{{.Names}}' | xargs -r docker start
	@printf "${GREEN}All previously stopped containers have been restarted.${RESET}\n"

re: clean fclean all

restart:
	@$(MAKE) stop
	@sleep 1
	@$(MAKE) start

create-dir:
	@if [ ! -d "$(DB_VOLUME)" ] || [ ! -d "$(APP_VOLUME)" ]; then \
		mkdir -p $(DB_VOLUME) $(APP_VOLUME); \
		printf "${BLUE}Bind mounts created (only if necessary):${RESET}\n";\
		printf "  - $(DB_VOLUME)\n"; \
		printf "  - $(APP_VOLUME)\n"; \
	fi

env:
	@printf "${BLUE}Updating .env variables based on environment...${RESET}\n"
	@( grep -q '^APP_VOLUME=' .env && sed -i 's|^APP_VOLUME=.*|APP_VOLUME=$(APP_VOLUME)|' .env || echo "APP_VOLUME=$(APP_VOLUME)" >> .env )
	@( grep -q '^DB_VOLUME=' .env && sed -i 's|^DB_VOLUME=.*|DB_VOLUME=$(DB_VOLUME)|' .env || echo "DB_VOLUME=$(DB_VOLUME)" >> .env )
	@printf "${GREEN}.env file updated.${RESET}"\n;

clean:
	@printf "${YELLOW}Cleaning PostgreSQL DB...${RESET}\n"
	@if docker container inspect my_postgres > /dev/null 2>&1; then \
		if docker ps -q -f name=my_postgres | grep -q .; then \
			printf "${BLUE}Container my_postgres is running. Withdrawal by docker exec.${RESET}\n"; \
			docker exec my_postgres bash -c "rm -rf /var/lib/postgresql/data/*" || echo "${RED}Failure of the withdrawal by container${RESET}"; \
		else \
			printf "${CYAN}Container my_postgres exists but is not running. Temporary start.${RESET}\n"; \
			docker start my_postgres > /dev/null; \
			sleep 3; \
			docker exec my_postgres bash -c "rm -rf /var/lib/postgresql/data/*" || echo "${RED}Failure after starting.${RESET}"; \
			printf "${BLUE}Stopping my_postgres container.${RESET}\n"; \
			docker stop my_postgres > /dev/null; \
		fi \
	else \
		printf "${RED}Container my_postgres does not exist. Skipping container-based cleaning.${RESET}\n"; \
	fi
	@printf "${MAGENTA}Final check with Busybox to clean bind mounted volume...${RESET}\n"
	@docker run --rm -v $(DB_VOLUME):/data busybox sh -c "rm -rf /data/*" || printf "${RED}Failure using Busybox${RESET}\n"
	@printf "${GREEN}Complete cleaning finished.${RESET}\n"

re: clean fclean all
