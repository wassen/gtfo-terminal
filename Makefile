.PHONY: develop-run release-run pipenv mypy

default: pipenv token

pipenv: Pipfile Pipfile.lock
	pipenv install

token:
	@read -p "Enter Discord App Token: " token && echo $$token > token

develop-run:
	pipenv run ./src/entry_point.py develop

release-run:
	pipenv run ./src/entry_point.py release

mypy:
	pipenv run mypy ./src/gtfo_terminal.py
