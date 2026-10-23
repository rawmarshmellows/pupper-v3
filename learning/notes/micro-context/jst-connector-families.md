---
term: JST Connector Families
created: 2026-03-25
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]

# JST Connector Families

> **See also:** [[quick-context/pupper-bom-control-board]]

**[[learning/notes/quick-context/capacitance|Definition]]:** JST (Japan Solderless [[learning/notes/quick-context/from-vacuum-tubes-to-coding-on-screens|Terminal]]) makes dozens of wire-to-board [[learning/notes/quick-context/qwiic-stemma-qt-i2c|connector]] [[learning/notes/quick-context/parallel-vs-series-voltage|series]], each identified by a 2-3 letter code. [[learning/notes/quick-context/capacitance|The]] series determines [[learning/notes/quick-context/bga-ball-grid-array|pitch]], [[learning/notes/quick-context/capacitance|current]] rating, locking, [[learning/notes/micro-context/push-pull-vs-open-drain|and]] mounting style. "MX 1.25mm" is **[[learning/notes/micro-context/can-bus-termination|not]]** an official JST series -- it's a misnomer for generic 1.25mm connectors (likely Molex PicoBlade clones). The real JST 1.25mm connector is the **GH** series. **SH** (1.0mm) is official and genuine.

## How It Works

- Each JST series defines a specific pin pitch ([[learning/notes/quick-context/embedded-communication-protocols|distance]] between contacts), which determines the connector's size, current capacity, and compatible housings.
- The wire-side [[learning/notes/quick-context/dupont-jumper-wires|housing]] crimps onto pre-stripped [[learning/notes/quick-context/uart|wires]] and snaps onto the board-side header ([[learning/notes/quick-context/common-ic-packages|through-hole]] or SMT).
- Locking series (GH, XH, VH) have a plastic [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|tab]] that clicks over a ridge on the header, requiring deliberate [[learning/notes/micro-context/push-pull-vs-open-drain|release]] — non-locking series rely on friction alone.

```
Pitch    Series   Lock?  Current  Common Use
─────────────────────────────────────────────────
1.0mm    SH       No     1A       FPV, Qwiic, laptops (SMT only)
1.25mm   GH       Yes    1A       Robotics, sensors (not "MX"!)
1.5mm    ZH       No     1A       3D printers, small electronics
2.0mm    PH       No     2A       LiPo batteries, stepper motors
2.0mm    PA       Yes    3A       Locking alt to PH
2.5mm    XH       Yes    3A       RC battery balancing
2.5mm    EH       No     3A       Low-profile wire-to-board
3.96mm   VH       Yes    10A      Appliances, high-current power

Wire-to-wire: SM (2.5mm), RCY (2.5mm, 2-pin only)

Lock = plastic tab on housing that snaps over a ridge on the header.
Must press tab to disconnect. Without it, friction alone holds the plug.

  LOCKING (GH, XH, VH...)       NON-LOCKING (SH, PH, ZH...)
  ┌──────────┐                   ┌──────────┐
  │ ┌─tab──┐ │ ◄─ press to       │          │
  │ └──┬───┘ │    release        │          │ ◄─ just pull
  │ ═══╪════ │                   │ ════════ │
  └────┼─────┘                   └──────────┘
       ▼ snaps over ridge
```

**Key insight:** "JST" is a manufacturer, not a connector [[learning/notes/quick-context/bjt-specifications|type]] -- saying "JST connector" without the series code is like saying "I need a Molex." The [[quick-context/pupper-bom-control-board|Pupper control board]] uses [[learning/notes/quick-context/dupont-jumper-wires|JST SH]] (BM07B-SRSS) and PH series connectors.
