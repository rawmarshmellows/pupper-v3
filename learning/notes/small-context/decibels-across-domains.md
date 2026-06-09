---
case: Why Decibels Show Up Everywhere — Volume, CMRR, Dynamic Range, PSNR
components: [decibel, logarithm, power-vs-amplitude, reference-level]
created: 2026-06-08
---

# Case: Why Decibels Show Up Everywhere (Volume → CMRR → Dynamic Range → PSNR)

> **Components:** [[quick-context/frequency-and-filtering]] | [[quick-context/thermal-noise-electronics]] | [[quick-context/camera-fundamentals]]
> **Micro-context:** [[micro-context/common-mode-rejection-ratio]] | [[micro-context/power-supply-rejection-ratio]] | [[micro-context/open-loop-voltage-gain]]

> **In brief:** Turn up the volume, read an op-amp's [[micro-context/common-mode-rejection-ratio|CMRR]], check a camera's dynamic range, score a compressed image with PSNR — the same little unit, **dB**, shows up in all four. It is not a coincidence: every one of these is the *same operation* — take a **ratio** of two quantities, take its **logarithm**, scale by 10 (or 20). Once you see the recipe, every "dB" reads the same way.

## The Situation

The decibel feels like four unrelated units wearing one costume. In audio it measures loudness; on a [[quick-context/comparator-specification|comparator datasheet]] it measures how well a chip ignores noise; in photography it measures the brightest-to-darkest range a sensor can hold; in image compression it scores how close a JPEG is to the original. Why does *one* unit span perception, analog electronics, optics, and information theory? Because all four are asking the same question — "how big is this compared to that?" — and answering it with a logarithm.

## The Pieces

**The logarithm.** A log compresses huge ratios into small numbers ($10^{12}$ becomes "120") and turns *multiplication into addition*. Cascaded gains that would multiply ($100\times$ then $0.5\times$) simply **add** in dB (+20 dB then −3 dB = **+17 dB**) — the trick that makes signal-chain math trivial. It also matches human senses: loudness and brightness are perceived roughly logarithmically (Weber–Fechner law), so the unit and the ear agree.

**Power vs amplitude (the 10-vs-20 rule).** A decibel is *always* a power ratio: $\text{dB} = 10\log_{10}(P/P_\text{ref})$. But power scales as amplitude **squared** ($P \propto A^2$, e.g. $P = V^2/R$), and $\log(A^2) = 2\log(A)$ pulls the exponent out front. So for an *amplitude* quantity (voltage, sound pressure, current) the same dB becomes $20\log_{10}(A/A_\text{ref})$. The 10 and the 20 are not two definitions — they describe the **identical** physical change.

**The reference (the denominator).** Plain dB is a pure dimensionless ratio. Pin the denominator to a fixed value and it becomes an *absolute* measurement: **dB SPL** (ref $20\,\mu\text{Pa}$), **dBm** (ref 1 mW), **dBV** (ref 1 V), **dBFS** (ref digital full scale). Same math, just a named zero point.

> Historical aside: the **bel** is named after Alexander Graham Bell. Bell Labs coined the logarithmic "Transmission Unit" in **1924** to measure power loss on telephone lines (replacing the clumsy "miles of standard cable"), then renamed it the **decibel** in **1928**.

## Step by Step: What Happens

The whole unit is one three-step recipe — run it on *any* pair of quantities:

```
THE ONE RECIPE  —  run it on ANY pair of quantities
==============================================================================

   STEP 1: form a RATIO   ──>   STEP 2: pick 10 or 20   ──>   STEP 3: log + scale

     numerator                    power?      → 10·log         dB = N · log10(ratio)
     ──────────                   amplitude?  → 20·log         one human-sized number
     denominator                  20 because P ∝ A²

   "how big vs what?"           "squaring doubles the dB"      "× turns into +"
```

### Step 1: Form the ratio
Decide what you want (numerator) over what you compare against (denominator). Loudness: sound pressure over the hearing threshold. CMRR: wanted gain over leaked gain. Dynamic range: brightest over darkest. PSNR: peak signal over error.

### Step 2: Pick 10 or 20
If both quantities are already **powers** (watts, intensity, mean-squared error), use $10\log_{10}$. If they are **amplitudes** (volts, pascals, pixel values), use $20\log_{10}$.

### Step 3: Take the log, scale, read it off
The result is one human-sized number. Here is the *same* recipe instantiated across the four domains the question asked about:

```
SAME OPERATION, FOUR DOMAINS   (only the numerator/denominator change)
==============================================================================

  DOMAIN             NUMERATOR   ÷  DENOMINATOR          N      dB FORMULA
  ──────────────────────────────────────────────────────────────────────────
  Volume (dB SPL)    pressure p  ÷  20 µPa (hearing)     20·    20·log10(p / 20µPa)
  CMRR               diff gain   ÷  common-mode gain     20·    20·log10(Ad / Acm)
  Camera dyn range   full well   ÷  noise floor          20·    20·log10(Vmax / Vn)
  PSNR               MAX²        ÷  MSE (error)           10·    10·log10(MAX² / MSE)
  ──────────────────────────────────────────────────────────────────────────
  (bonus) SNR        signal pwr  ÷  noise-floor pwr       10·    10·log10(Ps / Pn)
```

- **Volume** — pressure is an amplitude, so $20\log$. Reference $20\,\mu\text{Pa}$ = threshold of hearing, so 0 dB SPL = "just audible." Whisper ≈ 30 dB, conversation ≈ 60 dB, traffic ≈ 80 dB, rock concert ≈ 110 dB, jet takeoff ≈ 140 dB.
- **[[micro-context/common-mode-rejection-ratio|CMRR]]** — a ratio of two *gains* (differential ÷ common-mode), so $20\log$. 75 dB means common-mode noise is rejected by **≈ 5623×**. Its sibling [[micro-context/power-supply-rejection-ratio|PSRR]] (80 dB ≈ 10,000×) is the same shape for supply ripple.
- **Camera dynamic range** — full-well charge ÷ [[quick-context/thermal-noise-electronics|noise floor]], an amplitude ratio → $20\log$. Photographers also count it in **stops** (doublings of light); one stop $= 20\log_{10}(2) = 6.02$ dB, so 14 stops $\approx 84.3$ dB. (Full treatment: [[quick-context/camera-fundamentals]].)
- **PSNR** — the error MSE is *already squared* (a power), so $10\log$: $\text{PSNR} = 10\log_{10}(\text{MAX}^2/\text{MSE})$, with MAX = 255 for 8-bit. It is literally an [[quick-context/thermal-noise-electronics|SNR]] where the "noise" is compression error.

## The Result

Because it is all one operation, a handful of conversion anchors decodes *every* dB you will ever meet:

```
THE UNIVERSAL CONVERSION TABLE     ratio = 10^(dB/20) amplitude,  10^(dB/10) power
==============================================================================

    dB        POWER ratio  (10·log)        AMPLITUDE ratio  (20·log)
   ──────────────────────────────────────────────────────────────────
     0 dB          1×    (equal)                  1×    (equal)
     3 dB          2×    (DOUBLE power)           1.41×  (√2)
     6 dB          4×                             2×    (DOUBLE amplitude)
    10 dB         10×                             3.16×
    20 dB        100×                            10×
    60 dB         10⁶×                         1,000×    (op-amp gain)
    75 dB    ~3.2×10⁷×                         ~5,623×    (CMRR)
    80 dB         10⁸×                        10,000×    (PSRR)
   100 dB        10¹⁰×                       100,000×    (open-loop gain)
```

This is why a single mental table serves audio engineers, op-amp designers, photographers, and codec authors. They are not using "different decibels" — they picked different numerators and denominators and ran the same recipe.

## Why Each Piece Matters

- **The logarithm:** turns million-to-one spans into two-digit numbers and converts cascaded gain *multiplication* into *addition* (+20 dB − 3 dB = +17 dB).
- **The 10-vs-20 rule:** the only real decision. Power → 10, amplitude → 20, because $P \propto A^2$. Miss it and your CMRR or PSNR is off by a factor of two in dB.
- **The reference:** decides whether dB is *relative* ("3 dB louder than before") or *absolute* (dB SPL, dBm, dBFS). Naming the zero is what turns a ratio into a measurement.

## Go Deeper

**Quick definitions (30 seconds):**
- [[micro-context/common-mode-rejection-ratio]] — CMRR: rejecting noise common to both inputs (75 dB ≈ 5600×)
- [[micro-context/power-supply-rejection-ratio]] — PSRR: rejecting supply-rail ripple (80 dB ≈ 10,000×)
- [[micro-context/open-loop-voltage-gain]] — why 100 dB of gain slams a comparator to the rail

**Full treatment (10 minutes):**
- [[quick-context/frequency-and-filtering]] — "Decibels: the language of signal levels," the −3 dB cutoff, and dB/decade rolloff
- [[quick-context/thermal-noise-electronics]] — the noise floor that sits in the denominator of every SNR and dynamic-range figure
- [[quick-context/camera-fundamentals]] — dynamic range in stops *and* dB, and the 6.02 dB/stop bridge
- [[quick-context/comparator-specification]] — where CMRR, PSRR, and gain appear together on a real datasheet

## Test Your Understanding

**Q1:** A comparator lists CMRR = 75 dB. By what factor does it attenuate a common-mode disturbance, and why is the multiplier 20 (not 10)?

> CMRR is a ratio of two *gains* (amplitude quantities), so it uses $20\log_{10}$. Inverting: ratio $= 10^{75/20} = 10^{3.75} \approx 5623\times$. The 20 appears because gain is an amplitude ratio, and $20\log_{10}(A) = 10\log_{10}(A^2)$ describes the same underlying power change.

**Q2:** Doubling your amplifier's output power raises SPL by only +3 dB, yet listeners say you need "twice as loud." How much more power is that, and why the gap?

> +3 dB = 2× power (since $10\log_{10}2 = 3.01$). But *perceived* loudness roughly doubles every **+10 dB**, which is **10× the power**. The gap is that the ear responds logarithmically (Weber–Fechner): a 10× intensity jump only *sounds* about twice as loud.

**Q3:** PSNR uses $10\log_{10}(\text{MAX}^2/\text{MSE})$ while camera dynamic range uses $20\log_{10}(V_\text{max}/V_\text{noise})$. Both are "signal over noise" — why does one use 10 and the other 20?

> MSE is a **mean *squared* error** — already a power quantity — so PSNR takes $10\log$ of a power ratio. Dynamic range compares two **amplitudes** (voltages), so it takes $20\log$. They are the same operation; the factor differs only because PSNR's quantities are pre-squared. (Indeed $10\log_{10}(\text{MAX}^2/\text{MSE}) = 20\log_{10}(\text{MAX}/\sqrt{\text{MSE}})$.)
