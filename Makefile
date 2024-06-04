.PHONY: develop
develop:
	docker compose up -d --build --force-recreate 

.PHONY: clean
clean:
	docker compose down
