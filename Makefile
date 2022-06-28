install:
	python3 -m pip install virtualenv
	python3 -m virtualenv .venv
	. .venv/bin/activate && pip install -r requirements.txt

test:
	. .venv/bin/activate && pytest

test.integration.ios:
	. .venv/bin/activate && sh scripts/integration_test_ios.sh

format:
	. .venv/bin/activate && isort . && black .
