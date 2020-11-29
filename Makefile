.PHONY: run pipenv

default: pipenv token

pipenv: Pipfile Pipfile.lock
	pipenv install

token:
	@read -p "Enter Discord App Token: " token && echo $$token > token

run:
	pipenv run ./gtfo_terminal.py

