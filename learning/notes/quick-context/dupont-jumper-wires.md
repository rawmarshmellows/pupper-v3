---
topic: DuPont Jumper Wires
created: 2026-04-03
---

> **Related:** [[learning/notes/quick-context/voltage]] | [[learning/notes/quick-context/galvanic-cells-batteries]] | [[learning/notes/micro-context/oxidation]] | [[learning/notes/micro-context/microcontroller]] | [[learning/notes/quick-context/soldering]]

# DuPont Jumper Wires

> **TL;DR:** DuPont jumper wires are cheap, solder-free cables with 2.54mm-pitch crimp connectors used to quickly wire up breadboard and [[learning/notes/micro-context/microcontroller|microcontroller]] circuits. They're the universal prototyping cable of hobbyist electronics -- indispensable for experimentation, unreliable for anything permanent.

## The Core Problem

Electronics prototyping requires connecting dozens of components -- sensors, microcontrollers, displays, motors -- without [[learning/notes/quick-context/soldering|soldering]]. You need connections you can make in seconds, rearrange freely, and discard when the design changes. DuPont jumper wires solve this by providing plug-and-play cables that mate with the 0.1" pin headers found on virtually every dev board. Without them, every breadboard experiment would require soldering or expensive connector systems.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **2.54mm pitch** | The 0.1" (100 mil) spacing between adjacent pins -- the universal standard for breadboards, Arduino headers, and Raspberry Pi GPIO |
| **Crimp contact** | The stamped metal pin or socket inside the plastic housing, mechanically squeezed onto the wire rather than soldered |
| **Housing** | The small rectangular plastic shell (nylon 66) that holds crimp contacts; comes in 1P through 20P sizes for single or multi-pin groupings |
| **Gender** | Male (pin) vs female (socket); jumper wires come in M-M, M-F, and F-F combinations depending on what endpoints you're connecting |
| **Mini-PV** | The original Berg Electronics connector design ("Perpetual Virgin" -- named because the contact performed like new even after hundreds of mating cycles) that DuPont acquired in 1972 -- the ancestor of all modern "DuPont" connectors |

<details>
<summary><strong>How It Works</strong> -- Anatomy of a DuPont jumper wire</summary>

A DuPont jumper wire has three parts: wire, crimp contact, and housing.

```
                   FEMALE END                              MALE END
                ┌──────────────┐                     ┌──────────────┐
                │   Housing    │                     │   Housing    │
                │  (Nylon 66)  │                     │  (Nylon 66)  │
                │              │                     │              │
  Wire    ──────┤  ┌────────┐  │      26 AWG         │  ┌────────┐  ├────── Pin
  (26 AWG)      │  │ Socket │  ├─────stranded────────┤  │  Pin   │  │    (0.64mm
  stranded      │  │contact │  │  tinned copper      │  │contact │  │     square)
  tinned Cu     │  └────────┘  │                     │  └────────┘  │
                │              │                     │              │
                └──────────────┘                     └──────────────┘

  CRIMP DETAIL (cross-section):

      Insulation crimp         Conductor crimp
     ┌─────────────┐          ┌─────────────┐
     │  ┌───────┐  │          │  ┌───────┐  │
     │  │  PVC  │  │          │  │ Bare  │  │
     │  │insul. │  │          │  │copper │  │
     │  │       │  │          │  │strands│  │
     │  └───────┘  │          │  └───────┘  │
     └──── ↑ ──────┘          └──── ↑ ──────┘
      Strain relief         Electrical connection
```

**The mating mechanism:** The female socket contains a leaf spring that grips a 0.025" (0.64mm) square male pin through friction alone. There are no latches, clips, or keying features -- the connection is held purely by spring tension against the pin. This is what makes DuPont connectors both easy to use and prone to loosening.

**Ribbon cable construction:** Most jumper wires are sold as 40-wire rainbow ribbon cables that can be peeled apart into any grouping:

```
  40-pin ribbon (peelable):

  ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──────────────────┬──┐
  │R │O │Y │G │B │P │Br│Bk│W │Gy│  ... 30 more ... │R │
  └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──────────────────┴──┘
       ↑         ↑
    Peel apart at any boundary
```

**Housing sizes:** The plastic housing comes in various widths:

