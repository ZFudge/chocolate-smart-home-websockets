.PHONY: build
build:
	@docker build . -t csm-ws-service

.PHONY: dev
dev:
	@docker run \
        --name csm-ws-service-dev \
        -p 8050:8050 \
		--rm \
        --volume .:/ws-service/ \
        --volume /tmp/logs/:/var/logs/ \
        --workdir /ws-service/ \
		csm-ws-service \
        sh -c \
            "uvicorn src.ws-app:app \
            --reload \
            --reload-dir src \
            --host 0.0.0.0 \
            --port 8050 \
            --log-level debug \
            --log-config logs.ini"

#@docker compose -f docker-compose-dev.yml up

.PHONY: shell
shell:
	@docker compose -f docker-compose-dev.yml exec csm-ws-service-dev sh

