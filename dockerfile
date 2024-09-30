FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies, including PostgreSQL client and build tools
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . /app

# Set PYTHONPATH to ensure the app module can be found
ENV PYTHONPATH=/app

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

