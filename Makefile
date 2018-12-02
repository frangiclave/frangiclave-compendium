.PHONY: run

run:
	#uwsgi --http-socket 127.0.0.1:5777 --master --processes 4 --enable-threads --virtualenv=./venv/ --mount /=frangiclave.main:init --manage-script-name
	uwsgi -s /tmp/frangiclave.sock --master --processes 4 --enable-threads --virtualenv=./venv/ --manage-script-name --mount /frangiclave=frangiclave.main:app --chmod-socket=777
