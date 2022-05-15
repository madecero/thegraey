# Purpose: Provide simple "make" targets for developers

# Default goal runs the "help" target
.DEFAULT_GOAL := help

.PHONY: download fetch-upstream

help: ## Show Makefile targets
	@printf "\033[36mUsage: make <target>\n" $$1, $$2
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\t\033[36m%-20s\033[0m %s\n", $$1, $$2}'

download: ## Download rawTweets data file
	@echo "Enter the following in your terminal: "
	@echo "./scripts/dl-raw-tweets.sh [rawTweets.txt file URL] rawTweets.txt"

fetch-upstream: ## Fetch any changes made to original repo
	@./scripts/pull-from-main-project.sh

