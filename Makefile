.PHONY: build
build:
	@docker build . -t csm-ws-service

.PHONY: clean
clean:
	@docker compose -f docker-compose-dev.yml down

.PHONY: dev
dev: clean
	@docker compose -f docker-compose-dev.yml up --remove-orphans

.PHONY: shell
shell:
	@docker compose -f docker-compose-dev.yml exec -it csm-ws-service-dev sh

.PHONY: black
black:
	@docker compose -f docker-compose-dev.yml exec csm-ws-service-dev sh -c "black /ws-service/"

.PHONY: ruff
ruff:
	@docker compose -f docker-compose-dev.yml exec csm-ws-service-dev sh -c "ruff check /ws-service/"

.PHONY: ruff-fix
ruff-fix:
	@docker compose -f docker-compose-dev.yml exec csm-ws-service-dev sh -c "ruff check --fix /ws-service/"

.PHONY: coverage
coverage:
	@docker compose -f docker-compose-dev.yml exec csm-ws-service-dev sh -c "pytest --cov=src --cov-report=term-missing tests/"

.PHONY: test
test:
	@docker compose -f docker-compose-dev.yml exec csm-ws-service-dev sh -c "pytest tests/"
