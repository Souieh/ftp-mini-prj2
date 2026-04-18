# ============================================================
#  Makefile  --  University Mini Project
# ============================================================

PYTHON  = python3
PIP     = pip3
OUTDIR  = output

.PHONY: all install run part1 part2 clean help

all: help

install:
	$(PIP) install pandas matplotlib

run:
	$(PYTHON) launcher.py

part1:
	$(PYTHON) phonebook.py

part2:
	$(PYTHON) patient_analysis.py

clean:
	rm -rf $(OUTDIR)
	@echo "[OK] output/ directory removed."

help:
	@echo ""
	@echo "  University Mini Project  --  Makefile"
	@echo "  ----------------------------------------"
	@echo "  make install   Install pandas + matplotlib"
	@echo "  make run       Start the launcher"
	@echo "  make part1     Run the Phonebook directly"
	@echo "  make part2     Run Patient Analysis directly"
	@echo "  make clean     Delete the output/ folder"
	@echo ""
