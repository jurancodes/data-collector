# Makefile for managing Docker containers

# Define the name of your Docker Compose file
DATABASE_FILE = infra/database.yml
NETWORK_FILE = infra/network.yml
NBA_PLAYER_LOADER_FILE = infra/nba-player-loader.yml
.PHONY: database-up database-down

database-up:
	docker-compose -f $(DATABASE_FILE) up -d

database-down:
	docker-compose -f $(DATABASE_FILE) down

# NBA PLAYER LOADER
.PHONY: build run stop

# Build the Docker image
nba-player-loader-build:
	docker build -t nba-player-loader:latest ./code/nba-player-loader

# Run the Docker container with the Python script
# nba-player-loader-run: docker run --rm -it --name nba-player-loader --network infra_data_network nba-player-loader:latest
nba-player-loader-run:
	docker-compose -f $(NBA_PLAYER_LOADER_FILE) up -d

# Stop and remove the Docker container
nba-player-loader-stop:
	docker stop nba-player-loader || true
	docker rm nba-player-loader

nba-player-loader-play: nba-player-loader-build nba-player-loader-stop nba-player-loader-run