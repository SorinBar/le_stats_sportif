IS_VENV_ACTIVE=false
ifdef VIRTUAL_ENV
	IS_VENV_ACTIVE=true
endif

enforce_venv:
ifeq ($(IS_VENV_ACTIVE), false)
	$(error "You must activate your virtual environment. Exiting...")
endif

create_venv:
	python -m venv venv

install: enforce_venv requirements.txt
	python -m pip install -r requirements.txt

run_server: enforce_venv
	flask run
	rm -r results

run_tests: enforce_venv
	python checker/checker.py

run_unittests: enforce_venv
	python unittests/test_webserver.py

zip:
	rm -r asc1.zip
	rm -r /home/sorin/Downloads/t/*
	git log > git-log
	zip -r asc1 api_server.py git-log README.md app/ unittests/ -x 'app/__pycache__/*'
	rm git-log
	unzip asc1.zip -d /home/sorin/Downloads/t
	cp nutrition_activity_obesity_usa_subset.csv /home/sorin/Downloads/t/nutrition_activity_obesity_usa_subset.csv