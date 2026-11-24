"""Generate a printable Miryoku cheat sheet PDF from the ZMK keymap file.

usage: python3 scripts/cheatsheet.py [keymap] [out.pdf]
  defaults: boards/shields/corne_xiao_v2/corne_xiao_v2.keymap -> docs/miryoku-cheatsheet.pdf

Requires reportlab (pip install reportlab) and macOS's bundled Arial fonts.
"""
import re
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONT_DIR = "/System/Library/Fonts/Supplemental/"
pdfmetrics.registerFont(TTFont("U", FONT_DIR + "Arial Unicode.ttf"))
pdfmetrics.registerFont(TTFont("B", FONT_DIR + "Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("R", FONT_DIR + "Arial.ttf"))

INK = HexColor("#1d1d1f")
MUTED = HexColor("#6e6e73")
EDGE = HexColor("#8e8e93")
NONE_FILL = HexColor("#ececec")
TRANS_FILL = HexColor("#fafafa")

# One colour per layer (fills are light so it prints fine in grey too)
LAYERS = {
    "BASE":   ("Base",   "#ffffff", "#444444"),
    "BUTTON": ("Button", "#efe3f7", "#7b3fa0"),
    "NAV":    ("Nav",    "#dcefff", "#1f6fb5"),
    "MOUSE":  ("Mouse",  "#e2f5e4", "#2e8540"),
    "MEDIA":  ("Media",  "#ffe7d6", "#c0581b"),
    "NUM":    ("Num",    "#fff3c4", "#a07800"),
    "SYM":    ("Sym",    "#ffdfe5", "#b3304b"),
    "FUN":    ("Fun",    "#e0e6f5", "#40538f"),
}
MOD_FILL = HexColor("#f2f2f7")

# ---------------------------------------------------------------- parsing

ARGC = {"&kp": 1, "&hml": 2, "&hmr": 2, "&lt": 2, "&mkp": 1, "&mmv": 1,
        "&msc": 1, "&out": 1}


def parse(path):
    src = open(path).read()
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    src = re.sub(r"//[^\n]*", "", src)
    layer_ids = dict(re.findall(r"#define\s+(\w+)\s+(\d+)\s*$", src, re.M))
    order = sorted(layer_ids, key=lambda k: int(layer_ids[k]))
    order = [k for k in order if k in LAYERS]
    defines = dict(re.findall(r"#define\s+(U_\w+)\s+(\S+)", src))
    layers = []
    for body in re.findall(r"\w+_layer\s*\{.*?bindings\s*=\s*<(.*?)>;", src, re.S):
        toks = body.split()
        out, i = [], 0
        while i < len(toks):
            t = toks[i]
            n = (2 if toks[i + 1] == "BT_SEL" else 1) if t == "&bt" else ARGC.get(t, 0)
            out.append([t] + [defines.get(a, a) for a in toks[i + 1:i + 1 + n]])
            i += 1 + n
        assert len(out) == 44, (len(out), body[:60])
        layers.append(out)
    return order, layers


KEYS = {
    "SEMI": ";", "SQT": "'", "COMMA": ",", "DOT": ".", "FSLH": "/", "BSLH": "\\",
    "LBKT": "[", "RBKT": "]", "LBRC": "{", "RBRC": "}", "LPAR": "(", "RPAR": ")",
    "EQUAL": "=", "MINUS": "-", "GRAVE": "`", "TILDE": "~", "EXCL": "!", "AT": "@",
    "HASH": "#", "DLLR": "$", "PRCNT": "%", "CARET": "^", "AMPS": "&", "ASTRK": "*",
    "PLUS": "+", "UNDER": "_", "PIPE": "|", "COLON": ":",
    "TAB": "Tab", "ESC": "Esc", "SPC": "Space", "RET": "Enter", "BSPC": "Bksp",
    "DEL": "Del", "INS": "Ins", "HOME": "Home", "END": "End", "PG_UP": "PgUp",
    "PG_DN": "PgDn", "LEFT": "←", "RIGHT": "→", "UP": "↑", "DOWN": "↓",
    "PSCRN": "PrtSc", "SLCK": "ScrLk", "PAUSE_BREAK": "Pause", "K_APP": "Menu",
    "C_PREV": "Prev", "C_NEXT": "Next", "C_VOL_UP": "Vol +", "C_VOL_DN": "Vol −",
    "C_PP": "Play", "C_STOP": "Stop", "C_MUTE": "Mute",
    "LG(Z)": "Undo", "LG(X)": "Cut", "LG(C)": "Copy", "LG(V)": "Paste",
    "LG(LS(Z))": "Redo",
}
MODS = {"LGUI": "Cmd", "RGUI": "Cmd", "LALT": "Opt", "RALT": "AltGr",
        "LCTRL": "Ctrl", "RCTRL": "Ctrl", "LSHFT": "Shift", "RSHFT": "Shift"}
POINT = {"MOVE_LEFT": "←", "MOVE_RIGHT": "→", "MOVE_UP": "↑", "MOVE_DOWN": "↓",
         "SCRL_LEFT": "←", "SCRL_RIGHT": "→", "SCRL_UP": "↑", "SCRL_DOWN": "↓",
         "LCLK": "L Click", "RCLK": "R Click", "MCLK": "M Click"}


def keyname(k):
    if k in KEYS:
        return KEYS[k]
    if re.fullmatch(r"N\d", k):
        return k[1]
    if re.fullmatch(r"F\d+", k) or re.fullmatch(r"[A-Z]", k):
        return k
    return k


def describe(b):
    """-> (kind, tap, hold, hold_layer)"""
    t = b[0]
    if t == "&trans":
        return "trans", "", "", None
    if t == "&none":
        return "none", "", "", None
    if t == "&kp":
        if b[1] in MODS:
            return "mod", MODS[b[1]], "", None
        return "key", keyname(b[1]), "", None
    if t in ("&hml", "&hmr"):
        return "key", keyname(b[2]), MODS[b[1]], None
    if t == "&lt":
        return "key", keyname(b[2]), LAYERS[b[1]][0], b[1]
    if t == "&mkp":
        return "key", POINT[b[1]], "", None
    if t == "&mmv":
        return "key", "Mouse " + POINT[b[1]], "", None
    if t == "&msc":
        return "key", "Wheel " + POINT[b[1]], "", None
    if t == "&bt":
        return "key", ("BT " + b[2]) if b[1] == "BT_SEL" else "BT Clear", "", None
    if t == "&out":
        return "key", "USB / BT", "", None
    if t == "&caps_word":
        return "key", "Caps Word", "", None
    if t == "&td_boot":
        return "key", "Boot", "tap twice", None
    return "key", t.lstrip("&"), "", None


# ---------------------------------------------------------------- geometry

# Column stagger (key units, downwards) for a Corne, outer -> inner
STAGGER = [0.35, 0.35, 0.12, 0.0, 0.12, 0.24]
HALF_GAP = 1.6


def positions():
    """Map binding index (0..43) -> (x, y) top-left in key units."""
    pos = {}
    def left(col, row):
        return col, row + STAGGER[col]
    def right(col, row):  # col 0 = innermost
        return 6 + HALF_GAP + col, row + STAGGER[5 - col]
    for r, base in ((0, 0), (1, 12)):
        for c in range(6):
            pos[base + c] = left(c, r)
            pos[base + 6 + c] = right(c, r)
    for c in range(6):
        pos[24 + c] = left(c, 2)
        pos[32 + c] = right(c, 2)
    for i, c in enumerate((3.4, 4.45, 5.5)):
        pos[38 + i] = (c, 3.35 + (0.12 * i))
    for i, c in enumerate((0, 1.05, 2.1)):
        pos[41 + i] = (6 + HALF_GAP - 0.5 + c, 3.35 + 0.24 - 0.12 * i)
    return pos


POS = positions()
WIDTH_U = 12 + HALF_GAP
HEIGHT_U = 4.6


def fit(c, text, font, size, maxw):
    while size > 4 and c.stringWidth(text, font, size) > maxw:
        size -= 0.25
    return size


def draw_key(c, x, y, u, kind, tap, hold, fill, hold_color, held=False,
             layer_key=None):
    pad = u * 0.06
    w = h = u - 2 * pad
    x0, y0 = x + pad, y - u + pad
    rad = u * 0.12
    if kind == "none":
        c.setFillColor(NONE_FILL); c.setStrokeColor(NONE_FILL)
    elif kind == "trans":
        c.setFillColor(TRANS_FILL); c.setStrokeColor(HexColor("#dddddd"))
    elif kind == "mod":
        c.setFillColor(MOD_FILL); c.setStrokeColor(EDGE)
    else:
        c.setFillColor(white); c.setStrokeColor(EDGE)
    if held:
        c.setFillColor(fill); c.setStrokeColor(hold_color)
    if layer_key:  # layer-tap on base: tint with target layer colour
        c.setFillColor(HexColor(LAYERS[layer_key][1]))
        c.setStrokeColor(HexColor(LAYERS[layer_key][2]))
    c.setLineWidth(1.6 if held else 0.6)
    c.roundRect(x0, y0, w, h, rad, stroke=1, fill=1)

    cx = x0 + w / 2
    if held:
        c.setFillColor(hold_color)
        s = fit(c, "HELD", "B", u * 0.22, w * 0.85)
        c.setFont("B", s)
        c.drawCentredString(cx, y0 + h / 2 - s * 0.35, "HELD")
        return
    if kind in ("none", "trans"):
        return
    has_hold = bool(hold)
    main_y = y0 + h * (0.56 if has_hold else 0.5)
    words = tap.split(" ")
    base_size = u * (0.36 if len(tap.replace(" ", "")) <= 2 else 0.22)
    c.setFillColor(INK)
    if len(words) == 2 and c.stringWidth(tap, "U", base_size) > w * 0.86:
        s = min(fit(c, words[0], "U", base_size, w * 0.86),
                fit(c, words[1], "U", base_size, w * 0.86))
        c.setFont("U", s)
        c.drawCentredString(cx, main_y + s * 0.15, words[0])
        c.drawCentredString(cx, main_y - s * 0.95, words[1])
    else:
        s = fit(c, tap, "U", base_size, w * 0.86)
        c.setFont("U", s)
        c.drawCentredString(cx, main_y - s * 0.35, tap)
    if has_hold:
        hc = HexColor(LAYERS[layer_key][2]) if layer_key else MUTED
        s = fit(c, hold, "U", u * 0.16, w * 0.9)
        c.setFillColor(hc)
        c.setFont("U", s)
        c.drawCentredString(cx, y0 + h * 0.1, hold)


def draw_layer(c, layers, order, idx, ox, oy, u, title=True):
    """Draw layer idx with top-left origin at (ox, oy)."""
    key = order[idx]
    name, fill, accent = LAYERS[key]
    fill, accent = HexColor(fill), HexColor(accent)
    # which base key activates this layer?
    held_pos = {i for i, b in enumerate(layers[0])
                if b[0] == "&lt" and b[1] == key}
    if key == "BUTTON":
        held_pos = {i for i, b in enumerate(layers[0])
                    if b[0] == "&lt" and b[1] == "BUTTON"}
    if title:
        how = ""
        if held_pos:
            b = layers[0][min(held_pos)]
            tap = keyname(b[2])
            others = [keyname(layers[0][p][2]) for p in sorted(held_pos)]
            how = "hold " + " or ".join(others)
        c.setFillColor(accent)
        c.roundRect(ox, oy - u * 0.42, u * 0.42, u * 0.42, u * 0.08, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("B", u * 0.28)
        c.drawCentredString(ox + u * 0.21, oy - u * 0.32, str(idx))
        c.setFillColor(INK)
        c.setFont("B", u * 0.34)
        c.drawString(ox + u * 0.58, oy - u * 0.34, name)
        if how:
            c.setFillColor(MUTED)
            c.setFont("R", u * 0.22)
            c.drawString(ox + u * 0.58 + c.stringWidth(name, "B", u * 0.34) + u * 0.2,
                         oy - u * 0.33, how)
        oy -= u * 0.6
    for i, b in enumerate(layers[idx]):
        if i == 30:  # unused left encoder slot
            continue
        kind, tap, hold, lk = describe(b)
        if idx == 0 and i in (11, 23, 37):
            tap = {"-": "- _", "'": "' \""}.get(tap, tap)
        x, y = POS[i] if i != 31 else (6 + HALF_GAP / 2 - 0.5, 1.5)
        px, py = ox + x * u, oy - y * u
        if i == 31:
            # right encoder: round knob
            r = u * 0.42
            c.setStrokeColor(EDGE); c.setLineWidth(0.6)
            c.setFillColor(TRANS_FILL if kind in ("trans", "none") else white)
            c.circle(px + u / 2, py - u / 2, r, stroke=1, fill=1)
            c.setFillColor(MUTED)
            s = u * 0.14
            c.setFont("U", s)
            c.drawCentredString(px + u / 2, py - u / 2 + s * 0.6, "Vol −/+")
            if tap:
                c.setFillColor(INK)
                c.setFont("U", s * 1.1)
                c.drawCentredString(px + u / 2, py - u / 2 - s * 0.9, "press: " + tap)
            continue
        draw_key(c, px, py, u, kind, tap, hold, fill, accent,
                 held=(i in held_pos and idx != 0), layer_key=lk)
    return oy - HEIGHT_U * u


# ---------------------------------------------------------------- pages

PAGE = landscape(letter)
M = 36  # margin


def header(c, text, sub=None):
    W, H = PAGE
    c.setFillColor(INK)
    c.setFont("B", 20)
    c.drawString(M, H - M - 14, text)
    if sub:
        c.setFillColor(MUTED)
        c.setFont("R", 10)
        c.drawString(M, H - M - 30, sub)


def footer(c, n):
    W, H = PAGE
    c.setFillColor(MUTED)
    c.setFont("R", 8)
    c.drawString(M, M - 14, "Corne XIAO v2 · Miryoku (Colemak) · ZMK")
    c.drawRightString(W - M, M - 14, str(n))


def para(c, x, y, lines, size=11, lead=1.45, maxw=None):
    for ln in lines:
        bold = ln.startswith("**")
        font = "B" if bold else "U"
        ln = ln.strip("*")
        c.setFont(font, size)
        c.setFillColor(INK)
        c.drawString(x, y, ln)
        y -= size * lead
    return y


def page_base(c, order, layers):
    W, H = PAGE
    header(c, "Miryoku on the Corne",
           "Every layer is held by a thumb on the opposite hand from the keys it gives you.")
    u = (W - 2 * M) / WIDTH_U
    u = min(u, 54)
    ox = (W - WIDTH_U * u) / 2
    bottom = draw_layer(c, layers, order, 0, ox, H - M - 46, u)

    # Legend: thumb -> layer
    y = bottom - 14
    col_w = (W - 2 * M) / 3
    x1, x2, x3 = M, M + col_w, M + 2 * col_w
    c.setFont("B", 12.5); c.setFillColor(INK)
    c.drawString(x1, y, "Thumbs: tap = key, hold = layer")
    c.drawString(x2, y, "Home-row mods (hold)")
    c.drawString(x3, y, "Learning tips")
    y -= 20
    # thumb list
    yy = y
    for i in range(38, 44):
        b = layers[0][i]
        if b[0] != "&lt":
            continue
        nm, fl, ac = LAYERS[b[1]]
        c.setFillColor(HexColor(fl)); c.setStrokeColor(HexColor(ac))
        c.roundRect(x1, yy - 3, 10, 10, 2, stroke=1, fill=1)
        c.setFillColor(INK); c.setFont("U", 11)
        side = "L" if i < 41 else "R"
        c.drawString(x1 + 16, yy, f"{side} thumb: {keyname(b[2])}  →  {nm}")
        yy -= 16
    c.setFillColor(HexColor(LAYERS["BUTTON"][1])); c.setStrokeColor(HexColor(LAYERS["BUTTON"][2]))
    c.roundRect(x1, yy - 3, 10, 10, 2, stroke=1, fill=1)
    c.setFillColor(INK)
    c.drawString(x1 + 16, yy, "Z or /  →  Button (clipboard + clicks)")

    para(c, x2, y, [
        "Left:   A Ctrl   R Opt   S Cmd   T Shift",
        "Right:  O Ctrl   I Opt   E Cmd   N Shift",
        "X and .  →  AltGr (right Option)",
        "A mod only fires with a key on the",
        "other hand (or a thumb), so rolls",
        "on one hand stay as letters.",
    ])
    para(c, x3, y, [
        "Mods: hold mod, then tap the key on",
        "  the other hand (Cmd+C = hold S, tap C).",
        "Layers: thumb down first, then keys.",
        "Numbers = right thumb Bksp + left hand.",
        "Arrows = hold Space, then N E I O.",
        "Outer columns: Tab, Bksp, Ctrl | - _, ' \", Shift.",
        "Set macOS input to ABC / U.S., not Colemak.",
    ])


def page_overview(c, order, layers):
    W, H = PAGE
    header(c, "All layers at a glance")
    cols, rows = 2, 4
    gx, gy = 22, 6
    cell_w = (W - 2 * M - gx) / cols
    top = H - M - 30
    cell_h = (top - M - gy * (rows - 1)) / rows
    u = min(cell_w / WIDTH_U, cell_h / (HEIGHT_U + 0.6))
    for idx in range(len(order)):
        r, col = divmod(idx, cols)
        ox = M + col * (cell_w + gx) + (cell_w - WIDTH_U * u) / 2
        oy = top - r * (cell_h + gy)
        draw_layer(c, layers, order, idx, ox, oy, u)


def page_pair(c, order, layers, idxs, notes=None):
    W, H = PAGE
    u = min((W - 2 * M) / WIDTH_U, (H - 2 * M - 30) / (2 * (HEIGHT_U + 0.6)))
    ox = (W - WIDTH_U * u) / 2
    oy = H - M
    for idx in idxs:
        oy = draw_layer(c, layers, order, idx, ox, oy, u) - 10
    if notes:
        c.setFont("B", 12); c.setFillColor(INK)
        c.drawString(ox, oy - 8, notes[0])
        para(c, ox, oy - 28, notes[1:], size=10.5)


def main(keymap, out):
    order, layers = parse(keymap)
    assert len(order) == len(layers)
    c = canvas.Canvas(out, pagesize=PAGE)
    c.setTitle("Miryoku Corne cheat sheet")
    n = 1
    page_base(c, order, layers); footer(c, n); c.showPage(); n += 1
    page_overview(c, order, layers); footer(c, n); c.showPage(); n += 1
    rest = list(range(1, len(order)))
    groups = [rest[i:i + 2] for i in range(0, len(rest), 2)]
    for g in groups:
        notes = None
        if len(g) == 1:
            notes = ["Reading the diagrams",
                     "HELD  = the thumb (or key) you are holding to reach this layer.",
                     "Grey key  = does nothing on this layer.",
                     "Faint key  = falls through to the base layer (e.g. outer-column extras).",
                     "Small text at the bottom of a key  = what it does when held.",
                     "Boot (tap twice)  = enter the bootloader to flash new firmware."]
        page_pair(c, order, layers, g, notes); footer(c, n); c.showPage(); n += 1
    c.save()


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    args = sys.argv[1:]
    keymap = args[0] if len(args) > 0 else root / "boards/shields/corne_xiao_v2/corne_xiao_v2.keymap"
    out = args[1] if len(args) > 1 else root / "docs/miryoku-cheatsheet.pdf"
    main(str(keymap), str(out))
    print(f"wrote {out}")
