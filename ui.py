# ============================================================
#  ui.py  --  Shared ASCII UI toolkit
#  Cross-platform: Windows CMD / PowerShell / Linux / macOS
# ============================================================
#
#  All box-drawing uses plain ASCII (+, -, |) so every shell
#  renders them correctly without needing Unicode support.
#
#  Symbols used:
#    [OK]   success
#    [!!]   error / warning
#    [--]   info / neutral
#    [??]   prompt / question
# ============================================================

import os
import sys
import time

# ── Terminal width (safe default 60) ─────────────────────────
def term_width():
    try:
        return min(os.get_terminal_size().columns, 72)
    except Exception:
        return 60

# ── Clear screen (works on all platforms) ────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ── Pause ────────────────────────────────────────────────────
def pause(msg="Press Enter to continue..."):
    print()
    input(f"  {msg}")

# ════════════════════════════════════════════════════════════
#  BOX DRAWING  (pure ASCII, universally compatible)
# ════════════════════════════════════════════════════════════

def _hline(width, left="+", fill="-", right="+"):
    return left + fill * (width - 2) + right

def box(lines, width=None, title=None):
    """
    Render lines of text inside an ASCII box.
    Each line is a string or a (text, align) tuple.
    align: 'l' (default) | 'c' | 'r'
    """
    w = width or term_width()
    inner = w - 4          # 2 for borders, 2 for padding spaces

    def fmt(line):
        if isinstance(line, tuple):
            text, align = line
        else:
            text, align = line, "l"
        text = str(text)
        # Truncate if too long
        if len(text) > inner:
            text = text[: inner - 3] + "..."
        if align == "c":
            return text.center(inner)
        elif align == "r":
            return text.rjust(inner)
        else:
            return text.ljust(inner)

    top    = _hline(w)
    bottom = _hline(w)
    sep    = _hline(w, "+", "-", "+")

    out = []
    if title:
        t = f"[ {title} ]"
        title_line = "| " + t.center(inner) + " |"
        out.append(top)
        out.append(title_line)
        out.append(sep)
    else:
        out.append(top)

    for line in lines:
        if line == "---":          # horizontal rule inside box
            out.append(sep)
        else:
            out.append("| " + fmt(line) + " |")

    out.append(bottom)
    return "\n".join(out)


def section(title, width=None):
    """A slim section header bar."""
    w = width or term_width()
    inner = w - 4
    t = f"-- {title} --"
    return "\n+" + t.center(w - 2, "-") + "+"


def status_line(symbol, text):
    """Print a status message with a symbol tag."""
    tags = {"ok": "[OK]", "err": "[!!]", "info": "[--]", "q": "[??]"}
    tag = tags.get(symbol, "[--]")
    print(f"  {tag} {text}")


def table(headers, rows, col_widths=None):
    """
    Render a plain ASCII table.
    headers: list of str
    rows:    list of lists/tuples
    col_widths: optional list of ints (auto-computed if omitted)
    """
    if not col_widths:
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

    def row_line(cells):
        parts = [str(c).ljust(col_widths[i]) for i, c in enumerate(cells)]
        return "| " + " | ".join(parts) + " |"

    def sep_line():
        dashes = ["-" * w for w in col_widths]
        return "+-" + "-+-".join(dashes) + "-+"

    lines = [sep_line(), row_line(headers), sep_line()]
    for row in rows:
        lines.append(row_line(row))
    lines.append(sep_line())
    return "\n".join(lines)


def progress_bar(label, steps, delay=0.04):
    """Animate a simple ASCII progress bar."""
    width = 30
    print(f"\n  {label}")
    for i in range(steps + 1):
        filled = int(width * i / steps)
        bar    = "#" * filled + "." * (width - filled)
        pct    = int(100 * i / steps)
        print(f"  [{bar}] {pct:3d}%", end="\r")
        time.sleep(delay)
    print()


def spinner(label, seconds=1.2):
    """Show a spinning indicator for a brief moment."""
    frames = ["|", "/", "-", "\\"]
    end    = time.time() + seconds
    i      = 0
    while time.time() < end:
        print(f"  {frames[i % 4]}  {label}", end="\r")
        time.sleep(0.1)
        i += 1
    print(f"  [OK] {label}")


def prompt(msg, symbol=">>"):
    """Styled input prompt."""
    return input(f"\n  {symbol} {msg}: ").strip()


def confirm(msg):
    """Yes/no prompt, returns bool."""
    ans = prompt(f"{msg} (yes/no)", symbol="[??]").lower()
    return ans in ("yes", "y")
