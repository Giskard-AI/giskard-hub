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

setup: ## Install dependencies
	uv sync --dev --all-extras
.PHONY: setup

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

test: ## Launch unit tests
	uv run pytest -vvv ./tests
.PHONY: test
