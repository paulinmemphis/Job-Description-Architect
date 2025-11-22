import os

# Content for the missing/empty files
files_to_fix = {
    "docker-compose.yml": """services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - .:/app
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
""",
    "Dockerfile": """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed (none for this simple app)
# RUN apt-get update && apt-get install -y ...

# Copy requirements first to leverage cache
COPY pyproject.toml .

# Install dependencies using pip
RUN pip install streamlit pandas pydantic pytest

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
""",
    "pyproject.toml": """[project]
name = "job-description-architect"
version = "1.0.0"
description = "App to enhance and manage job descriptions"
requires-python = ">=3.11"
dependencies = [
    "streamlit>=1.32.0",
    "pandas>=2.2.0",
    "pydantic>=2.6.0",
    "pytest>=8.0.0"
]

[tool.uv]
# UV configuration if used

[tool.ruff]
line-length = 120
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
""",
    "Makefile": """.PHONY: run test lint docker-build docker-up clean

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
"""
}

def repair():
    print("Repairing project files in current directory...")
    for filename, content in files_to_fix.items():
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed/Created: {filename}")
    print("\nSuccess! You can now run 'docker compose up'")

if __name__ == "__main__":
    repair()