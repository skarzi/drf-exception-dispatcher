SHELL := /usr/bin/env bash
.SHELLFLAGS := -euo pipefail -c
.DEFAULT_GOAL := help

_MAKEFILE_TARGETS := $(sort $(shell awk '/^\.PHONY:/{for (i = 2; i <= NF; i++) print $$i}' $(firstword $(MAKEFILE_LIST))))
EXTRA_ARGS = $(filter-out $(_MAKEFILE_TARGETS),$(MAKECMDGOALS)) $(filter -%,$(-*-command-variables-*-))
_PYTHON_PATHS = $(if $(strip $(EXTRA_ARGS)),$(EXTRA_ARGS),exception_dispatcher tests tools)
_MARKDOWN_ARGS = $(if $(strip $(EXTRA_ARGS)),--no-globs $(EXTRA_ARGS))
_TOML_PATHS = $(if $(strip $(EXTRA_ARGS)),$(EXTRA_ARGS),.)
_YAML_PATHS = $(if $(strip $(EXTRA_ARGS)),$(EXTRA_ARGS),.yamlfmt $(shell git ls-files --cached --others --exclude-standard '*.yml' '*.yaml'))
_COMMIT_MESSAGE_ARGS = $(if $(strip $(EXTRA_ARGS)),$(EXTRA_ARGS),.git/COMMIT_EDITMSG)

REPOSITORY_ROOT := $(patsubst %/,%,$(dir $(abspath $(firstword $(MAKEFILE_LIST)))))
_CLEAN_PATHS := \
	$(REPOSITORY_ROOT)/.coverage \
	$(REPOSITORY_ROOT)/.mypy_cache \
	$(REPOSITORY_ROOT)/.pytest_cache \
	$(REPOSITORY_ROOT)/.ruff_cache \
	$(REPOSITORY_ROOT)/.tests_reports \
	$(REPOSITORY_ROOT)/build \
	$(REPOSITORY_ROOT)/dist

# GNU Make 3.81 has no target-specific .NOTPARALLEL behavior.
.NOTPARALLEL:

#: Trust and install the exact mise tool configuration.
.PHONY: install-mise
install-mise:
	mise trust --yes "$(REPOSITORY_ROOT)/mise.toml"
	mise install

#: Install locked Python runtime and development dependency groups.
.PHONY: install-python
install-python:
	uv sync --locked --all-groups

#: Install locked Node development dependencies.
.PHONY: install-node
install-node:
	npm ci

#: Install pre-commit and commit-msg hooks.
.PHONY: install-pre-commit
install-pre-commit:
	uv run --no-sync pre-commit install --install-hooks \
		--hook-type pre-commit --hook-type commit-msg

#: Install all development tools, dependencies, and Git hooks.
.PHONY: install-dev
install-dev: install-mise install-python install-node install-pre-commit

#: Run tests; arguments after -- are forwarded to pytest and disable coverage.
.PHONY: test
test:
	uv run --no-sync pytest $(if $(strip $(EXTRA_ARGS)),--no-cov) $(EXTRA_ARGS)

#: Check Python syntax, formatting, style, and types.
.PHONY: lint-python-code
lint-python-code:
	uv run --no-sync ruff check $(_PYTHON_PATHS)
	uv run --no-sync ruff format --check $(_PYTHON_PATHS)
	uv run --no-sync flake8 $(_PYTHON_PATHS)
	uv run --no-sync mypy $(_PYTHON_PATHS)

#: Check the package dependency-layer contract without cached results.
.PHONY: lint-python-architecture
lint-python-architecture:
	uv run --no-sync lint-imports --no-cache

#: Check dead and duplicate pytest fixtures without coverage.
.PHONY: lint-python-tests
lint-python-tests:
	uv run --no-sync pytest --no-cov -o addopts= \
		--strict-config --strict-markers --dead-fixtures
	uv run --no-sync pytest --no-cov -o addopts= \
		--strict-config --strict-markers --dup-fixtures

#: Run all Python checks.
.PHONY: lint-python
lint-python: lint-python-code lint-python-architecture lint-python-tests

