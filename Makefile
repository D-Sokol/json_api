SHELL := /bin/bash

release: upgrade-db install-reqs run-tests
	# upgrade
	# new_requirements

run:
	source venv/bin/activate;\
	flask run

install-reqs: requirements.txt
	source venv/bin/activate;\
	pip install -r requirements.txt

update-reqs:
	source venv/bin/activate;\
	pip freeze | grep -v 'pkg-resources==0.0.0' > requirements.txt

upgrade-db: adverts/models.py
	source venv/bin/activate;\
	flask db migrate;\
	flask db upgrade

run-tests:
	source venv/bin/activate;\
	python3 test.py
