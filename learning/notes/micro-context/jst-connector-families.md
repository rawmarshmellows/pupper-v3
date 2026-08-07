---
term: JST Connector Families
created: 2026-03-25
updated: 2026-03-27
---

> **Related:** [[quick-context/dupont-jumper-wires]] | [[quick-context/qwiic-stemma-qt-i2c]] | [[quick-context/soldering]] | [[quick-context/usb-peripheral-hardware]]

# JST Connector Families

> **See also:** [[quick-context/pupper-bom-control-board]]

**Definition:** JST (Japan Solderless Terminal) makes dozens of wire-to-board connector series, each identified by a 2-3 letter code. The series determines pitch, current rating, locking, and mounting style. "MX 1.25mm" is **not** an official JST series -- it's a misnomer for generic 1.25mm connectors (likely Molex PicoBlade clones). The real JST 1.25mm connector is the **GH** series. **SH** (1.0mm) is official and genuine.

## How It Works

- Each JST series defines a specific pin pitch (distance between contacts), which determines the connector's size, current capacity, and compatible housings.
- The wire-side housing crimps onto pre-stripped wires and snaps onto the board-side header (through-hole or SMT).
- Locking series (GH, XH, VH) have a plastic tab that clicks over a ridge on the header, requiring deliberate release — non-locking series rely on friction alone.

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

**Key insight:** "JST" is a manufacturer, not a connector type -- saying "JST connector" without the series code is like saying "I need a Molex." The [[quick-context/pupper-bom-control-board|Pupper control board]] uses JST SH (BM07B-SRSS) and PH series connectors.