#: Apply safe Ruff fixes and formatting to Python files.
.PHONY: fix-python
fix-python:
	uv run --no-sync ruff check --fix $(_PYTHON_PATHS)
	uv run --no-sync ruff format $(_PYTHON_PATHS)

#: Format and check Python files.
.PHONY: lint-fix-python
lint-fix-python: fix-python lint-python

#: Check TOML formatting and validity.
.PHONY: lint-toml
lint-toml:
	uv run --no-sync tombi format --check $(_TOML_PATHS)
	uv run --no-sync tombi lint $(_TOML_PATHS)

#: Format TOML files.
.PHONY: fix-toml
fix-toml:
	uv run --no-sync tombi format $(_TOML_PATHS)

#: Format and check TOML files.
.PHONY: lint-fix-toml
lint-fix-toml: fix-toml lint-toml

#: Check Markdown files.
.PHONY: lint-markdown
lint-markdown:
	npm run lint:markdown -- $(_MARKDOWN_ARGS)

#: Format Markdown files.
.PHONY: fix-markdown
fix-markdown:
	npm run fix:markdown -- $(_MARKDOWN_ARGS)

#: Format and check Markdown files.
.PHONY: lint-fix-markdown
lint-fix-markdown: fix-markdown lint-markdown

#: Check YAML formatting and validity.
.PHONY: lint-yaml
lint-yaml:
	yamlfmt -lint $(_YAML_PATHS)
	uv run --no-sync yamllint $(_YAML_PATHS)

#: Format YAML files.
.PHONY: fix-yaml
fix-yaml:
	yamlfmt $(_YAML_PATHS)

#: Format and check YAML files.
.PHONY: lint-fix-yaml
lint-fix-yaml: fix-yaml lint-yaml

#: Validate a commit message file.
.PHONY: lint-commit-message
lint-commit-message:
	npm run lint:commit-message -- $(_COMMIT_MESSAGE_ARGS)

#: Validate the pre-commit configuration.
.PHONY: lint-pre-commit
lint-pre-commit:
	uv run --no-sync pre-commit validate-config .pre-commit-config.yaml

#: Verify that pyproject.toml and uv.lock agree.
.PHONY: lint-lock
lint-lock:
	uv lock --check

#: Validate the Makefile.
.PHONY: lint-makefile
lint-makefile:
	checkmake $(if $(strip $(EXTRA_ARGS)),$(EXTRA_ARGS),Makefile)

#: Validate GitHub Actions workflows and embedded shell.
.PHONY: lint-github-actions-workflow
lint-github-actions-workflow:
	actionlint $(EXTRA_ARGS)

#: Check spelling.
.PHONY: lint-spelling
lint-spelling:
	uv run --no-sync codespell $(if $(strip $(EXTRA_ARGS)),$(EXTRA_ARGS),.)

#: Run all read-only checks.
.PHONY: lint
lint: lint-python lint-toml lint-markdown lint-yaml lint-pre-commit lint-lock \
	lint-makefile lint-github-actions-workflow lint-spelling

#: Run all formatters.
.PHONY: fix
fix: fix-python fix-toml fix-markdown fix-yaml

#: Apply all fixes, then run all checks.
.PHONY: lint-fix
lint-fix: fix lint

#: Show and validate the active compatibility-test environment.
.PHONY: check-environment
check-environment:
	.venv/bin/python --version
	uv pip show --python .venv/bin/python Django djangorestframework
	uv pip check --python .venv/bin/python

#: Validate a release tag and write GitHub Actions outputs.
.PHONY: validate-release
validate-release:
	uv run --no-sync python tools/validate_release.py

#: Audit the complete locked dependency graph.
.PHONY: audit
audit:
	@requirements="$$(mktemp)"; trap 'rm -f "$$requirements"' EXIT; \
	uv export --locked --all-groups --no-emit-project \
		--no-hashes --output-file "$$requirements"; \
	uv run --no-sync pip-audit --requirement "$$requirements" $(EXTRA_ARGS)

