REQ_PY  := python3.6
SRC     := fmap

ENV_DIR := env
DEPS    := requirements.txt
ENV_BIN := $(ENV_DIR)/bin
ENV     := $(ENV_BIN)/activate
PIP     := $(ENV_BIN)/pip
PY      := $(ENV_BIN)/python


all: dev

.PHONY: dev

dev: init
	make watch TASK=validate

init: $(ENV)

$(ENV): $(DEP)
	virtualenv -p $$(which $(REQ_PY)) $(ENV_DIR) --no-site-packages
	$(PIP) install -r $(DEPS)
	touch $(ENV)


.PHONY: lint typecheck test validate watch

lint:
	@banner $@
	@$(PY) -m flake8

typecheck:
	@banner $@
	@$(PY) -m mypy $(SRC)

test:
	@banner $@
	@$(PY) -m pytest

validate:
	make lint && \
	make typecheck && \
	make test

watch:
	while true; do \
		make $(TASK); \
		inotifywait -qre close_write .; \
	done


.PHONY: clean

clean:
	rm -rf .mypy_cache .cache build __pycache__ $(ENV_DIR)
