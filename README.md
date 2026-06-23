# Corne XIAO v2 — Keymap Reference

6 layers: **Base**, **Lower**, **Raise**, **Macro**, **Extra2** (reserved), **Mouse**.
Encoders on both halves: volume up/down (turn) · see per-layer notes for button actions.

---

## Layer 0 — Base

```
┌────────┬─────┬─────┬─────┬─────┬─────┐                    ┌─────┬─────┬─────┬─────┬─────┬──────┐
│  TAB   │  Q  │  W  │  E  │  R  │  T  │                    │  Y  │  U  │  I  │  O  │  P  │  -   │
├────────┼─────┼─────┼─────┼─────┼─────┤                    ├─────┼─────┼─────┼─────┼─────┼──────┤
│  BKSP  │ A/⌘ │ S/⌥ │ D/⌃ │ F/⇧ │  G  │                    │  H  │ J/⇧ │ K/⌃ │ L/⌥ │ ;/⌘ │  '   │
├────────┼─────┼─────┼─────┼─────┼─────┼────────┬───────────┼─────┼─────┼─────┼─────┼─────┼──────┤
│  CTRL  │  Z* │  X  │  C  │  V  │  B  │  [enc] │  [MUTE]   │  N  │  M  │  ,  │  .  │  /  │ SHFT │
└────────┴─────┴─────┼─────┼─────┼─────┼────────┴───────────┼─────┼─────┼─────┼─────┴─────┴──────┘
                     │ GUI │ LWR │SHFT │                     │ SPC │ RSE │ RET │
                     └─────┴─────┴─────┘                     └─────┴─────┴─────┘
```

- **LWR** = hold to activate Lower · **RSE** = hold to activate Raise
- **Z\*** = tap for Z · hold to activate Mouse layer (left pinky holds, right hand moves + clicks)
- Home row keys are dual-function: **tap** = letter, **hold** = modifier (see below)

---

## Home Row Mods

Hold the key for the modifier. Tap normally for the letter.
Tapping term: **280 ms** — hold longer than this to trigger the modifier.

```
┌─────┬──────────┐     ┌─────┬──────────┐
│ KEY │ HOLD     │     │ KEY │ HOLD     │
├─────┼──────────┤     ├─────┼──────────┤
│  A  │ ⌘  GUI  │     │  J  │ ⇧  SHIFT │
│  S  │ ⌥  OPT  │     │  K  │ ⌃  CTRL  │
│  D  │ ⌃  CTRL │     │  L  │ ⌥  OPT   │
│  F  │ ⇧  SHIFT│     │  ;  │ ⌘  GUI   │
└─────┴──────────┘     └─────┴──────────┘
  LEFT HAND               RIGHT HAND
```

**Tips:**
- Roll keys quickly (under 280 ms) — letters will register, not modifiers
- If a modifier fires accidentally, increase `tapping-term-ms` in the keymap
- `require-prior-idle-ms = 150` prevents mod triggers during fast typing bursts

---

## Layer 1 — Lower

Hold **LWR**.

```
┌────────┬──────┬──────┬──────┬──────┬──────┐                    ┌──────┬──────┬──────┬──────┬──────┬──────┐
│  ESC   │  !   │  @   │  #   │  $   │  %   │                    │  ^   │  &   │  *   │  (   │  )   │ BKSP │
├────────┼──────┼──────┼──────┼──────┼──────┤                    ├──────┼──────┼──────┼──────┼──────┼──────┤
│  BKSP  │  1   │  2   │  3   │  4   │  5   │                    │  6   │  7   │  8   │  9   │  0   │  F12 │
├────────┼──────┼──────┼──────┼──────┼──────┼────────┬───────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│  CTRL  │  F1  │  F2  │  F3  │  F4  │  F5  │  [enc] │  [BOOT]   │  \   │  `   │  =   │  {   │  }   │  F11 │
└────────┴──────┴──────┼──────┼──────┼──────┼────────┴───────────┼──────┼──────┼──────┼──────┴──────┴──────┘
                       │ ---- │ (hd) │ SHFT │                    │ SPC  │ MAC  │ ---- │
                       └──────┴──────┴──────┘                    └──────┴──────┴──────┘
