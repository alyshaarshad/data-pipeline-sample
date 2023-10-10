# Environment file
include .env
export

# Docker Compose
COMPOSE = docker-compose -f docker-compose.yml

# Docker
DOCKER = docker

# Build the Docker image
build:
	$(DOCKER) build -t my-app .

# Start the application with Docker Compose
start:
	$(COMPOSE) up -d

# Stop the application with Docker Compose
stop:
	$(COMPOSE) down

# Clean up Docker images and containers
clean:
	$(DOCKER) system prune -a --volumes

# Run the main ETL script
run:
	.\message-generators\windows.exe