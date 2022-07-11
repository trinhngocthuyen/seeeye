install:
	python3 -m pip install virtualenv
	python3 -m virtualenv .venv
	. .venv/bin/activate && pip install -r requirements.txt

test: test.py test.integration.ios

test.py:
	. .venv/bin/activate && pytest

test.integration.ios:
	. .venv/bin/activate && sh scripts/integration_test_ios.sh

format:
	. .venv/bin/activate && \
		autoflake -r -i \
			--remove-all-unused-imports \
			--remove-unused-variables \
			--exclude __init__.py \
			src tests && \
		isort src tests && \
		black src tests
