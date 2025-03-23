FROM ubuntu:24.04

# Set non-interactive mode
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and required tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Setup virtual environment and activate it
RUN python3 -m venv env
ENV PATH="/app/env/bin:$PATH"

# Install Python dependencies into the virtual environment
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files into container
COPY . .

# Expose port 5000
EXPOSE 5000

# Run the Flask application within the virtual environment
CMD ["python", "app.py"]

