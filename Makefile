VENV_BIN=.venv/bin

venv:
	python -m venv .venv

install-deps:
	${VENV_BIN}/pip install -r requirements.txt

dev:
	${VENV_BIN}/fastapi dev shorturl/main.py

start:
	${VENV_BIN}/fastapi run shorturl/main.py

test:
	${VENV_BIN}/pytest

init_db:
	${VENV_BIN}/python -m shorturl.init_db

setup:
	$(MAKE) venv
	$(MAKE) install-deps
	$(MAKE) init_db

.PHONY: clean
clean:
	rm -rf .venv
	rm -f test.db
	rm -f shorturl.db