```
  1P       2P        3P            4P
  ┌──┐   ┌──┬──┐   ┌──┬──┬──┐   ┌──┬──┬──┬──┐
  │  │   │  │  │   │  │  │  │   │  │  │  │  │
  └──┘   └──┴──┘   └──┴──┴──┘   └──┴──┴──┴──┘
                    ↑
                 3P is standard
                 for RC servos
                 (Signal/VCC/GND)
```

### Wire Specifications

| Parameter | Typical Value |
|-----------|--------------|
| Wire gauge | 26 AWG (pre-made); 22-28 AWG (DIY crimp) |
| Conductor | Stranded tinned copper |
| Insulation | PVC (80$^\circ$C) or silicone (150$^\circ$C) |
| Standard lengths | 10cm, 15cm, 20cm, 30cm |
| Resistance | ~134 $\Omega$/km (~0.054 $\Omega$ per 20cm round trip) |

</details>

<details>
<summary><strong>The Key Tension</strong> -- Convenience vs reliability</summary>

The fundamental tradeoff with DuPont jumper wires is **speed of connection vs quality of connection**.

| Factor | DuPont Jumpers | Soldered / Latched Connectors |
|--------|---------------|-------------------------------|
| Setup time | Seconds | Minutes to hours |
| Reconfigurability | Unlimited | Destructive to change |
| Connection reliability | Poor (friction only) | Excellent |
| Vibration resistance | Very poor | Good to excellent |
| Current capacity | ~1A practical (26 AWG) | Limited only by wire gauge |
| Cost per connection | ~$0.05 | ~$0.10-1.00 |
| Keying / polarity | None | Usually keyed |
| Skill required | None | Soldering or proper crimping |

**The practitioner debate:** When should you graduate from DuPont wires to proper connectors?

- **"Prototype only" camp:** DuPont wires should never leave the bench. Any project that moves past breadboard should use JST, Molex, or soldered connections.
- **"Good enough" camp:** For low-current, low-vibration applications (desktop sensor stations, display projects), DuPont connections with hot glue strain relief work fine permanently.
- **The middle ground:** Use DuPont for signal-level connections (<100mA) in static environments, but always use rated connectors for power delivery and anything that moves.

### Ratings: Datasheet vs Reality

| Parameter | Datasheet (genuine) | Clone practical limit |
|-----------|--------------------|-----------------------|
| Current | 3A | ~1A max, 500mA comfortable |
| Mating cycles | 500+ | 50-100 before loosening |
| Contact resistance | 15-20 m$\Omega$ | 50-200+ m$\Omega$ (variable) |
| [[learning/notes/quick-context/voltage|Voltage]] | 250V AC/DC | Rarely the limiting factor |
| Temperature | -25$^\circ$C to +85$^\circ$C | PVC degrades above 80$^\circ$C |

</details>

<details>
<summary><strong>Concrete Example</strong> -- Wiring a servo to an Arduino</summary>

A typical robotics task: connecting an RC servo motor to an Arduino Uno.

**The servo has a 3-pin male header:**
```
  Servo cable (pre-attached):
  ┌──────────────────────────────┐
  │  Brown (GND)                 │
  │  Red   (VCC, +5V)  ──────────├──┐
  │  Orange (Signal, PWM)        │  │  3-pin DuPont
  └──────────────────────────────┘  │  male header
                                 └──┘
```

**Connection using F-F jumper wires to Arduino headers:**
```
  Servo 3-pin male          F-F Jumper Wires         Arduino Uno
  ┌────────────┐                                    ┌────────────┐
  │ Brown  GND ├──── Black F-F ────────────────────►│ GND        │
  │ Red    VCC ├──── Red F-F ──────────────────────►│ 5V         │
  │ Orange SIG ├──── Orange F-F ───────────────────►│ D9 (PWM)   │
  └────────────┘                                    └────────────┘
```

**Current concern:** A typical hobby servo draws 200-500mA under load, and up to 1-2A at stall. A single 26 AWG DuPont jumper wire on the power line is marginal. For multiple servos (as in a quadruped robot), you should:
1. Power servos from a separate supply, not through the Arduino's 5V pin
2. Use thicker gauge wire (22 AWG or heavier) for the power line
3. Consider XT30 connectors or screw terminals for the main power bus

