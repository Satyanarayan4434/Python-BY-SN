from pathlib import Path

from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "#30 Python_Day_30_Function_Arguments_in_Python.pdf"

W, H = 1080, 1350
TOTAL = 7

BG = colors.HexColor("#06131f")
PANEL = colors.HexColor("#0d2030")
PANEL_HEAD = colors.HexColor("#14293c")
BLUE = colors.HexColor("#2c84ff")
BLUE_DARK = colors.HexColor("#12345b")
GREEN = colors.HexColor("#2df78a")
GREEN_DARK = colors.HexColor("#083b35")
YELLOW = colors.HexColor("#ffe052")
RED = colors.HexColor("#ff6170")
PURPLE = colors.HexColor("#8768ff")
MUTED = colors.HexColor("#8da0b6")
WHITE = colors.HexColor("#f5f8fb")


def sw(text, font="Helvetica", size=24):
    return stringWidth(text, font, size)


def draw_wrapped(c, text, x, y, max_width, font="Helvetica", size=24, leading=None, fill=WHITE):
    leading = leading or size * 1.28
    c.setFont(font, size)
    c.setFillColor(fill)
    words = text.split()
    lines = []
    line = ""
    for word in words:
        trial = word if not line else f"{line} {word}"
        if sw(trial, font, size) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def fit_text(c, text, x, y, max_width, font="Helvetica-Bold", size=66, min_size=28, fill=WHITE):
    while size > min_size and sw(text, font, size) > max_width:
        size -= 2
    c.setFont(font, size)
    c.setFillColor(fill)
    c.drawString(x, y, text)
    return size


def rounded_rect(c, x, y, w, h, stroke, fill=None, radius=18, width=2):
    c.setLineWidth(width)
    c.setStrokeColor(stroke)
    if fill:
        c.setFillColor(fill)
    c.roundRect(x, y, w, h, radius, stroke=1, fill=1 if fill else 0)


def small_chip(c, text, x, y, color=GREEN, bg=None, w=None):
    font_size = 18
    pad_x = 22
    w = w or sw(text, "Helvetica-Bold", font_size) + pad_x * 2
    bg = bg or colors.HexColor("#123047")
    c.setFillColor(bg)
    c.roundRect(x, y, w, 42, 20, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", font_size)
    c.setFillColor(color)
    c.drawCentredString(x + w / 2, y + 14, text)


def code_panel(c, x, y, w, h, title, lines, title_color=GREEN, border=BLUE, highlight=None):
    rounded_rect(c, x, y, w, h, border, PANEL, radius=18, width=2)
    c.setFillColor(PANEL_HEAD)
    c.roundRect(x, y + h - 58, w, 58, 18, stroke=0, fill=1)
    c.setFillColor(RED)
    c.circle(x + 28, y + h - 29, 7, stroke=0, fill=1)
    c.setFillColor(YELLOW)
    c.circle(x + 51, y + h - 29, 7, stroke=0, fill=1)
    c.setFillColor(GREEN)
    c.circle(x + 74, y + h - 29, 7, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(title_color)
    c.drawRightString(x + w - 28, y + h - 36, title)

    top_y = y + h - 104
    bottom_y = y + 38
    leading = min(38, (top_y - bottom_y) / max(1, len(lines) - 1))
    font_size = min(22, max(13, leading * 0.62))
    max_text_w = w - 76
    for raw in lines:
        text = raw[0] if isinstance(raw, tuple) else raw
        while font_size > 13 and sw(text, "Courier-Bold", font_size) > max_text_w:
            font_size -= 1
    leading = max(font_size * 1.35, leading)

    line_y = top_y
    c.setFont("Courier-Bold", font_size)
    for idx, raw in enumerate(lines):
        text, color = raw if isinstance(raw, tuple) else (raw, WHITE)
        if highlight is not None and idx == highlight:
            c.setFillColor(colors.HexColor("#113d3f"))
            c.roundRect(x + 24, line_y - 8, w - 48, font_size + 15, 8, stroke=0, fill=1)
        c.setFillColor(color)
        c.drawString(x + 38, line_y, text)
        line_y -= leading


def header(c, page_num):
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 21)
    c.drawString(74, H - 92, "DAY 30/55")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 16)
    c.drawString(74, 62, "Prepared by Satyanarayan Sen")
    c.drawRightString(W - 74, 62, f"{page_num}/{TOTAL}")


