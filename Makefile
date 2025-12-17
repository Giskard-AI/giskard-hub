# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

setup: install pre-commit-install ## Complete development setup

install: ## Install project dependencies
	uv sync --all-extras
.PHONY: setup

pre-commit-install: ## Setup pre-commit hooks
	uv tool run pre-commit install
.PHONY: pre-commit-install

dev: ## Start development server
	uv run sphinx-autobuild source build
.PHONY: dev

doc: clean html ## Build the doc
	rm -rf ./docs && mkdir -p ./docs && touch ./docs/.nojekyll && mv ./build/html/* ./docs
	echo docs.giskard.ai > ./docs/CNAME
.PHONY: setup
