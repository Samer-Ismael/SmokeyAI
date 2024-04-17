# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir Flask requests flask-cors

EXPOSE 5000
EXPOSE 11434

CMD ["python", "main.py"]
