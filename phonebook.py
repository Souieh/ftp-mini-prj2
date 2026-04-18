# ============================================================
#  phonebook.py  --  Part 1: Phonebook Application
#  University Mini Project
# ============================================================

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import ui

# ── Data ─────────────────────────────────────────────────────
phonebook = {
    "Amine":   "0552-23-45-67",
    "Nour":    "0661-34-56-78",
    "Salah":   "0770-11-22-33",
    "Kenza":   "0558-90-12-34",
    "Yasmine": "0662-44-55-66",
    "Walid":   "0771-78-89-90",
    "Lina":    "0551-65-43-21",
    "Rachid":  "0665-98-76-54",
    "Sara":    "0772-12-34-56",
    "Farid":   "0554-67-89-01",
}
backup = {}


# ── Screen header ─────────────────────────────────────────────
def screen(title):
    ui.clear()
    print(ui.box([
        ("PHONEBOOK APPLICATION", "c"),
        (f">> {title} <<", "c"),
    ]))
    print()


# ════════════════════════════════════════════════════════════
#  FEATURES
# ════════════════════════════════════════════════════════════

def print_all():
    screen("All Contacts")
    if not phonebook:
        ui.status_line("info", "Phonebook is empty.")
    else:
        rows = [(name, num) for name, num in phonebook.items()]
        print(ui.table(["Name", "Phone Number"], rows, [14, 16]))
    ui.pause()

def add_contact():
    screen("Add New Contact")
    name = ui.prompt("Name").title()
    if not name:
        ui.status_line("err", "Name cannot be empty.")
        ui.pause(); return
    if name in phonebook:
        ui.status_line("err", f"'{name}' already exists. Use Update to change the number.")
        ui.pause(); return
    number = ui.prompt("Phone number")
    phonebook[name] = number
    ui.status_line("ok", f"'{name}' added successfully.")
    ui.pause()

def update_contact():
    screen("Update Contact")
    name = ui.prompt("Name to update").title()
    if name not in phonebook:
        ui.status_line("err", f"'{name}' not found.")
        ui.pause(); return
    ui.status_line("info", f"Current number: {phonebook[name]}")
    new_num = ui.prompt("New phone number")
    phonebook[name] = new_num
    ui.status_line("ok", f"'{name}' updated successfully.")
    ui.pause()

def delete_contact():
    screen("Delete Contact")
    name = ui.prompt("Name to delete").title()
    if name not in phonebook:
        ui.status_line("err", f"'{name}' not found.")
        ui.pause(); return
    if ui.confirm(f"Delete '{name}' ({phonebook[name]})?"):
        del phonebook[name]
        ui.status_line("ok", f"'{name}' deleted.")
    else:
        ui.status_line("info", "Cancelled.")
    ui.pause()

def search_contact():
    screen("Search Contact")
    name = ui.prompt("Name to search").title()
    if name in phonebook:
        print()
        print(ui.table(["Name", "Phone Number"], [(name, phonebook[name])], [14, 16]))
    else:
        ui.status_line("err", f"'{name}' not found.")
    ui.pause()

def contact_exists():
    screen("Check Contact")
    name = ui.prompt("Name to check").title()
    if name in phonebook:
        ui.status_line("ok", f"'{name}' EXISTS in the phonebook  -->  {phonebook[name]}")
    else:
        ui.status_line("err", f"'{name}' does NOT exist.")
    ui.pause()

def list_alphabetical():
    screen("Contacts A to Z")
    if not phonebook:
        ui.status_line("info", "Phonebook is empty.")
    else:
        rows = [(name, phonebook[name]) for name in sorted(phonebook)]
        print(ui.table(["Name", "Phone Number"], rows, [14, 16]))
    ui.pause()

def list_numbers():
    screen("All Phone Numbers")
    rows = [(i + 1, num) for i, num in enumerate(phonebook.values())]
    print(ui.table(["#", "Phone Number"], rows, [4, 16]))
    ui.pause()

