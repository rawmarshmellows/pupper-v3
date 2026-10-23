---
term: PLC (Programmable Logic Controller)
created: 2026-03-29
---

> **Related:** [[learning/notes/micro-context/push-pull-vs-open-drain]] | [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]]

# PLC (Programmable Logic Controller)

> **See also:** [[quick-context/plc-vs-software]] | [[quick-context/preempt-rt-ros2-plc-replacement]] | [[quick-context/pcb-printed-circuit-board]]

**[[learning/notes/quick-context/capacitance|Definition]]:** A PLC is a ruggedized industrial computer purpose-built to control factory machinery in real time. It contains a CPU, [[learning/notes/quick-context/plc-vs-software|I/O modules]] for sensors and actuators, [[learning/notes/quick-context/d-flip-flop|power]] conditioning, watchdog timers, and a scan-cycle engine that reads inputs, executes user logic ([[learning/notes/quick-context/plc-vs-software|ladder logic]] or structured [[learning/notes/quick-context/how-source-code-is-stored|text]]), and writes outputs in a deterministic 1-50ms loop — all housed in an electrically isolated, vibration-tolerant enclosure with safety certification.

## How It Works

- A **scan-cycle engine** reads all inputs, runs [[learning/notes/quick-context/capacitance|the]] user program, and [[learning/notes/quick-context/firmware|updates]] all outputs in a fixed deterministic loop (1-50ms), with [[learning/notes/quick-context/code-to-gates-and-bootstrapping|hardware]] watchdogs that force outputs to a safe state if anything stalls.
- PLCs are assembled from PCBs, power supplies, I/O modules, and a ruggedized enclosure — the PCB inside carries the CPU, [[learning/notes/quick-context/bare-minimal-data-storage-circuit|memory]], and communication chips, just as in any electronic device.
- PLCs add industrial hardening [[learning/notes/quick-context/pupper-lab5-neural-controller|on top]] of a standard CPU: wide temperature range, vibration [[learning/notes/quick-context/cnc-machining|tolerance]], electrical [[learning/notes/quick-context/pupper-brain|isolation]], and [[learning/notes/quick-context/plc-vs-software|fail-safe]] I/O.
- Programming uses domain-specific [[learning/notes/quick-context/firmware|languages]] (ladder logic, structured text, [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|function]] block diagrams) rather than [[learning/notes/quick-context/singular-value-decomposition|general]]-purpose code, making them accessible to electricians and process engineers.

## Common Confusions

- **PLC vs CPU (device vs [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|component]]):** A CPU is a general-purpose chip that executes instructions. A PLC is a complete industrial computer that *contains* a CPU plus I/O, power conditioning, and safety hardware. Comparing them is like comparing a car to its engine — [[learning/notes/quick-context/ram-addressing-decoder|one]] contains the other.
- **PLC vs PCB (controller vs [[learning/notes/quick-context/flip-chip|substrate]]):** A PCB is a fiberglass-and-copper substrate that physically connects [[learning/notes/quick-context/tensor|components]]. A PLC *contains* PCBs as internal wiring. Comparing them is like comparing a car to metal — one is a material used to build the other.
- **PLC vs Bare Metal / RTOS (industrial computer vs MCU approaches):** Bare metal runs code directly on a [[learning/notes/micro-context/microcontroller|microcontroller]] with no OS (sub-microsecond response). An RTOS adds a [[learning/notes/quick-context/data-bus-and-arbitration|priority]]-based scheduler (~10-100us overhead). A PLC is a different class of device entirely — a self-contained industrial computer with safety certification and fail-safe behavior. Pupper uses bare metal / RTOS on an STM32; factories use PLCs where failures [[learning/notes/quick-context/embedded-communication-protocols|can]] kill people.

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

**Key insight:** A PLC is [[learning/notes/micro-context/can-bus-termination|not]] a chip or a board — it is a complete, safety-certified industrial computer; confusions arise because people compare it against its own internal components (CPU, PCB) or against the bare-metal/RTOS approaches used in non-industrial robotics like Pupper.