**Color coding convention:**
| Color | Typical Use |
|-------|-------------|
| Red | VCC / positive supply |
| Black | GND / ground |
| White | Data / signal |
| Yellow | Clock / SCL |
| Blue | SDA / chip select |
| Green | MOSI / TX |
| Orange | MISO / RX |

**The one thing most outsiders get wrong about this is...** that DuPont connectors are a standardized, specified product. They are not. "DuPont connector" is a genericized brand name with no official spec sheet for the clones that dominate the market. Every batch from every factory is slightly different. The original Berg Mini-PV connector is a real, specified product (now sold by Amphenol) -- but it costs roughly 2x as much and is rarely what hobbyists are buying. When you buy a bag of "DuPont jumper wires" from Amazon or AliExpress, you're getting unspecified clones with no guaranteed tolerances.

</details>

<details>
<summary><strong>History</strong> -- Why they're called "DuPont"</summary>

The name traces through decades of corporate acquisitions:

| Year | Event |
|------|-------|
| 1950 | Quentin Berg founds **Berg Electronics** and invents the **Mini-PV contact** ("Perpetual Virgin") -- a crimp connector with a beryllium copper spring achieving 500+ mating cycles |
| 1972 | **E.I. du Pont de Nemours** (DuPont) acquires Berg Electronics for ~$25M. All catalogs rebrand to "DuPont" |
| 1990s | Chinese manufacturers begin producing low-cost clones without the beryllium copper spring or selective gold plating. The "DuPont" name sticks to the clones |
| 1993 | DuPont divests Berg Electronics for $370M |
| 1998 | **FCI** (Framatome Connectors International) acquires Berg |
| 2016 | **Amphenol** acquires FCI. Genuine Mini-PV connectors still manufactured today |

The name persists because the clones flooded the hobbyist market during the 1990s-2000s Arduino revolution, and "DuPont connector" became the de facto generic term -- much like "Band-Aid" for adhesive bandages.

</details>

<details>
<summary><strong>Common Mistakes</strong></summary>

1. **Reversed polarity** -- No keying means VCC and GND can be swapped. This is the #1 way hobbyists destroy sensors and microcontrollers. Always double-check before powering on.

2. **Off-by-one pin errors** -- Plugging a multi-pin connector shifted by one position sends power into signal pins. Mark pin 1 with a dot of paint or tape.

3. **Exceeding current limits** -- Using a single 26 AWG jumper to power a servo motor (stall current 1-2A). The wire heats up, contact resistance increases, and the housing can melt.

4. **Trusting loose connections** -- Intermittent contact from weak spring tension causes phantom bugs: sensors returning random values, I2C failures, serial corruption. When debugging, suspect the physical layer first.

5. **Using pliers to crimp** -- A proper ratcheting crimp tool ($20-30) is essential for reliable DIY cables. Pliers produce inconsistent crimps that fail under load.

6. **Leaving them in production** -- DuPont connections left in place for months develop intermittent failures from [[learning/notes/micro-context/oxidation|oxidation]], vibration, and spring fatigue. Graduate to proper connectors for anything permanent.

7. **Mixing 2.54mm and 2.0mm pitch** -- Some boards (certain ESP modules, fine-pitch breakouts) use 2.0mm headers. Standard DuPont connectors won't seat properly.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> -- Related topics to explore</summary>

- **Breadboards** -- The solderless prototyping boards that DuPont jumpers are designed to connect to; share the 2.54mm pitch standard
- **Pin headers** -- The male 0.1" pitch headers on PCBs that DuPont female connectors mate with
- **JST connectors** -- The keyed, latched alternative for semi-permanent connections (XH, PH, SH families)
- **Wire gauge (AWG)** -- Understanding current capacity vs wire thickness; critical for knowing when DuPont jumpers are adequate
- **Crimping** -- The mechanical process of attaching contacts to wire; the skill needed to make custom DuPont cables
- **RC servo connectors** -- 3-pin DuPont-compatible connectors used throughout hobby robotics and RC models
- **I2C / Qwiic / STEMMA QT** -- Modern standardized connector ecosystems (JST SH 4-pin) replacing ad-hoc DuPont wiring for sensor buses

</details>

<details>
<summary><strong>Alternatives Comparison</strong></summary>

