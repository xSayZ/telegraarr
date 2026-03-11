FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY telegraarr/ ./telegraarr/

# Create config directory for database
RUN mkdir -p /config

# Non-root user for security
RUN useradd -r -s /bin/false telegraarr
RUN chown -R telegraarr:telegraarr /app /config
USER telegraarr

CMD ["python", "-m", "telegraarr.bot"]