# University Mini Project -- Python

A two-part Python project with a shared ASCII-based terminal UI.
Compatible with: Windows CMD, PowerShell, Linux shell, macOS Terminal.

## File Structure

```
mini_project/
+-- launcher.py            Entry point  -- run this first
+-- phonebook.py           Part 1: Phonebook application
+-- patient_analysis.py    Part 2: Patient data analysis
+-- ui.py                  Shared ASCII UI toolkit
+-- Makefile               Shortcuts for common tasks
+-- README.md              This file

output/                    Created automatically at runtime
+-- patients.csv           ...and populated with results,
+-- visits.csv             CSVs, and chart images.
+-- results.csv
+-- high_average_patients.csv
+-- frequent_visitors.csv
+-- chart_avg_per_patient.png
+-- chart_avg_per_question.png
+-- chart_gender_pie.png
```

## Requirements

- Python 3.8+
- pandas, matplotlib  (Part 2 only)

```
pip install pandas matplotlib
```

Or use the Makefile:

```
make install
```

## How to Run

### Launcher (recommended)

```
python launcher.py        # Linux / macOS
python launcher.py        # Windows CMD / PowerShell
```

Select 1 for the Phonebook or 2 for Patient Data Analysis.

### Run parts directly

```
python phonebook.py
python patient_analysis.py
```

### Makefile shortcuts (Linux / macOS)

```
make run      -- Start the launcher
make part1    -- Run the phonebook directly
make part2    -- Run the patient analysis directly
make clean    -- Delete the output/ folder
```

## Part 1 -- Phonebook Application

Interactive menu-driven phonebook using Python dictionaries.
No external libraries required.

Menu options:
  a) Print all contacts          h) List all phone numbers
  b) Add a new contact           i) Count total contacts
  c) Update a contact's number   j) Search by area code
  d) Delete a contact            k) Create backup
  e) Search for a contact        l) Clear phonebook
  f) Check if a contact exists   m) Restore from backup
  g) List names alphabetically   n) Search by first letter

## Part 2 -- Patient Data Analysis

Automated 10-step pipeline with progress indicators.

Steps:
  1  Build patients.csv and load into DataFrame
  2  Compute average scores per patient (Q1-Q10)
  3  Gender distribution count
  4  Save results.csv
  5  Generate 3 charts (bar, line, pie) as PNG files
  6  Create visits.csv and merge with patient data
  7  Assign Status column (Critical / Stable / Good)
  8  Boost all scores +1 (capped at 5)
  9  Remove patients with LastVisitDays > 50
 10  Export filtered subsets to separate CSV files

## UI Module (ui.py)

Shared toolkit used by all scripts:
  - ASCII boxes and tables (pure +, -, | characters)
  - Status lines: [OK] [!!] [--] [??]
  - Spinner and progress bar animations
  - Cross-platform screen clear and prompts
  - No external libraries required
