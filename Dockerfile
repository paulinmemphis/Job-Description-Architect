FROM python:3.11-slim

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
