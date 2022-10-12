build:
	docker build -f Dockerfile -t inference-test:latest .

run_dev: build
	docker run -it inference-test:latest /bin/bash

test:
	pytest ./test/

test_data:
	pytest -rc ./test/test_data.py

test_code:
	pytest -rc ./test/test_code.py

test_model:
	pytest -ss ./test/test_model.py
