# ============================================================
#  patient_analysis.py  --  Part 2: Patient Data Analysis
#  University Mini Project
# ============================================================

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import ui

# ── Check dependencies before importing ──────────────────────
try:
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")          # non-interactive backend (safe everywhere)
    import matplotlib.pyplot as plt
except ImportError as e:
    ui.clear()
    print(ui.box([
        ("MISSING DEPENDENCY", "c"),
        "---",
        str(e),
        "---",
        "Run:  pip install pandas matplotlib",
    ], title="ERROR"))
    ui.pause("Press Enter to exit...")
    sys.exit(1)

# ── Output folder ─────────────────────────────────────────────
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def out(filename):
    return os.path.join(OUTPUT_DIR, filename)


# ════════════════════════════════════════════════════════════
#  STEPS
# ════════════════════════════════════════════════════════════

def step_header(num, title):
    print()
    print(ui.section(f"STEP {num}: {title}"))
    print()

def run_analysis():
    ui.clear()
    print(ui.box([
        ("PATIENT DATA ANALYSIS", "c"),
        ("Part 2  --  pandas + matplotlib", "c"),
    ]))

    # ── Step 1: Create patients.csv ───────────────────────────
    step_header(1, "Building patients.csv")

    patients_data = {
        "ID":     [1, 2, 3, 4, 5],
        "Age":    [25, 40, 30, 50, 35],
        "Gender": ["M", "F", "M", "F", "M"],
        "Q1":  [3, 4, 2, 5, 3], "Q2":  [4, 4, 3, 5, 3],
        "Q3":  [5, 4, 3, 5, 4], "Q4":  [2, 3, 2, 4, 3],
        "Q5":  [1, 2, 2, 4, 3], "Q6":  [3, 4, 3, 5, 3],
        "Q7":  [4, 4, 3, 5, 4], "Q8":  [5, 4, 3, 5, 3],
        "Q9":  [2, 3, 2, 4, 3], "Q10": [3, 4, 3, 5, 4],
    }
    df = pd.DataFrame(patients_data)
    df.to_csv(out("patients.csv"), index=False)
    ui.status_line("ok", "patients.csv created")

    # Reload and show as table
    df = pd.read_csv(out("patients.csv"))
    rows = [list(r) for r in df[["ID", "Age", "Gender"]].itertuples(index=False)]
    print()
    print(ui.table(["ID", "Age", "Gender"], rows, [4, 5, 8]))
    ui.status_line("info", f"Loaded {len(df)} records  |  Columns: {list(df.columns)}")

    # ── Step 2: Compute averages ──────────────────────────────
    step_header(2, "Computing Average Scores (Q1-Q10)")

    q_cols = [f"Q{i}" for i in range(1, 11)]
    df["AverageScore"] = df[q_cols].mean(axis=1).round(2)

    best_id  = df.loc[df["AverageScore"].idxmax(), "ID"]
    worst_id = df.loc[df["AverageScore"].idxmin(), "ID"]

    rows = [(int(r.ID), f"{r.AverageScore:.2f}") for r in df[["ID","AverageScore"]].itertuples(index=False)]
    print(ui.table(["Patient ID", "Avg Score"], rows, [10, 10]))
    print()
    ui.status_line("ok", f"Highest average  -->  Patient {best_id}")
    ui.status_line("ok", f"Lowest  average  -->  Patient {worst_id}")

    # ── Step 3: Gender count ──────────────────────────────────
    step_header(3, "Gender Distribution")

    gender_counts = df["Gender"].value_counts()
    rows = [("Male"   if g == "M" else "Female", int(c))
            for g, c in gender_counts.items()]
    print(ui.table(["Gender", "Count"], rows, [8, 6]))

    # ── Step 4: Save results.csv ──────────────────────────────
    step_header(4, "Saving results.csv")

    df[["ID", "AverageScore"]].to_csv(out("results.csv"), index=False)
    ui.status_line("ok", f"results.csv saved  -->  {out('results.csv')}")

    # ── Step 5: Charts ────────────────────────────────────────
    step_header(5, "Generating Charts (3 PNG files)")

    PALETTE = ["#2E4057", "#048A81", "#54C6EB", "#8B4513", "#E76F51"]

    ui.spinner("Bar chart: avg score per patient   ", seconds=0.6)
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(df["ID"].astype(str), df["AverageScore"],
                  color=PALETTE[:len(df)], edgecolor="white", linewidth=1.2)
    ax.bar_label(bars, fmt="%.2f", padding=4, fontsize=9, color="#333")
    ax.set_xlabel("Patient ID"); ax.set_ylabel("Average Score")
    ax.set_title("Average Score per Patient", fontweight="bold")
    ax.set_ylim(0, 5.5); ax.spines[["top","right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(out("chart_avg_per_patient.png"), dpi=150); plt.close()

    ui.spinner("Line plot: avg score per question  ", seconds=0.6)
    q_means = df[q_cols].mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(q_cols, q_means.values, marker="o", color="#048A81",
            linewidth=2.2, markersize=7, markerfacecolor="white", markeredgewidth=2.2)
    ax.fill_between(range(len(q_cols)), q_means.values, alpha=0.12, color="#048A81")
    ax.set_xticks(range(len(q_cols))); ax.set_xticklabels(q_cols, fontsize=9)
    ax.set_xlabel("Question"); ax.set_ylabel("Mean Score")
    ax.set_title("Average Score per Question", fontweight="bold")
    ax.set_ylim(0, 5.5); ax.spines[["top","right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(out("chart_avg_per_question.png"), dpi=150); plt.close()

    ui.spinner("Pie chart: gender distribution     ", seconds=0.6)
    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(
        gender_counts.values,
        labels=["Male" if g == "M" else "Female" for g in gender_counts.index],
        colors=["#2E4057", "#E76F51"], autopct="%1.0f%%", startangle=120,
        pctdistance=0.75, wedgeprops={"linewidth": 2, "edgecolor": "white"})
    for at in autotexts:
        at.set_fontsize(13); at.set_fontweight("bold"); at.set_color("white")
    ax.set_title("Gender Distribution", fontweight="bold")
    fig.tight_layout(); fig.savefig(out("chart_gender_pie.png"), dpi=150); plt.close()

    # ── Step 6: visits.csv + merge ────────────────────────────
    step_header(6, "Creating visits.csv and Merging")

    visits_data = {
        "ID":            [1,  2,  3,  4,  5],
        "Visits":        [5,  2,  3,  6,  1],
        "LastVisitDays": [10, 30, 20, 5,  60],
    }
    visits_df = pd.DataFrame(visits_data)
    visits_df.to_csv(out("visits.csv"), index=False)
    ui.status_line("ok", "visits.csv created")

    merged = pd.merge(df, visits_df, on="ID")
    rows = [(int(r.ID), r.Gender, f"{r.AverageScore:.2f}", int(r.Visits), int(r.LastVisitDays))
            for r in merged[["ID","Gender","AverageScore","Visits","LastVisitDays"]].itertuples(index=False)]
    print()
    print(ui.table(["ID","Gender","Avg","Visits","LastDays"], rows, [4,7,6,7,9]))

    # ── Step 7: Status column ─────────────────────────────────
    step_header(7, "Assigning Status")

    def assign_status(avg):
        if avg < 3:   return "Critical"
        elif avg <= 4: return "Stable"
        else:          return "Good"

    merged["Status"] = merged["AverageScore"].apply(assign_status)
    rows = [(int(r.ID), f"{r.AverageScore:.2f}", r.Status)
            for r in merged[["ID","AverageScore","Status"]].itertuples(index=False)]
    print(ui.table(["ID", "Avg Score", "Status"], rows, [4, 10, 10]))

    # ── Step 8: Boost scores +1, cap at 5 ────────────────────
    step_header(8, "Boosting Scores +1 (cap: 5)")

    merged[q_cols] = merged[q_cols].apply(lambda col: col + 1).clip(upper=5)
    merged["AverageScore"] = merged[q_cols].mean(axis=1).round(2)
    ui.status_line("ok", "All Q1-Q10 scores increased by 1 (max 5). Averages updated.")

    # ── Step 9: Drop patients with LastVisitDays > 50 ─────────
    step_header(9, "Removing Inactive Patients (LastVisitDays > 50)")

    before = len(merged)
    dropped = merged[merged["LastVisitDays"] > 50][["ID","LastVisitDays"]]
    merged  = merged[merged["LastVisitDays"] <= 50].reset_index(drop=True)
    after   = len(merged)

    if len(dropped):
        rows = [(int(r.ID), int(r.LastVisitDays)) for r in dropped.itertuples(index=False)]
        print(ui.table(["Removed ID", "LastVisitDays"], rows, [10, 13]))
    ui.status_line("ok", f"Removed {before - after} patient(s). Remaining: {after}")

    # ── Step 10: Export filtered subsets ─────────────────────
    step_header(10, "Exporting Filtered Subsets")

    high_avg = merged[merged["AverageScore"] > 4]
    high_avg.to_csv(out("high_average_patients.csv"), index=False)
    ui.status_line("ok", f"high_average_patients.csv  -->  {len(high_avg)} patient(s)")

    frequent = merged[merged["Visits"] > 3]
    frequent.to_csv(out("frequent_visitors.csv"), index=False)
    ui.status_line("ok", f"frequent_visitors.csv      -->  {len(frequent)} patient(s)")

    # ── Summary ───────────────────────────────────────────────
    print()
    print(ui.box([
        ("ANALYSIS COMPLETE", "c"),
        "---",
        ("All files saved to:  output/", "c"),
        "---",
        "  patients.csv               visits.csv",
        "  results.csv                high_average_patients.csv",
        "  frequent_visitors.csv",
        "  chart_avg_per_patient.png",
        "  chart_avg_per_question.png",
        "  chart_gender_pie.png",
    ], title="DONE"))
    ui.pause()


def main():
    ui.clear()
    print(ui.box([
        ("PATIENT DATA ANALYSIS", "c"),
        ("Part 2  --  pandas + matplotlib", "c"),
        "---",
        "  This will run all 10 analysis steps",
        "  and save results to the output/ folder.",
        "---",
        "  1)  Run Full Analysis",
        "  0)  Back to Launcher",
    ], width=52))

    choice = ui.prompt("Select option")
    if choice == "1":
        run_analysis()
    else:
        return


if __name__ == "__main__":
    main()
