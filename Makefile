pip:
	python -m pip install pip -U
	python -m pip install -r requirements.txt -U

pip-dev:
	python -m pip install pip -U
	python -m pip install -r requirements.txt -U
	python -m pip install -r requirements-dev.txt -U

lint:
	mypy --install-types --non-interactive .

test:
	pytest

prepare:
	make lint
	make test

serve:
	python main.py

docker:
	docker build -t local/hlb:0.1.0 .
	docker volume create hlb-tmp
	docker run --rm -it -v hlb-tmp:/usr/src/app/tmp --env HLB_DEBUG=0 --name=hlb010 local/hlb:0.1.0
