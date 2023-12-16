# Dockerfile in app/
FROM python:3.8.18-slim

WORKDIR /app

# RUN apt-get update && apt-get install -y postgresql-server-dev-all
RUN apt-get update && apt-get install -y \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p /app/log

# Install Python dependencies
COPY requirements.txt .

# Create and activate a new virtual environment
RUN python -m venv .venv
ENV PATH="/app/.venv/bin:$PATH"

# Install Python dependencies
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Copy geckodriver (replace 'linux_geckodriver' with the actual filename)
ENV MOZ_HEADLESS=1
ENV PATH="/app:${PATH}"
COPY .venv/Scripts/geckodriver_linux /app/.venv/bin/geckodriver

# Touch and chmod the log file
RUN touch /app/log/app.log && chmod a+rw /app/log/app.log

# Run the application
# CMD ["python", "-m", "main"]
CMD [".venv/bin/python", "-m", "main"]
