# ============================================================
#  launcher.py  --  Main entry point
#  University Mini Project
# ============================================================

import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import ui

PART1 = os.path.join(BASE_DIR, "phonebook.py")
PART2 = os.path.join(BASE_DIR, "patient_analysis.py")

LOGO = r"""
  ____  _  _   ___   ____  ____  ____     __    ____  ____
 ( ___)(  )( ) (  ,) (  _ \( ___)(  _ \   /__\  (  _ \(  _ \
  )__)  )(  )(  ) \   ) _ < )__)  )   /  /(__)\  )___/ )___/
 (__)  (__)(__)(___)  (____/(____)(_)\_) (__)(__)(__) (__)
"""

VERSION  = "v1.0"
SUBTITLE = "Python Mini Project  --  Launcher"


def run_part(path, label):
    if not os.path.exists(path):
        print()
        ui.status_line("err", f"File not found: {path}")
        ui.status_line("info", "Make sure all .py files are in the same folder.")
        ui.pause()
        return

    ui.clear()
    print(ui.box(
        [(f"Launching: {label}", "c"), "---", ("Starting sub-program...", "c")],
        title="STARTING"
    ))
    print()
    subprocess.run([sys.executable, path])
    print()
    print(ui.section("RETURNED TO LAUNCHER"))
    ui.status_line("ok", f"{label} finished.")
    ui.pause("Press Enter to return to the main menu...")


def main():
    while True:
        ui.clear()
        print(LOGO)
        print(ui.box([
            (SUBTITLE, "c"),
            (VERSION, "c"),
        ]))
        print()
        print(ui.box([
            ("MAIN MENU", "c"),
            "---",
            "  1)  Phonebook Application     (Part 1)",
            "  2)  Patient Data Analysis     (Part 2)",
            "---",
            "  0)  Exit",
        ], width=50))

        choice = ui.prompt("Select option")

        if choice == "1":
            run_part(PART1, "Phonebook Application")
        elif choice == "2":
            run_part(PART2, "Patient Data Analysis")
        elif choice == "0":
            ui.clear()
            print(ui.box([
                ("Thank you for using the app!", "c"),
                ("Goodbye.", "c"),
            ], title="BYE"))
            print()
            sys.exit(0)
        else:
            ui.status_line("err", "Invalid choice. Enter 1, 2, or 0.")
            ui.pause()


if __name__ == "__main__":
    main()
