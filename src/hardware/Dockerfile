FROM python:alpine

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
    # && apt-get update \
    # && apt-get install -y \
    # python3-rpi.gpio \
    # && rm -rf /var/lib/apt/lists/*
    
# Copy all application files into the container
COPY . .

CMD ["python", "app.py"]
