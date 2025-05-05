FROM python:alpine

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container (if needed)
EXPOSE 5000

CMD ["python", "-u", "app.py"]
