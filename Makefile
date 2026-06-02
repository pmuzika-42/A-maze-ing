ARG = config.txt

PY3 = python3

PY = ./$(ENV_NAME)/bin/$(PY3)

NAME = a_maze_ing.py

OUTPUT_FILE = maze.txt

# Package name not defined yet
# to be completed
PACKAGE = ...

ENV_NAME = The_A(mazing)_Team

VENV = venv

PIP = pip install

FLAKE = flake8

MYPY = mypy

MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

MYPY_STRICT = --strict

DEBUG = pdb

CACHE = __pycache__ .mypy_cache 

run:
	$(PY3) $(NAME) $(ARG)

install:
	$(PIP) $(PACKAGE)

env:
	$(PY3) -m $(VENV) $(ENV_NAME)

debug:
	$(PY) -m $(DEBUG) $(NAME) $(ARG)

clean:
	rm -rf $(CACHE)
	rm -rf $(ENV_NAME)

clean-output:
	rm -f $(OUTPUT_FILE)

lint:
	$(FLAKE) . ; $(MYPY) . $(MYPY_FLAGS)

lint-strict:
	$(FLAKE) . ; $(MYPY) . $(MYPY_STRICT)

.PHONY: install run debug clean lint lint-strict