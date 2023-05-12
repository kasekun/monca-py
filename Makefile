.PHONY: purge instantiate install setup recreate format

purge:
	command -v deactivate >/dev/null && deactivate || true
	pipenv --rm || true

instantiate:
	pipenv --python 3.10.10

install:
	pipenv install --dev

setup: instantiate install

recreate: purge instantiate install

format:
	pipenv run black .
	pipenv run isort .
