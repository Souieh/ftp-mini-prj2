# ============================================================
#  Makefile  --  University Mini Project
# ============================================================

SYSTEM_PYTHON = python3
VENV          = .venv
PYTHON        = $(VENV)/bin/python
PIP           = $(VENV)/bin/pip
PYINSTALLER   = $(VENV)/bin/pyinstaller
OUTDIR        = output
APP_NAME      = mini_project

.PHONY: all venv install install-dev run build clean help

all: help

$(PYTHON):
	$(SYSTEM_PYTHON) -m venv $(VENV)

venv: $(PYTHON)
	$(PIP) install --upgrade pip

install: venv
	$(PIP) install -r requirements.txt

install-dev: install
	$(PIP) install -r requirements-dev.txt

run: install
	$(PYTHON) phonebook.py


build: install-dev
	$(PYINSTALLER) --clean phonebook.spec
	@echo "[OK] Executable available at dist/$(APP_NAME)"

clean:
	rm -rf $(OUTDIR) build dist
	@echo "[OK] output/, build/, and dist/ directories removed."

help:
	@echo ""
	@echo "  University Mini Project  --  Phonebook"
	@echo "  ----------------------------------------"
	@echo "  make venv        Create .venv and upgrade pip"
	@echo "  make install     Install runtime dependencies"
	@echo "  make install-dev Install runtime + build dependencies"
	@echo "  make run         Start the Phonebook"
	@echo "  make build       Build executable with PyInstaller"
	@echo "  make clean       Delete output/, build/, and dist/"
	@echo ""
