VENV_NAME?=.venv
PYTHON_VERSION?=3.11
SRC=src

venv-create:
	python$(PYTHON_VERSION) -m venv $(VENV_NAME)
	pip install poetry
	poetry install

venv-activate:
	. $(VENV_NAME)/bin/activate

run:
	@python${PYTHON_VERSION} ${SRC}

venv-clean:
	rm -rf $(VENV_NAME)

source:
	source $(PWD)/.env.sh &&

clean:
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	rm -rf build/ dist/ *.egg-info/

lint:
	poetry run black .

ruff:
	poetry run ruff $(SRC)

pyright:
	poetry run pyright $(SRC)

test:
	source $(PWD)/.env.sh && \
	poetry run pytest


postman_tests:
	newman run ./postman/postman.json -e ./postman/fitko_local_dev.postman_environment.json