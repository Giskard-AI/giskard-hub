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

setup: ## Install all dependencies (dev + docs)
	uv sync --group dev --group docs
.PHONY: setup

setup-dev: ## Install only development dependencies
	uv sync --group dev
.PHONY: setup-dev

setup-docs: ## Install only documentation dependencies
	uv sync --group docs
.PHONY: setup-docs

doc: setup ## Build the doc
	cp ./README.md ./script-docs/README.md
	cd ./script-docs && rm -rf _build && uv run sphinx-build -b html . _build/html -v
	rm -rf ./docs && mkdir -p ./docs && touch ./docs/.nojekyll && mv ./script-docs/_build/html/* ./docs
	echo docs.giskard.ai > ./docs/CNAME
.PHONY: setup

quick-doc: ## Build the doc & serve it locally
	cp ./README.md ./script-docs/README.md
	cd ./script-docs && rm -rf _build && uv run sphinx-build -b html . _build/html -v
	uv run python -m http.server --directory ./script-docs/_build/html/
.PHONY: quick-doc

live-docs: ## Serve the doc locally with auto-reload
	cd ./script-docs && uv run sphinx-autobuild . _build/html --port 8000 --host 127.0.0.1
.PHONY: live-docs


test: ## Launch unit tests
	uv run pytest -vvv ./tests
.PHONY: test
