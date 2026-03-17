FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Ensure we don't write generic bytecode and we see output in real time
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a non-root user for security
RUN adduser --disabled-password --gecos "" appuser

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /app/src/
COPY run.py /app/

# Set ownership to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose port
EXPOSE 8000

# Set entrypoint
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
