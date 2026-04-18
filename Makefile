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

.PHONY: shell
shell:
	@docker exec -it csm-ws-service-dev sh
