default: help;

# Usable commands
help: ## Display commands help
	@grep -E '^[a-zA-Z][a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY:

notebook: ## Start a jupyter notebook server
	jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --notebook-dir . --NotebookApp.token=''
.PHONY: notebook

format: ## Format all files inside backend with black & isort
	uv tool run black .
	uv tool run isort .
.PHONY: format

check_linting: ## Verify code with lint tools, like pylint
	uv run pylint ./src/giskard_hub
.PHONY: check_linting

check_format: ## Verify code formatting
	uv tool run black --check .
	uv tool run isort -c .
.PHONY: check_format

setup: ## Install all dependencies (dev)
	uv sync --group dev
.PHONY: setup

setup-dev: ## Install only development dependencies
	uv sync --group dev
.PHONY: setup-dev

test: ## Launch unit tests
	uv run pytest -vvv ./tests
.PHONY: test
