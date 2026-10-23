---
term: Clock Source
created: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/clock-edges]] | [[learning/notes/micro-context/clock-speed-vs-temperature]] | [[learning/notes/micro-context/clock-speed]] | [[learning/notes/micro-context/push-pull-vs-open-drain]] | [[learning/notes/micro-context/4-wire-kelvin-measurement]]

# Clock Source

> **See also:** [[micro-context/ceramic-resonator]] | [[micro-context/clock-speed]] | [[quick-context/clock-sources-and-timing|Clock Sources and Timing]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/capacitance|The]] [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|component]] or circuit that generates the base frequency [[learning/notes/quick-context/comparator|reference]] for a [[micro-context/stm32-microcontroller|microcontroller's]] [[learning/notes/quick-context/bare-minimal-data-storage-circuit|clock]] system. On the Pupper v3 board, each STM32's [[learning/notes/quick-context/clock-sources-and-timing|clock source]] is an external 8 MHz [[micro-context/ceramic-resonator|ceramic resonator]] (HSE), which the on-chip PLL multiplies to the 180 MHz operating frequency.

## How It Works

- The MCU selects [[learning/notes/quick-context/ram-addressing-decoder|one]] of several clock sources at [[learning/notes/quick-context/firmware|startup]]: an internal [[quick-context/rc-oscillator|RC oscillator]] (HSI, ~16 MHz, ±1% [[learning/notes/quick-context/rc-oscillator|accuracy]] at 25°C but degrades over temperature) or an external crystal/resonator (HSE, higher accuracy).
- The selected [[learning/notes/quick-context/differential-pair|source]] feeds into the PLL (phase-locked loop), which multiplies the frequency up — e.g., $8\[[learning/notes/quick-context/how-source-code-is-stored|text]]{ MHz} \times 22.5 = 180\text{ MHz}$ for the Pupper's STM32F446.
- The PLL output then drives the system clock (SYSCLK), which is further divided down for peripheral buses (APB1 at 45 MHz max, APB2 at 90 MHz max).

```
CLOCK SOURCE → PLL → SYSTEM CLOCK
═══════════════════════════════════════════════

  Internal (HSI)         ┌─────────┐
  16 MHz RC ────────────►│         │
                         │   PLL   │──► SYSCLK (180 MHz)
  External (HSE)    ┌───►│  ×N/÷M  │       │
  8 MHz ceramic ────┘    └─────────┘       ├──► APB1 (÷4 → 45 MHz)
  resonator (X1,X2)                        └──► APB2 (÷2 → 90 MHz)
         ▲
     Pupper uses this
```

**Key insight:** The external [[learning/notes/micro-context/ceramic-resonator|ceramic resonator]] isn't the MCU's actual operating frequency — it's just a stable reference that the PLL multiplies up. The MCU couldn't run directly at 8 MHz [[learning/notes/quick-context/comparator|fast]] enough for 1 kHz motor control; the PLL is [[learning/notes/quick-context/bare-minimal-data-storage-circuit|what]] bridges the gap to 180 MHz.
