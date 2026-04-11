---
term: Clock Source
created: 2026-03-27
---

# Clock Source
> **Related:** [[micro-context/clock-speed]] | [[quick-context/clock-sources-and-timing]] | [[micro-context/ceramic-resonator]] | [[micro-context/stm32-microcontroller]] | [[quick-context/rc-oscillator]]

> **See also:** [[micro-context/ceramic-resonator]] | [[micro-context/clock-speed]] | [[quick-context/clock-sources-and-timing|Clock Sources and Timing]]

**Definition:** The component or circuit that generates the base frequency reference for a [[micro-context/stm32-microcontroller|microcontroller's]] clock system. On the Pupper v3 board, each STM32's clock source is an external 8 MHz [[micro-context/ceramic-resonator|ceramic resonator]] (HSE), which the on-chip PLL multiplies to the 180 MHz operating frequency.

## How It Works

- The MCU selects one of several clock sources at startup: an internal [[quick-context/rc-oscillator|RC oscillator]] (HSI, ~16 MHz, ±1% accuracy at 25°C but degrades over temperature) or an external crystal/resonator (HSE, higher accuracy).
- The selected source feeds into the PLL (phase-locked loop), which multiplies the frequency up — e.g., $8\text{ MHz} \times 22.5 = 180\text{ MHz}$ for the Pupper's STM32F446.
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

**Key insight:** The external ceramic resonator isn't the MCU's actual operating frequency — it's just a stable reference that the PLL multiplies up. The MCU couldn't run directly at 8 MHz fast enough for 1 kHz motor control; the PLL is what bridges the gap to 180 MHz.
