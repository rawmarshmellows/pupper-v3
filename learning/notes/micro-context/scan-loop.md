---
term: Scan Loop
created: 2026-04-07
---

> **Related:** [[learning/notes/quick-context/usb-peripheral-hardware]] | [[learning/notes/quick-context/from-vacuum-tubes-to-coding-on-screens]] | [[learning/notes/quick-context/physics-of-writing-data-to-memory]] | [[learning/notes/quick-context/bare-minimal-data-storage-circuit]] | [[learning/notes/quick-context/ros2-architecture]]
# Scan Loop

**Definition:** A firmware routine that rapidly cycles through rows of a **[[learning/notes/micro-context/switch-matrix|switch matrix]]** — a grid of electrical switches wired at the intersections of row and column lines, so each switch is uniquely identified by its (row, col) coordinate — driving each row LOW in turn and reading all columns to detect which switches are closed. Used by keyboard and keypad [[learning/notes/micro-context/stm32-microcontroller|microcontrollers]] to monitor many switches with few GPIO pins.

## How It Works

- The MCU configures row pins as outputs and column pins as inputs (with pull-up resistors so they default HIGH).
- Each iteration drives one row LOW while keeping all other rows HIGH, then reads every column pin — a LOW column means the switch at that (row, col) intersection is closed.
- The loop cycles through all rows every ~1–5 ms, fast enough that no human keypress is missed.
- When a press is detected, the firmware maps the (row, col) position to a [[learning/notes/quick-context/physics-of-writing-data-to-memory|scan code]] via a lookup table stored in flash.

```
GPIO PINS:    Row 0 ──┬────┬────┬──
              Row 1 ──┼────┼────┼──
              Row 2 ──┼────┼────┼──
                      │    │    │
                    Col 0 Col 1 Col 2

SCAN CYCLE (Row 0 active):
  Row 0 → LOW ─────────────────────
  Row 1 → HIGH ────────────────────
  Row 2 → HIGH ────────────────────

  Read columns:
    Col 0 = HIGH → open
    Col 1 = LOW  → KEY PRESSED at (0,1)
    Col 2 = HIGH → open

  Next iteration: Row 1 → LOW, repeat...
```

**Key insight:** An $N \times M$ matrix lets an MCU monitor $N \times M$ switches using only $N + M$ GPIO pins — a 6×14 keyboard matrix monitors 84 keys with just 20 pins.
