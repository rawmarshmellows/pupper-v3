---
term: PLC (Programmable Logic Controller)
created: 2026-03-29
---
> **Related:** [[micro-context/eeprom]] | [[quick-context/can-bus|CAN Bus (Controller Area Network)]] | [[quick-context/pupper-lab5-neural-controller]] | [[quick-context/pwm-controller-circuit]]

# PLC (Programmable Logic Controller)

> **See also:** [[quick-context/plc-vs-software]] | [[quick-context/preempt-rt-ros2-plc-replacement]] | [[quick-context/pcb-printed-circuit-board]]

**Definition:** A PLC is a ruggedized industrial computer purpose-built to control factory machinery in real time. It contains a CPU, I/O modules for sensors and actuators, power conditioning, watchdog timers, and a scan-cycle engine that reads inputs, executes user logic (ladder logic or structured text), and writes outputs in a deterministic 1-50ms loop — all housed in an electrically isolated, vibration-tolerant enclosure with safety certification.

## How It Works

- A **scan-cycle engine** reads all inputs, runs the user program, and updates all outputs in a fixed deterministic loop (1-50ms), with hardware watchdogs that force outputs to a safe state if anything stalls.
- PLCs are assembled from PCBs, power supplies, I/O modules, and a ruggedized enclosure — the PCB inside carries the CPU, memory, and communication chips, just as in any electronic device.
- PLCs add industrial hardening on top of a standard CPU: wide temperature range, vibration tolerance, electrical isolation, and fail-safe I/O.
- Programming uses domain-specific languages (ladder logic, structured text, function block diagrams) rather than general-purpose code, making them accessible to electricians and process engineers.

## Common Confusions

- **PLC vs CPU (device vs component):** A CPU is a general-purpose chip that executes instructions. A PLC is a complete industrial computer that *contains* a CPU plus I/O, power conditioning, and safety hardware. Comparing them is like comparing a car to its engine — one contains the other.
- **PLC vs PCB (controller vs [[quick-context/substrate-ic-packaging|substrate]]):** A PCB is a fiberglass-and-copper substrate that physically connects components. A PLC *contains* PCBs as internal wiring. Comparing them is like comparing a car to metal — one is a material used to build the other.
- **PLC vs Bare Metal / RTOS (industrial computer vs MCU approaches):** Bare metal runs code directly on a [[micro-context/microcontroller|microcontroller]] with no OS (sub-microsecond response). An RTOS adds a priority-based scheduler (~10-100us overhead). A PLC is a different class of device entirely — a self-contained industrial computer with safety certification and fail-safe behavior. Pupper uses bare metal / RTOS on an STM32; factories use PLCs where failures can kill people.

```
THREE WAYS PEOPLE CONFUSE PLCs:

1. PLC vs CPU (device vs component)
   ┌─────────────────────────┐
   │  ┌───┐                  │
   │  │CPU│  Power  Comms    │    CPU is inside the PLC
   │  └───┘  Supply Module   │    like an engine is inside a car
   │  IN: ● ● ● ●  OUT: ○ ○ │
   └─────────────────────────┘

2. PLC vs PCB (controller vs substrate)
   ┌─────────────────────────┐
   │  ┌─────────────────┐    │
   │  │ ═══ □ ▓▓ ═══ ○○ │    │    PCB is inside the PLC
   │  │ copper on board  │    │    like metal is inside a car
   │  └─────────────────┘    │
   └─────────────────────────┘

3. PLC vs Bare Metal / RTOS (industrial computer vs MCU approaches)
   Bare Metal       RTOS            PLC
   ┌──────────┐  ┌──────────┐  ┌──────────────────┐
   │ main()   │  │ Tasks +  │  │ Scan-cycle engine │
   │ + ISRs   │  │Scheduler │  │ Watchdog + I/O    │
   │ (STM32)  │  │ (STM32)  │  │ Safety cert (SIL) │
   └──────────┘  └──────────┘  └──────────────────┘
   ~μs            ~10-100μs     ~1-50ms scan cycle
   ◄── Pupper ──►              ◄── Factories ──►
```

**Key insight:** A PLC is not a chip or a board — it is a complete, safety-certified industrial computer; confusions arise because people compare it against its own internal components (CPU, PCB) or against the bare-metal/RTOS approaches used in non-industrial robotics like Pupper.
