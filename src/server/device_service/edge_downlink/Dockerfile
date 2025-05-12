FROM python:alpine

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files into the container
COPY . .

CMD [ "python", "-u", "app.py" ]