def decorations(c):
    c.setFillColor(GREEN_DARK)
    c.circle(30, H - 90, 210, stroke=0, fill=1)
    c.setFillColor(BLUE_DARK)
    c.circle(W - 100, H - 100, 250, stroke=0, fill=1)
    c.setStrokeColor(GREEN)
    c.setLineWidth(3)
    for i in range(3):
        y = H - 155 - i * 48
        c.line(W - 320, y, W - 90, y)
        c.circle(W - 320, y, 5, stroke=0, fill=1)
        c.circle(W - 90, y, 5, stroke=0, fill=1)


def background(c, page_num):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    decorations(c)
    header(c, page_num)


def note_bar(c, text, y, border=BLUE, size=28):
    rounded_rect(c, 118, y, 844, 90, border, colors.HexColor("#0c2236"), radius=20)
    while size > 18 and sw(text, "Helvetica-Bold", size) > 780:
        size -= 1
    c.setFont("Helvetica-Bold", size)
    c.setFillColor(WHITE)
    c.drawCentredString(540, y + 34, text)


def card(c, x, y, w, h, title, body, color):
    rounded_rect(c, x, y, w, h, color, colors.HexColor("#0c2236"), radius=18)
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(color)
    c.drawString(x + 26, y + h - 40, title)
    draw_wrapped(c, body, x + 26, y + h - 72, w - 52, size=18, leading=23, fill=WHITE)


def slide_1(c):
    background(c, 1)
    small_chip(c, "function arguments", 74, H - 218, BLUE, colors.HexColor("#123a70"), w=310)
    fit_text(c, "Make", 74, 900, 420, size=88)
    fit_text(c, "functions", 74, 806, 620, size=88, fill=YELLOW)
    fit_text(c, "flexible", 74, 712, 520, size=88, fill=GREEN)
    code_panel(
        c,
        610,
        660,
        400,
        330,
        "Argument toolkit",
        [
            ("def greet(name=\"Guest\")", GREEN),
            ("def add(*nums)", YELLOW),
            ("profile(age=25)", BLUE),
            ("def user(**data)", PURPLE),
        ],
        border=GREEN,
    )
    rounded_rect(c, 74, 404, 860, 132, BLUE, colors.HexColor("#0c2236"), radius=22)
    c.setFont("Helvetica-Bold", 31)
    c.setFillColor(WHITE)
    c.drawString(106, 484, "Arguments decide how flexible a function feels.")
    c.setFont("Helvetica", 20)
    c.setFillColor(MUTED)
    c.drawString(106, 446, "Defaults, *args, keywords, and **kwargs solve different call styles.")


def slide_2(c):
    background(c, 2)
    fit_text(c, "Default", 74, 1050, 430, size=66)
    fit_text(c, "arguments", 74, 974, 520, size=66, fill=GREEN)
    code_panel(
        c,
        120,
        610,
        840,
        340,
        "Fallback values",
        [
            ("def greet(name, msg=\"Welcome\"):", GREEN),
            ("    print(msg, name)", WHITE),
            ("", WHITE),
            ("greet(\"Satya\")", YELLOW),
            ("greet(\"Satya\", \"Hello\")", BLUE),
        ],
        border=GREEN,
        highlight=0,
    )
    card(c, 120, 390, 250, 118, "No value?", "Python uses the default parameter value.", GREEN)
    card(c, 415, 390, 250, 118, "Override", "Pass a new value when you need different behavior.", BLUE)
    card(c, 710, 390, 250, 118, "Prevents errors", "Useful when a parameter can safely fall back.", YELLOW)


def slide_3(c):
    background(c, 3)
    fit_text(c, "Variable", 74, 1050, 500, size=66)
    fit_text(c, "length args", 74, 974, 560, size=66, fill=YELLOW)
    code_panel(
        c,
        120,
        610,
        840,
        340,
        "*args",
        [
            ("def add(*nums):", GREEN),
            ("    total = 0", WHITE),
            ("    for n in nums:", YELLOW),
            ("        total += n", WHITE),
            ("    return total", BLUE),
            ("", WHITE),
            ("add(2, 4, 6)", PURPLE),
        ],
        border=YELLOW,
        highlight=0,
    )
    card(c, 120, 390, 250, 118, "One star", "* collects extra positional arguments.", YELLOW)
    card(c, 415, 390, 250, 118, "Tuple", "Inside the function, nums behaves like a tuple.", GREEN)
    card(c, 710, 390, 250, 118, "Flexible count", "Call with two, three, or many values.", BLUE)


