FROM python:slim

WORKDIR /app

# Install system dependencies for uamqp
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files into the container
COPY . .

CMD [ "python", "-u", "app.py" ]
