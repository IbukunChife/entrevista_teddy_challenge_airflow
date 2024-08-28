.PHONY: all test lint format run deploy setup_airflow_and_db migrate clean

# Default target
all: format lint test

setup_all: setup_airflow_and_db migrate

# Run Docker Compose to start the database
setup_airflow_and_db:
	@echo "Starting airflow and database with Docker Compose..."
	mkdir -p ./dags ./logs ./plugins
	docker-compose up -d
	pipenv run alembic upgrade head

# Perform migrations
migrate:
	@echo "Running migrations..."
	pipenv run alembic upgrade head

# Run linters
lint:
	@echo "Running linters..."
	pipenv run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	pipenv run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Run tests
test:
	@echo "Running tests..."
	pipenv run pytest

# Format code
format:
	@echo "Formatting code..."
	pipenv run black .

# Clean up
clean:
	@echo "Stopping and removing Docker containers..."
	docker-compose down
	docker system prune --volumes --force

