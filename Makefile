.PHONY: up
up:
	docker compose up -d --build --force-recreate 

.PHONY: down
down:
	docker compose down

SUBDIRS = go py

$(SUBDIRS):
	$(MAKE) -C $@

.PHONY: dev
dev:
	for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir dev; \
	done