| Connector | Pitch | Latching? | Current | Best For |
|-----------|-------|-----------|---------|----------|
| **DuPont** | 2.54mm | No | ~1A practical | Breadboard prototyping |
| **JST XH** | 2.5mm | Friction tab | 3A | Semi-permanent wire-to-board |
| **JST PH** | 2.0mm | Yes | 2A | Compact connections, LiPo [[learning/notes/quick-context/galvanic-cells-batteries|batteries]] |
| **JST SH** | 1.0mm | Yes | 1A | Qwiic/STEMMA QT I2C bus |
| **Molex KK 254** | 2.54mm | Polarized | 4A | Keyed 0.1" connections |
| **Screw terminals** | Various | Clamped | 10-30A | Power connections, field wiring |
| **XT30 / XT60** | N/A | Friction | 30A / 60A | Battery and high-current DC |
| **Harwin M20** | 2.54mm | Friction | 3A | Higher-quality DuPont-compatible drop-in |

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What pitch dimension defines a DuPont connector, and why does that number matter?
<details>
<summary>Answer</summary>
2.54mm (0.1" / 100 mil). This matters because it matches the universal spacing of breadboard holes and PCB pin headers, making DuPont connectors compatible with virtually all hobbyist development boards. See: 5 Essential Terms.
</details>

**Q2:** Why are modern "DuPont" connectors less reliable than the original Berg Mini-PV design?
<details>
<summary>Answer</summary>
The original Mini-PV used a separate beryllium copper spring for consistent tension and selective gold plating for low contact resistance. Modern clones use cheaper brass with tin plating and a simpler stamped spring, resulting in higher contact resistance, faster wear, and fewer reliable mating cycles (50-100 vs 500+). See: History section.
</details>

**Q3:** You're powering 4 hobby servos through DuPont jumper wires from an Arduino's 5V pin. Each servo draws 300mA under load. What will go wrong and how would you fix it?
<details>
<summary>Answer</summary>
Two problems: (1) Total current is 1.2A through a single 26 AWG DuPont wire, exceeding the practical 1A limit -- the wire will heat up and voltage will drop noticeably (~0.4-0.6V including wire resistance and clone contact resistance at two junctions). (2) The Arduino's onboard 5V regulator can only supply ~500mA total. Fix: use a separate 5V power supply with appropriately rated wiring (XT30 or screw terminals for the main bus), and distribute power to servos through 22 AWG or thicker wire. See: The Key Tension, Concrete Example.
</details>

**Q4:** Someone claims "DuPont connectors are rated for 3A, so they're fine for powering my 12V LED strip." What's wrong with this reasoning?
<details>
<summary>Answer</summary>
The 3A rating applies to genuine-spec connectors with properly crimped 22 AWG wire. Pre-made DuPont jumper wires use 26 AWG wire and clone contacts with poor spring tension and tin plating. The practical limit for these is ~1A, and even that assumes a good crimp and fresh contacts. Additionally, the contact resistance of clone connectors (50-200+ m$\Omega$) causes meaningful voltage drop and heating at higher currents. The datasheet rating cannot be applied to unspecified clones. See: Ratings: Datasheet vs Reality table.
</details>

**Q5:** You're designing a robot that uses DuPont jumpers for sensor connections during prototyping. The robot will eventually be deployed in a school classroom where students will handle it daily. What's your connector migration strategy, and what criteria determine when each connection type gets upgraded?
<details>
<summary>Answer</summary>
Migration strategy: (1) Keep DuPont for bench prototyping and iterating on sensor placement. (2) Once sensor positions are finalized, migrate signal-level connections (<100mA, static) to JST XH or PH connectors for keying and retention. (3) All power connections (servos, motor drivers) should use screw terminals or XT30 connectors from the start of integration testing. (4) For the I2C sensor bus, adopt Qwiic/STEMMA QT (JST SH 4-pin) for standardized, keyed, daisy-chainable connections. Upgrade criteria: any connection that (a) carries >500mA, (b) will be subject to vibration or movement, (c) could be reversed with damaging consequences, or (d) needs to survive repeated student handling should be upgraded to a keyed/latched connector before deployment. See: The Key Tension, Alternatives Comparison.
</details>

</details>