```

- **MAC** = hold (with LWR still held) to activate Macro layer
- Right encoder button: **bootloader**

---

## Layer 2 — Raise

Hold **RSE**.

```
┌────────┬────────┬────────┬────────┬────────┬────────┐                    ┌──────┬──────┬──────┬───────┬──────┬──────┐
│  TAB   │   1    │   2    │   3    │   4    │   5    │                    │  6   │  7   │  UP  │   9   │  0   │ BKSP │
├────────┼────────┼────────┼────────┼────────┼────────┤                    ├──────┼──────┼──────┼───────┼──────┼──────┤
│  CTRL  │ BT_CLR │ BT_PRV │ BT_NXT │  ----  │  ----  │                    │  -   │ LEFT │ DOWN │ RIGHT │  \   │  `   │
├────────┼────────┼────────┼────────┼────────┼────────┼────────┬───────────┼──────┼──────┼──────┼───────┼──────┼──────┤
│  SHFT  │  ----  │  ----  │  ----  │  ----  │ [BOOT] │  [enc] │  [BOOT]   │  =   │  +   │  {   │  }    │  \   │[BOOT]│
└────────┴────────┴────────┼────────┼────────┼────────┼────────┴───────────┼──────┼──────┼──────┼───────┴──────┴──────┘
                           │  ----  │  ----  │  SHFT  │                    │ SPC  │ (hd) │ ---- │
                           └────────┴────────┴────────┘                    └──────┴──────┴──────┘
```

- **BT_CLR** = clear paired device · **BT_PRV/NXT** = cycle Bluetooth profiles
- Arrow keys: vim-style navigation on right hand
- **[BOOT]** appears at: B key (left), right encoder button, right SHIFT (right) — any enters bootloader

---

## Layer 3 — Macro

Hold **LWR**, then hold **MAC** (right thumb middle).

```
┌──────┬──────┬──────┬──────┬──────┬──────┐                    ┌──────┬────────┬──────┬──────┬──────┬──────┐
│ ---- │ ---- │ ---- │ ---- │ ---- │ ---- │                    │ ---- │  ----  │ ---- │ ---- │ ---- │ ---- │
├──────┼──────┼──────┼──────┼──────┼──────┤                    ├──────┼────────┼──────┼──────┼──────┼──────┤
│ ---- │ ---- │ ---- │ ---- │ ---- │ ---- │                    │ ---- │ ⌃⇧⌘ 4  │ ---- │ ---- │ ---- │ ---- │
├──────┼──────┼──────┼──────┼──────┼──────┼────────┬───────────┼──────┼────────┼──────┼──────┼──────┼──────┤
│ ---- │ ---- │ ---- │ ---- │ ---- │ ---- │  [enc] │   [enc]   │ ---- │  ----  │ ---- │ ---- │ ---- │ ---- │
└──────┴──────┴──────┼──────┼──────┼──────┼────────┴───────────┼──────┼────────┼──────┼──────┴──────┴──────┘
                     │ ---- │ (hd) │ SHFT │                    │ SPC  │  (hd)  │ ---- │
                     └──────┴──────┴──────┘                    └──────┴────────┴──────┘
```

- **⌃⇧⌘4** = macOS area screenshot — on the `J` key position

---

## Layer 5 — Mouse

Hold **Z\*** (left pinky). Right hand handles all movement and clicks.

```
┌──────┬──────┬──────┬──────┬──────┬──────┐                    ┌──────┬──────┬──────┬──────┬──────┬──────┐
│ ---- │ ---- │ ---- │ ---- │ ---- │ ---- │                    │ ---- │ ---- │  ↑   │ ---- │ ---- │ ---- │
├──────┼──────┼──────┼──────┼──────┼──────┤                    ├──────┼──────┼──────┼──────┼──────┼──────┤
│ ---- │ ---- │ ---- │ ---- │ ---- │ ---- │                    │ ---- │  ←   │  ↓   │  →   │ ---- │ ---- │
├──────┼──────┼──────┼──────┼──────┼──────┼────────┬───────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ ---- │ ---- │ ---- │ ---- │ ---- │ ---- │  [enc] │  [enc]    │ ---- │ ---- │ ---- │ ---- │ ---- │ ---- │
└──────┴──────┴──────┼──────┼──────┼──────┼────────┴───────────┼──────┼──────┼──────┼──────┴──────┴──────┘
                     │ ---- │ ---- │ (hd) │                    │ LCLK │ RCLK │ MCLK │
                     └──────┴──────┴──────┘                    └──────┴──────┴──────┘
```

- Mouse movement: **I** = up · **J** = left · **K** = down · **L** = right
- **LCLK** = left click · **RCLK** = right click · **MCLK** = middle click

---

## Combos

| Keys | Action |
|------|--------|
| Q + W | Studio Unlock |

---

## Legend

| Symbol | Meaning |
|--------|---------|
| `----` | Transparent — passes through to layer below |
| `(hd)` | This key is being held to reach this layer |
| `KEY/⌘` | Tap = letter, Hold = modifier |
| `[enc]` | Encoder button action |
| `[BOOT]` | Enter bootloader (for flashing firmware) |
| `[MUTE]` | Mute media |
