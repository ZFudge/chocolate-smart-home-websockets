.PHONY: build
build:
	@docker build . -t csm-websockets

.PHONY: clean
clean:
	@docker compose -f docker-compose-dev.yml down

.PHONY: dev
dev: clean
	@docker compose -f docker-compose-dev.yml up --remove-orphans

.PHONY: shell
shell:
	@docker compose -f docker-compose-dev.yml exec -it csm-websockets-dev sh

.PHONY: black
black:
	@docker compose -f docker-compose-dev.yml exec csm-websockets-dev sh -c "black /csm-websockets/"

.PHONY: ruff
ruff:
	@docker compose -f docker-compose-dev.yml exec csm-websockets-dev sh -c "ruff check /csm-websockets/"

.PHONY: ruff-fix
ruff-fix:
	@docker compose -f docker-compose-dev.yml exec csm-websockets-dev sh -c "ruff check --fix /csm-websockets/"

.PHONY: coverage
coverage:
	@docker compose -f docker-compose-dev.yml exec csm-websockets-dev sh -c "pytest --cov=src --cov-report=term-missing tests/"

.PHONY: test
test:
	@docker compose -f docker-compose-dev.yml exec csm-websockets-dev sh -c "pytest tests/"
