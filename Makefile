run:
	uvicorn main:app --reload

init:
	pip-compile requirements.in && pip-compile requirements-dev.in && pip-sync requirements-dev.txt

before-init:
	pip install pip-tools