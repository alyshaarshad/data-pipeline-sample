FROM python:3.9-slim

# Ensure console logs can be gathered from Python when running in a container.

ENV PYTHONUNBUFFERED=1

WORKDIR /src

# Install generic dependencies

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copies the current src directory into container
COPY . .


CMD ["python", "main.py"]