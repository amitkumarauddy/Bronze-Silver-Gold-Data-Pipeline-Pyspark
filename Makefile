.PHONY: help build run clean-data clean-docker nuke

# The default command when someone just types 'make'
.DEFAULT_GOAL := help

help: ## Show this command hub
	@echo "🚕 NYC Taxi Medallion Pipeline - Control Panel"
	@echo "=============================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## 🏗️  Build the PySpark Docker environment
	docker-compose build

run: ## 🚀 Execute the end-to-end data pipeline
	docker-compose up

clean-data: ## 🧹 Delete Bronze, Silver, and Gold data (Keeps Raw safe!)
	rm -rf data/bronze/* data/silver/* data/gold/*
	@echo "Processed data layers cleared."

clean-docker: ## 🐳 Remove the Docker containers and images
	docker-compose down --rmi all

nuke: clean-data clean-docker ## ☢️  Complete factory reset (Clears data and Docker)
	@echo "Project reset to factory settings."
