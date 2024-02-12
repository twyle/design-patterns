install:
	@pip install -r requirements-dev.txt

lint:
	@black state/
	@isort state/
	@flake8 state/

