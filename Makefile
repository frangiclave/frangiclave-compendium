.PHONY: run

run:
	uwsgi --socket 127.0.0.1:5777 --wsgi-file frangiclave/main.py --callable init --processes 4 --enable-threads --virtualenv=./venv/ --plugin python3 --manage-script-name
