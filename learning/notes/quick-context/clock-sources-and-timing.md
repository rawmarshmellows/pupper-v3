---
topic: Clock Sources and Timing
created: 2026-03-29
---

# Clock Sources and Timing

> **Related:** [[micro-context/clock-edges]] | [[micro-context/clock-source]] | [[micro-context/clock-speed]] | [[micro-context/clock-speed-vs-temperature]] | [[micro-context/ceramic-resonator]]

> **TL;DR:** A [[micro-context/microcontroller|microcontroller]]'s clock chain starts with a frequency source ([[quick-context/rc-oscillator|RC oscillator]], [[micro-context/ceramic-resonator|ceramic resonator]], or quartz crystal), multiplied by a PLL to reach operating speed, then divided down for peripheral buses. Every rising clock edge triggers one step of computation, and each edge dissipates energy as heat ($P = CV^2f$), creating the fundamental speed-temperature tradeoff in all digital systems.

## The Core Problem

Every digital circuit needs a heartbeat -- a precise, repeating signal that tells billions of transistors exactly when to "look" at their inputs. The [[micro-context/clock-source|clock source]] determines how accurate that heartbeat is, the PLL multiplies it to operating speed, and the [[micro-context/clock-edges|clock edges]] are the atomic units of computation. But faster clocks generate more heat, and heat degrades performance, so the entire clock chain is a negotiation between speed, accuracy, power, and thermal limits.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Clock Source** | The component that generates the base frequency reference -- either an on-chip [[quick-context/rc-oscillator|RC oscillator]] (HSI), an external [[micro-context/ceramic-resonator|ceramic resonator]], or a [[micro-context/crystal-oscillator|quartz crystal]] (HSE). The Pupper v3 uses an 8 MHz ceramic resonator. |
| **PLL (Phase-Locked Loop)** | An on-chip circuit that multiplies the low base frequency up to operating speed. The Pupper's STM32F446 multiplies 8 MHz $\times$ 22.5 = 180 MHz. The PLL's job is speed; the source's job is stability. |
| **Clock Edge** | The precise moment when the clock signal transitions between states -- rising (0->1) or falling (1->0). [[micro-context/clock-edges|Flip-flops and registers]] capture data only at edges, ignoring the messy analog transitions in between. |
| **SYSCLK / Bus Dividers** | The PLL output (SYSCLK) is too fast for some peripherals, so it's divided down: APB1 at $\div 4$ (45 MHz max), APB2 at $\div 2$ (90 MHz max) on the STM32F446. |
| **Dynamic Power ($P = CV^2f$)** | Every clock edge charges and discharges transistor gate capacitances, converting electrical energy to heat. Power scales linearly with frequency and quadratically with voltage -- the fundamental reason CPUs throttle when hot. |

<details>
<summary><strong>How It Works</strong></summary>

### The Full Clock Chain: Source to Computation

The clock chain has four stages: source generation, PLL multiplication, bus distribution, and edge-triggered computation.

```
THE COMPLETE CLOCK CHAIN
==============================================================================

  STAGE 1: SOURCE                STAGE 2: PLL        STAGE 3: BUS DIVIDERS
  ─────────────────              ────────────         ─────────────────────

  Internal (HSI)                 ┌─────────┐
  16 MHz RC ─────────────────────►         │
  (±1-5%, free, on-chip)        │         │         ┌──► AHB  (180 MHz)
                                │   PLL   │         │
  External (HSE)           ┌───►│  ×N/÷M  ├──► SYSCLK──► APB2 (÷2 → 90 MHz)
  8 MHz ceramic ───────────┘    │         │         │
  resonator (±0.5%)             └─────────┘         └──► APB1 (÷4 → 45 MHz)
        ▲                                                    │
    Pupper uses this                                    Peripheral clocks:
                                                        Timers, UART, I2C,
  External (HSE)                                        CAN, SPI, ADC, etc.
  8 MHz quartz crystal
  (±0.002%, most accurate)


  STAGE 4: EDGE-TRIGGERED COMPUTATION
  ────────────────────────────────────

  Clock:  ───┐   ┌───┐   ┌───┐   ┌───
             └───┘   └───┘   └───┘
             ↑       ↑       ↑
             │       │       │
          Sample   Sample   Sample
          data     data     data
          (edges)  (edges)  (edges)

  Between edges: combinational logic computes new values
  At each edge: flip-flops capture ("latch") the results
  This is why imperfect analog transistors behave as perfect digital switches
```

### Three Clock Source Types Compared

```
CLOCK SOURCE ACCURACY HIERARCHY
==============================================================================

  ┌─────────────────────┬───────────┬─────────────┬──────────────────────────┐
  │ Source              │ Accuracy  │ Cost        │ Use Case                 │
  ├─────────────────────┼───────────┼─────────────┼──────────────────────────┤
  │ RC Oscillator (HSI) │ ±1-5%    │ Free        │ PWM, fallback, boot      │
  │                     │           │ (on-chip)   │                          │
  ├─────────────────────┼───────────┼─────────────┼──────────────────────────┤
  │ Ceramic Resonator   │ ±0.5%    │ ~$0.10-0.30 │ CAN, UART, I2C, SPI     │
  │ (HSE)               │           │ (1 part)    │ ← Pupper v3 uses this   │
  ├─────────────────────┼───────────┼─────────────┼──────────────────────────┤
  │ Quartz Crystal      │ ±0.002%  │ ~$0.20-1.00 │ USB, Ethernet, RF,       │
  │ (HSE)               │ (20 ppm) │ (+2 caps)   │ precision timing         │
  └─────────────────────┴───────────┴─────────────┴──────────────────────────┘

  100x                             10x
  ◄────── more accurate ──────────►◄────── more accurate ──────►
  RC oscillator          Ceramic resonator          Quartz crystal
```

### PLL Multiplication Math

The PLL multiplies the source frequency through configurable dividers:

$$f_{SYSCLK} = f_{source} \times \frac{N}{M \times P}$$

For the Pupper v3 STM32F446:
- $f_{source} = 8\text{ MHz}$ (ceramic resonator)
- PLL multiplies to: $8\text{ MHz} \times 22.5 = 180\text{ MHz}$
- APB1 = $180 \div 4 = 45\text{ MHz}$ (timers, [[quick-context/uart|UART]], I2C, CAN)
- APB2 = $180 \div 2 = 90\text{ MHz}$ (SPI, ADC)

### Clock Edges and Signal Settling

```
WHY CLOCK SPEED HAS A CEILING
==============================================================================

  Clock period = 1 / frequency

  180 MHz (Pupper STM32): 1 / 180e6 = 5.56 ns per cycle
  3 GHz (desktop CPU):    1 / 3e9   = 0.33 ns per cycle
  5 GHz (overclocked):    1 / 5e9   = 0.2 ns per cycle

  Within each cycle, signals must:
  1. Propagate through combinational logic gates
  2. Settle to a stable 0 or 1 voltage
  3. Meet setup time before the next clock edge

  If signals haven't settled when the edge arrives → wrong data is latched
  → the circuit produces incorrect results

  At 5 GHz, light travels only 6 cm in one clock period.
  Signals in copper travel at ~2/3 the speed of light.
  Physical distance becomes a design constraint.
```

### The Power-Temperature Equation

$$P_{dynamic} = C \times V^2 \times f$$

Where:
- $C$ = total switched [[quick-context/capacitance|capacitance]] (fixed by chip design)
- $V$ = supply [[quick-context/voltage|voltage]] (dominates because it's squared)
- $f$ = clock frequency (linear relationship)

```
THE HEAT-SPEED FEEDBACK LOOP
==============================================================================

  Double clock speed → ~2× heat
  BUT: higher speed often needs higher voltage
       Double voltage → 4× heat!

  ┌──────────────────────────────────────────────────────┐
  │  Fast clock → more heat → junction temperature rises │
  │      ↑                              │                │
  │      │                              ▼                │
  │  Throttle reduces       Firmware thermal throttle    │
  │  clock speed            kicks in at T_max            │
  └──────────────────────────────────────────────────────┘

  This is why "turbo boost" is temporary: the chip runs
  fast until heat catches up, then slows down to stay
  within its thermal envelope.
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The clock source selection is a four-way tradeoff between accuracy, cost, power, and temperature stability:

**Accuracy vs. Cost:** A quartz crystal gives ±0.002% accuracy but needs two external load capacitors (board space + cost). A ceramic resonator gives ±0.5% with built-in caps (3-pin, no external parts). An RC oscillator is free but drifts ±1-5%, especially over temperature.

**Speed vs. Thermal Budget:** $P = CV^2f$ means every MHz of [[micro-context/clock-speed|clock speed]] costs power and generates heat. The STM32F446 at 180 MHz consumes ~100 mA; at 90 MHz it would consume roughly half that. The Pupper runs at full 180 MHz because motor control at 1 kHz loop rate demands the throughput, but this means the thermal design must handle the heat.

**Startup Speed vs. Accuracy:** The internal RC oscillator (HSI) is ready in microseconds; an external resonator takes ~0.1-0.5 ms; a crystal takes ~1-10 ms. The STM32 boots on HSI immediately, then switches to the external source once the PLL locks. If the external source fails, the MCU can fall back to HSI.

**Protocol Requirements Drive the Choice:** [[quick-context/can-bus|CAN bus]] tolerates ±1.58% clock error -- ceramic resonators (±0.5%) pass easily, even RC oscillators are marginal. USB requires ±0.25% -- only crystals and good resonators qualify. RF communication needs ±0.01% or better -- crystals with temperature compensation (TCXO) are mandatory.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

### The Pupper v3 Clock Chain

The Pupper v3 control board has two STM32F446 microcontrollers, each with its own clock chain:

```
PUPPER V3 CLOCK CHAIN (per STM32)
==============================================================================

  muRata CSTNE8M00G55A000R0          STM32F446
  ┌─────────────────────┐     ┌─────────────────────────────────┐
  │  Ceramic Resonator  │     │                                 │
  │  8.000 MHz ±0.5%    │     │   ┌─────┐    ┌─────────┐       │
  │                     ├─────┤───┤ OSC ├───►│  PLL    │       │
  │  Built-in 33 pF     │     │   │ Amp │    │ ×22.5   ├──► SYSCLK
  │  load capacitors    │     │   └─────┘    └────┬────┘  180 MHz
  │  (no external caps) │     │                   │         │   │
  └─────────────────────┘     │                   │     ┌───┘   │
                              │                   │     │       │
    X1, X2 on the BOM         │               ┌───▼─┐ ┌▼──┐    │
    ~$0.15 each                │               │APB1 │ │APB2    │
                              │               │÷4   │ │÷2 │    │
                              │               │45MHz│ │90MHz    │
                              │               └──┬──┘ └─┬──┘   │
                              │                  │      │       │
                              │               CAN bus  SPI     │
                              │               UART     ADC     │
                              │               I2C      Timers  │
                              └─────────────────────────────────┘

  Why ceramic resonator instead of quartz crystal?
  ─────────────────────────────────────────────────
  1. CAN bus (the Pupper's main communication protocol) tolerates ±1.58%
     → ceramic resonator's ±0.5% is more than adequate
  2. Built-in 33 pF load caps → saves 2 external capacitors per MCU
     → 4 fewer parts on the BOM (2 MCUs × 2 caps each)
  3. 3-pin package vs. 2-pin crystal + 2 separate caps
     → simpler PCB layout, fewer solder joints
  4. No USB on this board → no need for crystal-level accuracy
```

**The one thing most outsiders get wrong about this is...** assuming the 8 MHz ceramic resonator IS the MCU's operating frequency. It's not -- 8 MHz is far too slow for 1 kHz motor control loops with PID computation, sensor fusion, and CAN communication. The resonator is just a stable *reference* that the PLL multiplies by 22.5 to reach 180 MHz. The resonator's job is accuracy; the PLL's job is speed. No CPU runs directly off its oscillator source.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

**Source micro-context files (glossary stubs consolidated here):**

- **[[micro-context/clock-source|Clock Source]]** -- HSI vs HSE selection, PLL multiplication, the full clock tree from source to peripheral buses.
- **[[micro-context/crystal-oscillator|Crystal Oscillator]]** -- Quartz crystal mechanics, ±20 ppm accuracy, why crystals need external load capacitors.
- **[[micro-context/ceramic-resonator|Ceramic Resonator]]** -- Piezoelectric ceramic resonance, ±0.5% accuracy, the muRata part on the Pupper v3 BOM.
- **[[micro-context/clock-speed|Clock Speed]]** -- Frequency as edges per second, signal settling time constraints, why clock speed has a ceiling.
- **[[micro-context/clock-speed-vs-temperature|Clock Speed vs Temperature]]** -- $P = CV^2f$, thermal throttling, the heat-speed feedback loop.
- **[[micro-context/clock-edges|Clock Edges]]** -- Rising/falling edges as the atomic unit of digital computation, edge-triggered flip-flop discipline.

**Related quick-context files:**

- **[[quick-context/rc-oscillator|RC Oscillator]]** -- The simplest clock source type: [[quick-context/resistor|resistor]]-[[quick-context/capacitor|capacitor]] charging loops. Covers the HSI internal oscillator and why it's "good enough" for PWM but not for CAN.
- **[[quick-context/pupper-bom-control-board|Pupper BOM Control Board]]** -- The full BOM including the two muRata CSTNE8M00G55A000R0 ceramic resonators (X1, X2).
- **[[quick-context/can-bus|CAN Bus]]** -- The communication protocol that drives the Pupper's clock source choice: its ±1.58% tolerance makes ceramic resonators sufficient.
- **[[quick-context/firmware|Firmware]]** -- The code that configures the clock tree at startup: selecting HSE, configuring PLL multipliers, switching SYSCLK.

**Related micro-context files:**

- **[[micro-context/stm32-microcontroller|STM32 Microcontroller]]** -- The STM32F446 that receives the clock chain's output.
- **[[micro-context/piezoelectric-effect|Piezoelectric Effect]]** -- The physics underlying both crystal and ceramic resonator operation.
- **[[micro-context/thermal-runaway|Thermal Runaway]]** -- The extreme case of the heat-speed feedback loop.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why doesn't the Pupper v3 MCU run directly at 8 MHz from its ceramic resonator?

<details>
<summary>Answer</summary>

8 MHz is far too slow for the Pupper's workload. At 1 kHz motor control loop rate, the MCU has only 1 ms per loop iteration to run PID control, read sensors via I2C/SPI, process CAN bus messages, and update PWM outputs. At 8 MHz that's only 8,000 clock cycles per iteration -- insufficient for floating-point sensor fusion and multi-axis PID. The PLL multiplies the 8 MHz reference to 180 MHz, giving 180,000 cycles per iteration. The resonator provides a *stable reference frequency*; the PLL provides *speed*. See: Concrete Example.
</details>

**Q2:** The Pupper uses ceramic resonators (±0.5%) instead of quartz crystals (±0.002%). Under what condition would this be a problem?

<details>
<summary>Answer</summary>

If the board needed USB connectivity. USB requires ±0.25% clock accuracy, and while ceramic resonators nominally meet this spec at room temperature, their accuracy degrades over the full operating temperature range. A quartz crystal's ±0.002% (20 ppm) provides a 100x margin. The Pupper v3 control board has no USB -- communication is via CAN bus (±1.58% tolerance) and UART -- so ceramic resonators are more than adequate and save 4 external capacitors across the two MCUs. See: The Key Tension (protocol requirements).
</details>

**Q3:** If you doubled the Pupper's STM32 clock speed from 180 MHz to 360 MHz (and had to raise voltage from 1.8V to 2.2V to make it stable), how much more power would it dissipate?

<details>
<summary>Answer</summary>

Using $P = CV^2f$:

$\frac{P_{new}}{P_{old}} = \frac{V_{new}^2 \times f_{new}}{V_{old}^2 \times f_{old}} = \frac{(2.2)^2 \times 360}{(1.8)^2 \times 180} = \frac{4.84 \times 360}{3.24 \times 180} = \frac{1742.4}{583.2} \approx 2.99$

About 3x more power -- nearly triple. The frequency doubling contributes 2x, and the voltage increase from 1.8V to 2.2V contributes another 1.49x ($2.2^2 / 1.8^2$). This is why voltage scaling dominates: a modest 22% voltage increase causes a 49% power increase due to the $V^2$ relationship. See: How It Works (Power-Temperature Equation).
</details>

**Q4:** The STM32 boots on its internal 16 MHz RC oscillator, then switches to the external 8 MHz ceramic resonator. Explain two reasons for this sequence.

<details>
<summary>Answer</summary>

**Speed:** The RC oscillator (HSI) is ready in microseconds because it's purely electronic -- just transistors oscillating. The external ceramic resonator needs ~0.1-0.5 ms for the piezoelectric element to build up stable mechanical vibration, and the PLL needs additional time to lock onto that reference. The MCU can begin executing startup code immediately on HSI rather than waiting.

**Reliability:** If the external resonator fails (bad solder joint, cracked component, PCB damage), the MCU can detect this and fall back to the HSI clock. It runs at reduced accuracy (±1% instead of ±0.5%) and lower speed (no PLL multiplication), but it still runs -- enough to blink an error LED or send a diagnostic message. If the MCU *required* the external source to start, a resonator failure would brick the board entirely. See: The Key Tension (startup speed).
</details>

**Q5:** A colleague suggests replacing the Pupper's two ceramic resonators with a single quartz [[micro-context/crystal-oscillator|crystal oscillator]] module shared between both STM32s. What are the tradeoffs?

<details>
<summary>Answer</summary>

**Advantages:** A single crystal oscillator module would give both MCUs phase-coherent clocks from one source, potentially simplifying CAN bus timing between the two MCUs. Crystal accuracy (±0.002%) would provide a 250x margin over CAN's ±1.58% requirement. One oscillator module replaces two resonators.

**Disadvantages:** (1) A crystal oscillator module is more expensive than two $0.15 ceramic resonators and requires its own power supply. (2) It creates a single point of failure -- if it dies, both MCUs lose their clock, whereas independent resonators provide fault isolation. (3) Running a high-frequency clock trace between two MCUs on a PCB creates EMI and requires careful impedance-matched routing. (4) The STM32's HSE input expects a resonator or crystal on its OSC_IN/OSC_OUT pins, not a buffered clock output -- you'd need to use a different input mode (HSE bypass). (5) The existing ±0.5% accuracy is already 3x better than CAN requires, so the improved accuracy provides zero practical benefit. The engineering maxim applies: don't add complexity to solve a problem you don't have. See: Concrete Example (why ceramic over crystal).
</details>

</details>
