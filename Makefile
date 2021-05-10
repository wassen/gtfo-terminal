.PHONY: develop-run release-run pipenv mypy test

default: pipenv token

pipenv: Pipfile Pipfile.lock
	pipenv install

token:
	@read -p "Enter Discord App Token: " token && echo $$token > token

develop-run:
	pipenv run ./entry_point.py develop

release-run:
	pipenv run ./entry_point.py release

mypy:
	# -pipenv run mypy ./entry_point.py --strict
	-pipenv run mypy ./test/test_gtfo_terminal.py --strict

test:
	pipenv run green test/test_gtfo_terminal.py

format:
	pipenv run black .
	pipenv run isort .

