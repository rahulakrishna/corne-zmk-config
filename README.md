# Corne Xiao V2 Keymap

6-column Corne on Seeeduino Xiao BLE, running ZMK v0.3. Right side has a rotary encoder for volume.

**[Miryoku](https://github.com/manna-harbour/miryoku) layout (Colemak), optimised for the Corne.** The core 36 keys (3×5 + 3 thumbs per half) are canonical Miryoku: 8 layers, each activated by a thumb (or the Z / `/` keys for Button) on the **opposite** hand from the layer's content. The Corne's outer columns hold convenience keys (Tab, BkSp, Ctrl, `-`, `'`, Shift), all of which are also reachable from the core 36.

Clipboard keys use macOS shortcuts (⌘Z / ⌘X / ⌘C / ⌘V / ⇧⌘Z).

---

## Thumb cluster

```
MEDIA/⎋  NAV/⎵  MOUSE/⇥      SYM/↵  NUM/⌫  FUN/⌦
```

Tap = the labeled key. Hold = the layer. Tap-then-hold repeats the tap key (e.g. hold Space/Backspace to auto-repeat).

---

## Layers

### 0 — base

```
Tab   Q      W      F      P      G              J      L      U      Y      '      - _
BkSp  GUI/A  ALT/R  CTL/S  SFT/T  D              H      SFT/N  CTL/E  ALT/I  GUI/O  ' "
Ctrl  BTN/Z  AGR/X  C      V      B   [encoder]  K      M      ,      AGR/.  BTN//  Shift
             MED/⎋  NAV/⎵  MSE/⇥                 SYM/↵  NUM/⌫  FUN/⌦
```

- Classic Colemak, done in the firmware: **set macOS's input source to ABC / U.S., not Colemak.**
- `'` replaces Colemak's `;` on the top row (Miryoku standard) and is repeated in the right outer column; `;` is on NUM.
- Hold X or `.` for AltGr (right Option on macOS).
- Hold Z or `/` for the Button layer.
- Outer columns (left: Tab, BkSp, Ctrl; right: `-`, `'`, Shift) are Corne-only extras.

---

### 1 — button (hold Z or /)

Clipboard and mouse buttons, mirrored on both hands — usable one-handed alongside the mouse.

```
      Undo   Cut    Copy   Paste  Redo           Redo   Paste  Copy   Cut    Undo
      GUI    ALT    CTL    SFT    ---            ---    SFT    CTL    ALT    GUI
      Undo   Cut    Copy   Paste  Redo           Redo   Paste  Copy   Cut    Undo
             MClk   LClk   RClk                  RClk   LClk   MClk
```

---

### 2 — nav (hold NAV/Space)

```
      Boot²  ---    ---    ---    ---            Redo   Paste  Copy   Cut    Undo
      GUI    ALT    CTL    SFT    ---            CapsW  ←      ↓      ↑      →
      ---    AGR    ---    ---    ---            Ins    Home   PgDn   PgUp   End
             ---    (held) ---                   Ret    BkSp   Del
```

- Arrows on the right home row, N E I O (← ↓ ↑ →)
- Home/PgDn/PgUp/End directly below the matching arrows

---

### 3 — mouse (hold MOUSE/Tab)

```
      Boot²  ---    ---    ---    ---            Redo   Paste  Copy   Cut    Undo
      GUI    ALT    CTL    SFT    ---            ---    M←     M↓     M↑     M→
      ---    AGR    ---    ---    ---            ---    W←     W↓     W↑     W→
             ---    ---    (held)                RClk   LClk   MClk
```

---

### 4 — media (hold MEDIA/Esc)

```
      Boot²  ---    ---    ---    ---            BT 0   BT 1   BT 2   BT 3   BT 4
      GUI    ALT    CTL    SFT    ---            USB/BT Prev   Vol-   Vol+   Next
      ---    AGR    ---    ---    ---            BTClr  ---    ---    ---    ---
             (held) ---    ---                   Stop   Play   Mute
```

---

### 5 — num (hold NUM/BkSp)

```
      [      7      8      9      ]              ---    ---    ---    ---    Boot²
      ;      4      5      6      =              ---    SFT    CTL    ALT    GUI
      `      1      2      3      \              ---    ---    ---    AGR    ---
             .      0      -                     ---    (held) ---
```

---

### 6 — sym (hold SYM/Enter)

Shifted versions of the NUM layer.

```
      {      &      *      (      }              ---    ---    ---    ---    Boot²
      :      $      %      ^      +              ---    SFT    CTL    ALT    GUI
      ~      !      @      #      |              ---    ---    ---    AGR    ---
             (      )      _                     (held) ---    ---
```

---

### 7 — fun (hold FUN/Del)

```
      F12    F7     F8     F9     PrtSc          ---    ---    ---    ---    Boot²
      F11    F4     F5     F6     ScrLk          ---    SFT    CTL    ALT    GUI
      F10    F1     F2     F3     Pause          ---    ---    ---    AGR    ---
             Menu   Spc    Tab                   ---    ---    (held)
```

`Boot²` = double-tap to enter the bootloader (single tap does nothing).

---

## Homerow mods

GACS order (pinky → index): GUI · Alt · Ctrl · Shift on both hands.

| Left | Mod | Right | Mod |
|------|-----|-------|-----|
| A | Cmd (GUI) | O | Cmd (GUI) |
| R | Opt (Alt) | I | Opt (Alt) |
| S | Ctrl | E | Ctrl |
| T | Shift | N | Shift |

Positional `balanced` hold-tap: a left-hand mod only becomes a hold when followed by a right-hand key or any thumb key (and vice versa), so same-hand rolls stay as letters.

- Tap term: 280ms
- Quick-tap: 175ms (tap-then-hold repeats the letter)
- Prior idle: 150ms (no mod if you were typing just before)

---

## Combos

| Keys | Output |
|------|--------|
| Tab + Q (positions 0, 1) | ZMK Studio unlock |

---

## Encoder

| Action | Result |
|--------|--------|
| Rotate (all layers) | Volume up / down |
| Press (base) | Mute |

---

## Printable cheat sheet

[`docs/miryoku-cheatsheet.pdf`](docs/miryoku-cheatsheet.pdf) is generated straight from the keymap. After changing the keymap, regenerate it with:

```sh
pip install reportlab
python3 scripts/cheatsheet.py
```

Uses macOS's bundled Arial fonts.
