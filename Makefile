.PHONY: run test lint docker-build docker-up clean

run:
	streamlit run app.py

test:
	pytest

lint:
	# Assuming ruff is installed in environment
	ruff check .

format:
	ruff check --fix .

docker-build:
	docker build -t job-architect .

docker-up:
	docker compose up

clean:
	rm -rf __pycache__ .pytest_cache core/__pycache__ tests/__pycache__
