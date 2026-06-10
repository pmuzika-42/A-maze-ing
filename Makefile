ARG = config.txt

PY3 = python3

NAME = a_maze_ing.py

OUTPUT_FILE = maze.txt

# Package name not defined yet
# to be completed
PACKAGE = mazegen-1.0.0-py3-none-any.whl

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

build:
	$(PY3) mazegen -m build

debug:
	$(PY3) -m $(DEBUG) $(NAME) $(ARG)

clean:
	rm -rf $(CACHE)

clean-output:
	rm -f $(OUTPUT_FILE)

lint:
	$(FLAKE) . ; $(MYPY) . $(MYPY_FLAGS)

lint-strict:
	$(FLAKE) . ; $(MYPY) . $(MYPY_STRICT)

.PHONY: install run debug clean clean-output lint lint-strict