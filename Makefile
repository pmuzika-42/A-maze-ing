ARG = config.txt

PY3 = python3

NAME = a_maze_ing.py

OUTPUT_FILE = maze.txt

PACKAGE = mazegen-1.0.0-py3-none-any.whl

PIP = pip

FLAKE = flake8

EXCLUDE_DIR = --exclude=.venv,venv,env,build,amazing,*.egg-info

MYPY = mypy

MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

DEBUG = pdb

CACHE = .mypy_cache 

BUILD_DIRS = dist build *.egg-info

install:
	$(PY3) -m $(PIP) install $(PACKAGE)

uninstall:
	$(PY3) -m $(PIP) uninstall $(PACKAGE)

reinstall: distclean uninstall install

run:
	$(PY3) $(NAME) $(ARG)

build: distclean
	$(PIP) install build
	$(PY3) -m build --wheel --sdist

debug:
	$(PY3) -m $(DEBUG) $(NAME) $(ARG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf $(CACHE)

clean-output: clean
	rm -f $(OUTPUT_FILE)

distclean: clean-output
	rm -rf $(BUILD_DIRS)

clean-pack: distclean
	rm -rf $(PACKAGE)

lint:
	$(FLAKE) . $(EXCLUDE_DIR); $(MYPY) . $(MYPY_FLAGS) $(EXCLUDE_DIR)

lint-strict:
	$(FLAKE) . $(EXCLUDE_DIR); $(MYPY) . --strict $(EXCLUDE_DIR) --ignore-missing-imports

.PHONY: install install-dev uninstall reinstall run build debug clean clean-output clean-pack distclean lint lint-strict