---
term: Bare Metal vs RTOS vs PLC
created: 2026-03-25
---

# Bare Metal vs RTOS vs PLC

> **See also:** [[quick-context/plc-vs-software]] | [[quick-context/preempt-rt]]

**Definition:** Three distinct approaches to real-time control, ordered by increasing abstraction and industrial hardening. **Bare metal** runs code directly on a [[micro-context/stm32-microcontroller|microcontroller]] with no OS — maximum speed, minimum overhead. An **RTOS** (Real-Time Operating System, e.g., FreeRTOS) adds priority-based task scheduling with deterministic context switching on the same microcontroller. A **[[quick-context/plc-vs-software|PLC]]** is a complete ruggedized industrial computer with its own CPU, I/O modules, watchdog timers, and safety certification — a different class of device entirely.

```
SPECTRUM OF REAL-TIME CONTROL:

  Bare Metal          RTOS              PLC
  (no OS)          (lightweight OS)  (industrial computer)
  ┌──────────┐     ┌──────────┐     ┌──────────────────┐
  │Your code │     │ Task A   │     │ Scan cycle engine │
  │    ↓     │     │ Task B   │     │ Ladder logic / ST │
  │ Hardware │     │Scheduler │     │ Watchdog + I/O    │
  │ (STM32)  │     │ Hardware │     │ Safety cert (SIL) │
  └──────────┘     └──────────┘     └──────────────────┘
  ~μs latency      ~10-100μs         ~1-50ms scan cycle
  No safety net    Priority-based    Fail-safe by design

  ◄── Pupper uses this ──►          ◄── Factories use this
```

**Key insight:** Bare metal and RTOS both run on microcontrollers (like the STM32 in Pupper) and give you raw speed for robotics — but they lack the safety certification, electrical hardening, and guaranteed fail-safe behavior that make PLCs mandatory in industrial settings where failures kill people.