#: Build the wheel and source distribution.
.PHONY: build
build:
	uv build --clear $(EXTRA_ARGS)

define CHECK_PACKAGE
tmp="$$(mktemp -d)"; trap 'rm -rf "$$tmp"' EXIT; \
wheel="$$(find dist -maxdepth 1 -name '*.whl' -print -quit)"; \
sdist="$$(find dist -maxdepth 1 -name '*.tar.gz' -print -quit)"; \
test -n "$$wheel"; test -n "$$sdist"; \
unzip -Z1 "$$wheel" > "$$tmp/wheel-files"; \
tar -tzf "$$sdist" > "$$tmp/sdist-files"; \
grep -q '^exception_dispatcher/py.typed$$' "$$tmp/wheel-files"; \
grep -q '/exception_dispatcher/py.typed$$' "$$tmp/sdist-files"; \
! grep -Eq '(^|/)(\.agents|\.venv|node_modules|\.tests_reports)/' \
	"$$tmp/wheel-files" "$$tmp/sdist-files"; \
project_version="$$(uv version --short --frozen)"; \
uv venv --python .venv/bin/python "$$tmp/venv"; \
uv pip install --python "$$tmp/venv/bin/python" "$$wheel"; \
(cd "$$tmp" && PROJECT_VERSION="$$project_version" "$$tmp/venv/bin/python" -c \
	"import importlib.metadata as m, os; from django.conf import settings; settings.configure(SECRET_KEY='package-check'); from django.core.exceptions import PermissionDenied; from django.http import Http404; from rest_framework.exceptions import APIException; from exception_dispatcher.dispatchers import exception_dispatcher; name = 'drf-exception-dispatcher'; requirements = [item.lower() for item in m.requires(name) or []]; assert m.version(name) == os.environ['PROJECT_VERSION']; assert any(item.startswith('django') for item in requirements); assert any(item.startswith('djangorestframework') for item in requirements); assert not any(item.startswith(('pytest', 'ruff', 'mypy')) for item in requirements); assert all(kind in exception_dispatcher.registry for kind in (Http404, PermissionDenied, APIException))"); \
mkdir "$$tmp/from-sdist"; \
tar -xzf "$$sdist" -C "$$tmp/from-sdist"; \
package_dir="$$(find "$$tmp/from-sdist" -mindepth 1 -maxdepth 1 -type d -print -quit)"; \
uv build --directory "$$package_dir" --wheel \
	--out-dir "$$tmp/from-sdist-wheel"; \
uv run --no-sync twine check "$$tmp/from-sdist-wheel"/*.whl
endef

#: Build and validate package metadata, contents, and installation.
.PHONY: check-package
check-package: build
	uv run --no-sync twine check dist/*
	@$(CHECK_PACKAGE)

#: Run lint, tests, and package validation.
.PHONY: check
check: lint test check-package

#: Update compatible Python and Node dependencies.
.PHONY: update-deps
update-deps:
	uv lock --upgrade
	npm update

#: Update remote pre-commit hook revisions.
.PHONY: update-hooks
update-hooks:
	uv run --no-sync pre-commit autoupdate

#: Report and update mise-managed tool pins.
.PHONY: update-tools
update-tools:
	mise outdated
	mise upgrade --bump

#: Remove generated reports, caches, and distributions.
.PHONY: clean
clean:
	rm -rf -- $(_CLEAN_PATHS)

#: Clean, install, fix, test, and build.
.PHONY: all
all: clean install-dev lint-fix test build

#: Show available targets.
.PHONY: help
help:
	@awk '/^#: / { sub(/^#: /, ""); description = description ? description " " $$0 : $$0; next } /^[a-zA-Z][a-zA-Z0-9_-]*:/ && description { sub(/:.*/, ""); printf "\033[36m%-28s\033[0m %s\n", $$0, description; description = "" }' $(MAKEFILE_LIST) | sort
	@printf '\nPass paths and flags after -- to leaf targets.\n'

# Forwarded arguments are Make goals but never recipes to execute.
%:
	@:
