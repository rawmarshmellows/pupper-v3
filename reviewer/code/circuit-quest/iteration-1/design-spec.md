# Circuit Quest: Pupper Rescue -- Pedagogical Design Specification

## Game Identity

**Title:** Circuit Quest: Pupper Rescue
**Genre:** Circuit diagnosis / repair RPG
**Setting:** An electronics repair lab where the player is an apprentice robotics engineer tasked with reviving a broken Pupper v3 quadruped robot. Each subsystem of the robot is a game zone with circuit puzzles.

---

## Pedagogical Framework

### Intrinsic Integration (Habgood Model)

Every game mechanic maps directly to an electronics concept. There are no quiz popups, no "answer to proceed" gates. The player learns by doing -- diagnosing real circuit problems using real electronics reasoning.

| Game Mechanic | Electronics Concept |
|---|---|
| Reading the schematic display and tracing signal paths | Schematic literacy, node voltage analysis |
| Selecting replacement components from inventory | Component selection (E-series values, package types, voltage ratings) |
| Adjusting resistor values in voltage dividers | Ohm's Law, voltage divider equation |
| Choosing communication protocols for sensor hookups | I2C vs SPI vs CAN tradeoffs |
| Interpreting symptom descriptions (dim LED, noisy signal) | Circuit debugging methodology |
| Managing RC time constants to fix timing issues | Capacitor charging/discharging, tau = RC |
| Placing decoupling capacitors near ICs | High-frequency power delivery, ESL/ESR |
| Setting CAN bus termination | Transmission line theory, impedance matching |

### Bloom's Taxonomy Targeting

The game targets Apply, Analyze, and Evaluate -- never just Remember or Understand.

| Bloom's Level | How the Game Engages It |
|---|---|
| **Apply** | Player calculates resistor values for voltage dividers, computes RC time constants, selects pull-up resistor values for I2C |
| **Analyze** | Player traces current paths through series/parallel circuits, identifies which component is causing a symptom, determines why a protocol fails at distance |
| **Evaluate** | Player chooses between multiple valid solutions (e.g., lower pull-up resistance vs. bus buffer for I2C capacitance issue), weighs tradeoffs (speed vs. wire count vs. noise immunity) |

### Desirable Difficulties