def slide_4(c):
    background(c, 4)
    fit_text(c, "Keyword", 74, 1050, 500, size=66)
    fit_text(c, "arguments", 74, 974, 520, size=66, fill=BLUE)
    code_panel(
        c,
        74,
        570,
        430,
        360,
        "Positional risk",
        [
            ("def student(name, age):", GREEN),
            ("    print(name, age)", WHITE),
            ("", WHITE),
            ("student(21, \"Satya\")", RED),
            ("# order is wrong", MUTED),
        ],
        border=RED,
        highlight=3,
    )
    code_panel(
        c,
        576,
        570,
        430,
        360,
        "Readable call",
        [
            ("student(age=21,", BLUE),
            ("        name=\"Satya\")", WHITE),
            ("", WHITE),
            ("# names map values", GREEN),
            ("# order is clear", GREEN),
        ],
        border=BLUE,
        highlight=0,
    )
    note_bar(c, "Keyword arguments make calls readable and avoid position mistakes.", 372, border=BLUE, size=24)


def slide_5(c):
    background(c, 5)
    fit_text(c, "Keyword", 74, 1050, 500, size=66)
    fit_text(c, "length args", 74, 974, 560, size=66, fill=PURPLE)
    code_panel(
        c,
        120,
        610,
        840,
        340,
        "**kwargs",
        [
            ("def profile(**data):", GREEN),
            ("    for key, value in data.items():", YELLOW),
            ("        print(key, value)", WHITE),
            ("", WHITE),
            ("profile(name=\"Satya\", age=21,", BLUE),
            ("        city=\"Pune\")", BLUE),
        ],
        border=PURPLE,
        highlight=0,
    )
    card(c, 120, 390, 250, 118, "Two stars", "** collects named arguments.", PURPLE)
    card(c, 415, 390, 250, 118, "Dictionary", "Inside the function, data is a dict.", GREEN)
    card(c, 710, 390, 250, 118, "Dynamic keys", "Handle name, age, city, or any extra field.", BLUE)


def slide_6(c):
    background(c, 6)
    fit_text(c, "Choose", 74, 1050, 430, size=66)
    fit_text(c, "the right tool", 74, 974, 620, size=66, fill=YELLOW)
    code_panel(
        c,
        120,
        610,
        840,
        340,
        "Argument map",
        [
            ("default value   -> optional input", GREEN),
            ("*args           -> many values", YELLOW),
            ("keyword=value   -> readable mapping", BLUE),
            ("**kwargs        -> many named values", PURPLE),
        ],
        border=YELLOW,
    )
    card(c, 120, 390, 250, 118, "Default", "Best when a missing value has a safe fallback.", GREEN)
    card(c, 415, 390, 250, 118, "*args", "Best when the number of values can change.", YELLOW)
    card(c, 710, 390, 250, 118, "**kwargs", "Best when named fields can change.", PURPLE)


def slide_7(c):
    background(c, 7)
    fit_text(c, "Cheat Sheet", 74, 1050, 620, size=66)
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(GREEN)
    c.drawString(74, 1002, "Python function arguments")
    code_panel(
        c,
        74,
        642,
        860,
        298,
        "Flexible signatures",
        [
            ("def demo(a, b=10, *args, **kwargs):", GREEN),
            ("    print(a, b)", WHITE),
            ("    print(args)    # tuple", YELLOW),
            ("    print(kwargs)  # dict", PURPLE),
        ],
        border=BLUE,
    )
    cards = [
        ("Default", "Use fallback values for optional parameters.", GREEN),
        ("*args", "Collect extra positional values into a tuple.", YELLOW),
        ("Keywords", "Name values at the call site for clarity.", BLUE),
        ("**kwargs", "Collect extra named values into a dictionary.", PURPLE),
    ]
    x_positions = [74, 560, 74, 560]
    y_positions = [484, 484, 318, 318]
    for (title, body, color), x, y in zip(cards, x_positions, y_positions):
        card(c, x, y, 374, 118, title, body, color)
    rounded_rect(c, 132, 155, 816, 90, GREEN, colors.HexColor("#0f2b3c"), radius=20)
    c.setFont("Helvetica-Bold", 31)
    c.setFillColor(WHITE)
    c.drawCentredString(540, 195, "Save this for your Python journey.")
    c.setFont("Helvetica", 16)
    c.setFillColor(MUTED)
    c.drawCentredString(540, 169, "Day 30/55 - Prepared by Satyanarayan Sen")


def build():
    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    for slide in [slide_1, slide_2, slide_3, slide_4, slide_5, slide_6, slide_7]:
        slide(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    build()
