install:
	python3 -m pip install --upgrade pip &&\
	python3 -m pip install -r requirements.txt

test:
	python -m pytest -vv veeam-sync-test.py

lint:
	pylint --disable=R,C veeam-sync-test.py veeam-sync.py

all: install lint test