def count_contacts():
    screen("Contact Count")
    total = len(phonebook)
    print(ui.box([
        (f"Total contacts in phonebook: {total}", "c"),
    ], width=46))
    ui.pause()

def search_by_area_code():
    screen("Search by Area Code")
    code = ui.prompt("Enter area code (e.g. 055)")
    matches = [(n, num) for n, num in phonebook.items() if num.startswith(code)]
    if matches:
        ui.status_line("ok", f"Found {len(matches)} contact(s) with area code '{code}':")
        print()
        print(ui.table(["Name", "Phone Number"], matches, [14, 16]))
    else:
        ui.status_line("err", f"No contacts found with area code '{code}'.")
    ui.pause()

def create_backup():
    screen("Create Backup")
    global backup
    backup = phonebook.copy()
    ui.status_line("ok", f"Backup created  --  {len(backup)} contact(s) saved.")
    ui.pause()

def clear_phonebook():
    screen("Clear Phonebook")
    ui.status_line("info", f"This will remove all {len(phonebook)} contact(s)!")
    if ui.confirm("Are you sure you want to clear the phonebook?"):
        phonebook.clear()
        ui.status_line("ok", "Phonebook cleared.")
    else:
        ui.status_line("info", "Cancelled.")
    ui.pause()

def restore_backup():
    screen("Restore from Backup")
    if not backup:
        ui.status_line("err", "No backup found. Create a backup first (option k).")
        ui.pause(); return
    phonebook.update(backup)
    ui.status_line("ok", f"Restored {len(backup)} contact(s) from backup.")
    ui.pause()

def search_by_letter():
    screen("Search by First Letter")
    letter = ui.prompt("Enter a letter (A-Z)").upper()
    if not letter.isalpha() or len(letter) != 1:
        ui.status_line("err", "Please enter a single letter.")
        ui.pause(); return
    matches = [(n, num) for n, num in phonebook.items() if n.upper().startswith(letter)]
    if matches:
        ui.status_line("ok", f"Found {len(matches)} contact(s) starting with '{letter}':")
        print()
        print(ui.table(["Name", "Phone Number"], matches, [14, 16]))
    else:
        ui.status_line("err", f"No contacts start with '{letter}'.")
    ui.pause()


# ════════════════════════════════════════════════════════════
#  MENU
# ════════════════════════════════════════════════════════════
ACTIONS = {
    "a": ("Print all contacts",          print_all),
    "b": ("Add a new contact",           add_contact),
    "c": ("Update a contact's number",   update_contact),
    "d": ("Delete a contact",            delete_contact),
    "e": ("Search for a contact",        search_contact),
    "f": ("Check if a contact exists",   contact_exists),
    "g": ("List names alphabetically",   list_alphabetical),
    "h": ("List all phone numbers",      list_numbers),
    "i": ("Count total contacts",        count_contacts),
    "j": ("Search by area code",         search_by_area_code),
    "k": ("Create backup",               create_backup),
    "l": ("Clear phonebook",             clear_phonebook),
    "m": ("Restore from backup",         restore_backup),
    "n": ("Search by first letter",      search_by_letter),
}

def show_menu():
    ui.clear()
    print(ui.box([("PHONEBOOK APPLICATION", "c"), ("Part 1  --  Dictionary Operations", "c")]))
    print()
    menu_lines = [("MENU", "c"), "---"]
    for key, (label, _) in ACTIONS.items():
        menu_lines.append(f"  {key})  {label}")
    menu_lines += ["---", "  0)  Back to Launcher"]
    print(ui.box(menu_lines, width=50))
    print()
    ui.status_line("info", f"Contacts loaded: {len(phonebook)}  |  Backup: {'Yes' if backup else 'No'}")

def main():
    while True:
        show_menu()
        choice = ui.prompt("Choose an option").lower()
        if choice == "0":
            break
        elif choice in ACTIONS:
            ACTIONS[choice][1]()
        else:
            ui.status_line("err", "Invalid option.")
            ui.pause()

if __name__ == "__main__":
    main()
