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

all: create-dir
	@bash -c 'source .env && exec docker compose up --build -d'

fclean: stop clean
	@echo "${YELLOW}Withdrawal of Docker images...${RESET}"
	@docker rmi -f my_app postgres:17 dpage/pgadmin4 busybox || true
	@echo "${GREEN}Images deleted.${RESET}"

stop:
	@docker compose stop

down:
	@docker compose down -v

start: create-dir
	@bash -c 'source .env && docker compose up -d'
	@echo "${BLUE}Waiting for my_app...${RESET}"
	@until docker ps | grep -q "my_app"; do sleep 1; done
	@docker exec -it my_app bash

resume:
	@echo "${BLUE}Restarting all stopped containers...${RESET}"
	@docker ps -a -f "status=exited" --format '{{.Names}}' | xargs -r docker start
	@echo "${GREEN}All previously stopped containers have been restarted.${RESET}"

re: clean fclean all

restart:
	@$(MAKE) stop
	@sleep 1
	@$(MAKE) start

create-dir:
	@if [ ! -d "$(DB_VOLUME)" ] || [ ! -d "$(APP_VOLUME)" ]; then \
		mkdir -p $(DB_VOLUME) $(APP_VOLUME); \
		echo "${BLUE}Bind mounts created (only if necessary):${RESET}"; \
		echo "  - $(DB_VOLUME)"; \
		echo "  - $(APP_VOLUME)"; \
	fi

env:
	@echo "${BLUE}Updating .env variables based on environment...${RESET}"
	@( grep -q '^APP_VOLUME=' .env && sed -i 's|^APP_VOLUME=.*|APP_VOLUME=$(APP_VOLUME)|' .env || echo "APP_VOLUME=$(APP_VOLUME)" >> .env )
	@( grep -q '^DB_VOLUME=' .env && sed -i 's|^DB_VOLUME=.*|DB_VOLUME=$(DB_VOLUME)|' .env || echo "DB_VOLUME=$(DB_VOLUME)" >> .env )
	@echo "${GREEN}.env file updated.${RESET}";

clean:
	@echo "${YELLOW}Cleaning PostgreSQL DB...${RESET}"
	@if docker container inspect my_postgres > /dev/null 2>&1; then \
		if docker ps -q -f name=my_postgres | grep -q .; then \
			echo "${BLUE}Container my_postgres is running. Withdrawal by docker exec.${RESET}"; \
			docker exec my_postgres bash -c "rm -rf /var/lib/postgresql/data/*" || echo "${RED}Failure of the withdrawal by container${RESET}"; \
		else \
			echo "${CYAN}Container my_postgres exists but is not running. Temporary start.${RESET}"; \
			docker start my_postgres > /dev/null; \
			sleep 3; \
			docker exec my_postgres bash -c "rm -rf /var/lib/postgresql/data/*" || echo "${RED}Failure after starting.${RESET}"; \
			echo "${BLUE}Stopping my_postgres container.${RESET}"; \
			docker stop my_postgres > /dev/null; \
		fi \
	else \
		echo "${RED}Container my_postgres does not exist. Skipping container-based cleaning.${RESET}"; \
	fi
	@echo "${MAGENTA}Final check with Busybox to clean bind mounted volume...${RESET}"
	@docker run --rm -v $(DB_VOLUME):/data busybox sh -c "rm -rf /data/*" || echo "${RED}Failure using Busybox${RESET}"
	@echo "${GREEN}Complete cleaning finished.${RESET}"

fclean: stop clean
	@echo "${YELLOW}Removing containers, images, and volumes from docker-compose...${RESET}"
	@docker compose down --volumes --rmi all || echo "${RED}Could not fully clean with docker compose down${RESET}"
	@docker rmi -f busybox || echo "${CYAN}busybox image not found or already removed.${RESET}"
	@echo "${GREEN}All docker-compose resources have been removed.${RESET}"

re: clean fclean all