- **Interleaving:** Puzzles mix concepts. A power supply puzzle may require understanding both the voltage divider (resistors) and output filter (capacitors + inductor).
- **Varied contexts:** The same concept (e.g., Ohm's Law) appears in LED current limiting, voltage divider design, pull-up resistor selection, and CAN termination -- never the same surface problem twice.
- **Scaffolding that fades:** Zone 1 (Power Supply) shows the schematic with annotations. Zone 2 shows the schematic without annotations. Zone 3 may require the player to sketch the missing part of the circuit mentally. Zone 4+ presents only symptoms and the player must determine what to even look at.

---

## Game Structure

### Character Creation

The player chooses a name and one of three specializations:

| Specialization | Starting Bonus | Flavor |
|---|---|---|
| **Power Systems** | +2 Circuit Analysis, starts with multimeter | You understand voltage regulation and power delivery |
| **Signal Integrity** | +2 Signal Tracing, starts with oscilloscope | You can read waveforms and trace signal paths |
| **Protocol Engineering** | +2 Protocol Knowledge, starts with logic analyzer | You understand how devices communicate |

Specialization affects starting tools and skill bonuses, but all content is accessible to all builds.

### Skill System (d20 Electronics Checks)

Traditional RPG ability scores remapped to electronics:

| Skill | Used For |
|---|---|
| **Circuit Analysis** | Calculating values, applying Ohm's Law, analyzing series/parallel |
| **Signal Tracing** | Following current paths, reading schematics, finding open/short circuits |
| **Component Knowledge** | Identifying parts, knowing specs, selecting replacements |
| **Protocol Knowledge** | Understanding I2C/SPI/CAN, choosing the right bus, configuring parameters |
| **Steady Hands** | Soldering, physical repairs, component placement |
| **Intuition** | Noticing patterns, gut feelings about failure modes, experience-based shortcuts |

Checks: d20 + skill modifier >= difficulty class. Natural 20 = critical insight (bonus information). Natural 1 = comical but educational failure.

### Zone Structure

#### Zone 1: Power Supply Bay
**Concepts:** Buck converter, voltage dividers, Ohm's Law, inductor behavior, capacitor filtering
**Narrative:** Pupper's main power is dead. The 5V rail reads 0V. Something in the TPS54561 buck converter circuit is wrong.
**Puzzles:**
1. **The Missing Feedback Resistor** -- R6 (11.5k) is missing from the voltage divider. Player must calculate the correct value to set 5V output. Uses: Vout = Vref x (1 + R5/R6), where Vref = 0.8V and R5 = 60.4k.
2. **Blown Output Capacitor** -- C18 (47uF) has failed. Player must select replacement from inventory considering capacitance value, voltage rating, and package size.
3. **Inductor Saturation** -- Someone replaced L1 with a 10uH inductor rated for only 500mA. At 3A load, it saturates. Player must understand saturation current and select a properly rated inductor.
4. **Reverse Polarity Protection** -- D1 (Schottky diode) is installed backwards. Player must understand diode orientation and forward vs. reverse bias.

#### Zone 2: Sensor Network
**Concepts:** I2C protocol, pull-up resistors, RC time constants, voltage levels, ADC resolution
**Narrative:** Power is restored but the IMU (BNO086) and battery ADC (ADS1110) aren't responding. The I2C bus is dead.
**Puzzles:**
1. **Missing Pull-ups** -- I2C SDA and SCL lines have no pull-up resistors. Player must add correct value (4.7k for 400kHz operation) and understand why I2C needs them (open-drain).
2. **Address Conflict** -- Two devices configured to same I2C address. Player must check addresses and reconfigure (understanding 7-bit addressing).
3. **Bus Capacitance Overload** -- Too many devices added to I2C bus, total capacitance exceeds 400pF. Player must calculate total parasitic capacitance and decide: reduce devices, lower pull-up resistance, or add a bus buffer.
4. **Voltage Level Mismatch** -- A 5V sensor connected to 3.3V I2C bus. Player must add a voltage divider or level shifter.

#### Zone 3: Motor Control Hub
**Concepts:** CAN bus, differential signaling, termination resistors, noise immunity, protocol selection
**Narrative:** Legs 1-3 work but Leg 4's three servos are unresponsive. The CAN bus for that leg has issues.
**Puzzles:**
1. **Missing Termination** -- CAN Bus 4 is missing its 120 ohm termination resistor. Player sees signal reflections described as symptoms (intermittent errors, worse at high speed). Must place termination at bus endpoints.
2. **Wrong Protocol** -- An intern tried to use SPI for a 30cm cable to the leg motors. Player must explain why CAN (differential, noise-immune) is needed over SPI (single-ended, short range) in an EMI environment.
3. **Transceiver Failure** -- MAX3051 transceiver for Bus 4 is blown. Player must identify it as the point of failure and replace it, understanding the transceiver's role (single-ended to differential conversion).
4. **Priority Inversion** -- Emergency stop message has a high CAN ID (low priority). Player must understand arbitration and reassign IDs so safety messages win.

#### Zone 4: Communication Bridge
**Concepts:** SPI configuration, protocol comparison, clock polarity/phase, full-duplex vs half-duplex
**Narrative:** The Raspberry Pi can't talk to the main MCU (U1). The SPI link between them is garbled.
**Puzzles:**
1. **Clock Mode Mismatch** -- Pi is configured for SPI Mode 0, MCU expects Mode 3. Player must understand CPOL/CPHA and match settings.
2. **Chip Select Wiring** -- CS line is floating (not connected). Player must understand active-low chip select and wire it correctly.
3. **Speed vs. Distance Tradeoff** -- SPI clock set too high for the trace length. Player must reduce clock speed or understand signal integrity.
4. **Protocol Selection Challenge** -- Final integration: player must assign the right protocol to each subsystem (SPI for MCU-MCU, I2C for sensors, CAN for motors, UART for debug) and justify each choice.

#### Zone 5: Full Integration (Boss Zone)
**Concepts:** All previous concepts combined, system-level debugging
**Narrative:** All subsystems are individually working, but Pupper still won't walk. Multiple interacting issues.
**Puzzles:**
1. **Decoupling Nightmare** -- Random crashes under load. Player must add decoupling capacitors near MCU power pins and understand transient current demands.
2. **Ground Loop** -- Sensor readings are noisy. Player must trace the return path and understand ground plane importance.
3. **The Full Diagnosis** -- Pupper attempts to walk but one leg stutters. Player must trace from symptom through CAN bus, motor controller, power supply, and back to find the root cause (a series of small issues compounding).

### Premium Zones (Locked, described but not playable)

- **Zone 6: RF Communications** -- WiFi module integration, antenna matching, impedance
- **Zone 7: Advanced Power** -- Multi-rail power sequencing, hot-swap protection
- **Zone 8: Signal Integrity** -- High-speed PCB design, controlled impedance, crosstalk

---

## Progression Mechanics

### Experience and Leveling
- XP earned by solving puzzles (more XP for harder puzzles, bonus for first-try solutions)
- Leveling up increases skill modifiers and unlocks new tools
- Tools: Multimeter (read voltages/resistances), Oscilloscope (see waveforms), Logic Analyzer (decode protocols), Soldering Iron (make physical changes), Component Tester (identify unknown parts)

### Inventory System
- Player collects components: resistors (various values), capacitors (various types/values), ICs, connectors
- Components found in supply closet, earned as puzzle rewards, or purchased from the parts catalog
- Wrong component selection teaches through failure (e.g., installing a 25V-rated cap on a 24V rail -- it works initially but fails under stress)

### Save System
- Auto-save to localStorage after each puzzle completion
- Saves: current zone, puzzle progress, inventory, skill levels, character info

---

## Narrative Voice and Tone

- **Mentor character:** "Doc" -- a veteran EE who gives contextual hints, never answers directly
- **Tone:** Encouraging but technically rigorous. Treats the player as a capable apprentice, not a student being quizzed
- **Failure responses:** Always educational. "The capacitor popped -- but notice how the voltage was 28V on a 25V-rated cap. What does that tell you about voltage ratings?"
- **Success responses:** Acknowledge the specific reasoning, not just "correct!" -- "Right. The 120 ohm termination matches the bus impedance, preventing the signal energy from reflecting back and corrupting data."

---

## Technical Requirements

- Single self-contained HTML file with embedded CSS and JavaScript
- Dark theme (comfortable for long sessions, matches "electronics lab" aesthetic)
- Mobile-responsive (playable on phone with touch)
- localStorage save state
- No external dependencies (fully offline capable)
- Freeform text input + context-sensitive suggested action buttons
- ASCII art circuit diagrams rendered in monospace

---

## Anti-Patterns Avoided

1. **No quiz popups** -- Learning happens through gameplay mechanics
2. **No "read this text then answer"** -- Information is discovered through exploration and diagnosis
3. **No disconnected rewards** -- XP comes from circuit knowledge, not from clicking fast or finding hidden objects
4. **No single-concept isolation** -- Puzzles naturally interleave multiple concepts
5. **No trivial difficulty** -- Even Zone 1 requires actual calculation, not just recognition
