#!/usr/bin/env python3
"""
Wiki-link auto-linker for Obsidian markdown notes.
Applies Type A (Related Documents Header) and Type B (inline term links).
"""

import os
import re
import sys

# ============================================================
# COMPLETE TERM MAP
# Maps display text -> path (without extension, using short format)
# ============================================================

TERM_MAP = {
    # micro-context terms
    "4-Wire Kelvin Measurement": "micro-context/4-wire-kelvin-measurement",
    "AC vs DC Current": "micro-context/ac-dc-current",
    "ADS1110": "micro-context/ads1110-battery-adc",
    "ADS1110 Battery Voltage ADC": "micro-context/ads1110-battery-adc",
    "ADC": "micro-context/adc-analog-to-digital-converter",
    "Analog-to-Digital Converter": "micro-context/adc-analog-to-digital-converter",
    "Buck Converter": "micro-context/buck-converter",
    "CAN Bus Termination": "micro-context/can-bus-termination",
    "Anode": "micro-context/anode",
    "CAN Bus Transceiver": "micro-context/can-bus-transceiver",
    "Ceramic Resonator": "micro-context/ceramic-resonator",
    "Clock Edge": "micro-context/clock-edges",
    "Cathode": "micro-context/cathode",
    "Clock Speed": "micro-context/clock-speed",
    "Clock Source": "micro-context/clock-source",
    "Clock Speed vs Temperature": "micro-context/clock-speed-vs-temperature",
    "CNC Process Selection": "micro-context/cnc-process-selection",
    "CNC Milling": "micro-context/cnc-milling",
    "Coriolis Effect": "micro-context/coriolis-effect",
    "CNC Turning": "micro-context/cnc-turning",
    "Crystal Oscillator": "micro-context/crystal-oscillator",
    "Current Mirror": "micro-context/current-mirror",
    "Diode Rectification": "micro-context/diode-rectification",
    "Decoupling Capacitor": "micro-context/decoupling-capacitor",
    "EDM Machining": "micro-context/edm-machining",
    "Electromagnetic Induction": "micro-context/electromagnetic-induction",
    "Full-Wave Bridge Rectifier": "micro-context/full-bridge-rectifier",
    "I2C": "micro-context/i2c",
    "Homogeneous Transformation Matrix": "micro-context/homogeneous-transformation-matrix",
    "I2S": "micro-context/i2s",
    "I2S Audio Amplifier": "micro-context/i2s-audio-amplifier",
    "Microcontroller": "micro-context/microcontroller",
    "MOSFET": "micro-context/mosfet",
    "JST Connector Families": "micro-context/jst-connector-families",
    "Piezoelectric Effect": "micro-context/piezoelectric-effect",
    "Pick and Place File": "micro-context/pick-and-place-file",
    "Power Inductor": "micro-context/power-inductor",
    "PLC": "micro-context/plc-programmable-logic-controller",
    "Programmable Logic Controller": "micro-context/plc-programmable-logic-controller",
    "PWM": "micro-context/pwm-pulse-width-modulation",
    "Pulse Width Modulation": "micro-context/pwm-pulse-width-modulation",
    "SPI": "micro-context/spi",
    "SMD Resistor": "micro-context/smd-resistor",
    "Reverse and Forward Bias": "micro-context/reverse-and-forward-bias",
    "SWD": "micro-context/swd-serial-wire-debug",
    "Serial Wire Debug": "micro-context/swd-serial-wire-debug",
    "STM32": "micro-context/stm32-microcontroller",
    "STM32 Microcontroller": "micro-context/stm32-microcontroller",
    "SPIneV1.elf": "micro-context/spinev1-elf",
    "ST-Link V2 Programmer": "micro-context/st-link-v2-programmer",
    "Tail Current": "micro-context/tail-current",
    "Thermal Runaway": "micro-context/thermal-runaway",
    # quick-context terms
    "3D Printer Hotends": "quick-context/3d-printer-hotends",
    "3D Printing Filament Types": "quick-context/3d-printing-filament-types",
    "3D Printing Slicer Settings": "quick-context/3d-printing-slicer-settings",
    "Bambu AMS": "quick-context/bambu-ams-automatic-material-system",
    "Ball Grid Array": "quick-context/bga-ball-grid-array",
    "BGA": "quick-context/bga-ball-grid-array",
    "BJT": "quick-context/bjt",
    "Bipolar Junction Transistor": "quick-context/bjt",
    "Breaking Elongation Rate": "quick-context/breaking-elongation-rate",
    "Bond Pad": "quick-context/bond-pad",
    "Camera Fundamentals": "quick-context/camera-fundamentals",
    "CAN Bus": "quick-context/can-bus",
    "Controller Area Network": "quick-context/can-bus",
    "Capacitive Sensing": "quick-context/capacitive-sensing-measurement",
    "Capacitance": "quick-context/capacitance",
    "Capacitor": "quick-context/capacitor",
    "Challenger Sale Methodology": "quick-context/challenger-sale-methodology",
    "Covalent Bonds": "quick-context/covalent-bonds",
    "Covariance Matrix": "quick-context/covariance-matrix",
    "Differential Pair": "quick-context/differential-pair",
    "Diode": "quick-context/diode",
    "Dipole-Dipole Interactions": "quick-context/dipole-dipole-interactions",
    "Doped Silicon": "quick-context/doped-silicon",
    "DuPont Jumper Wires": "quick-context/dupont-jumper-wires",
    "Electric Current": "quick-context/electric-current",
    "Electric and Magnetic Field Unification": "quick-context/electric-magnetic-field-unification",
    "Electrodes": "quick-context/electrodes",
    "Electricity Generation": "quick-context/electricity-generation",
    "Electrolyte": "quick-context/electrolyte",
    "Electrolysis": "quick-context/electrolysis",
    "Electromagnetism": "quick-context/electromagnetism",
    "Electromigration": "quick-context/electromigration",
    "Embedded Communication Protocols": "quick-context/embedded-communication-protocols",
    "Firmware": "quick-context/firmware",
    "Flip-Chip": "quick-context/flip-chip",
    "Frequency and Filtering": "quick-context/frequency-and-filtering",
    "Galvanic Cells": "quick-context/galvanic-cells-batteries",
    "Galvanic Cell": "quick-context/galvanic-cells-batteries",
    "Glass Transition Temperature": "quick-context/glass-transition-temperature",
    "Grounding and Return Paths": "quick-context/grounding-and-return-paths",
    "High-Gain Amplifier Stage": "quick-context/high-gain-amplifier-stage",
    "Hydrogen Bonds": "quick-context/hydrogen-bonds-beginners",
    "Impedance and Reactance": "quick-context/impedance-and-reactance",
    "Inductor": "quick-context/inductor",
    "Lenz's Law": "quick-context/lenzs-law",
    "Making Electrolytes": "quick-context/making-electrolytes",
    "Maxwell's Equations": "quick-context/maxwell-equations",
    "Metal Interconnect Layers": "quick-context/metal-interconnect-layers",
    "OEE": "quick-context/oee-overall-equipment-effectiveness",
    "Op-Amp": "quick-context/op-amp",
    "Operational Amplifier": "quick-context/op-amp",
    "Oscilloscope and Multimeter": "quick-context/oscilloscope-and-multimeter",
    "PCB Layers": "quick-context/pcb-layers",
    "PCB": "quick-context/pcb-printed-circuit-board",
    "Printed Circuit Board": "quick-context/pcb-printed-circuit-board",
    "Pi-Pi Stacking": "quick-context/pi-pi-stacking-aromatic-interactions",
    "Platinum Inertness": "quick-context/platinum-inertness",
    "PLC vs Software Control": "quick-context/plc-vs-software-control",
    "Polymer Chemical Bonds": "quick-context/polymer-chemical-bonds",
    "Polymer Crystallinity": "quick-context/polymer-crystallinity-vs-amorphous",
    "Electrical Power": "quick-context/power-watts-joules",
    "PPO": "quick-context/ppo-proximal-policy-optimization",
    "Proximal Policy Optimization": "quick-context/ppo-proximal-policy-optimization",
    "PREEMPT_RT": "quick-context/preempt-rt",
    "Pupper Control Board": "quick-context/pupper-bom-control-board",
    "Qwiic": "quick-context/qwiic-stemma-qt-i2c",
    "STEMMA QT": "quick-context/qwiic-stemma-qt-i2c",
    "RC Oscillator": "quick-context/rc-oscillator",
    "Resistor": "quick-context/resistor",
    "ROS2": "quick-context/ros2-architecture",
    "Rust": "quick-context/rust",
    "Schematic Reading": "quick-context/schematic-reading",
    "Self-Induction": "quick-context/self-induction",
    "Semiconductor Fabrication": "quick-context/semiconductor-fabrication",
    "Silicon Die": "quick-context/silicon-die",
    "Similarity Transform": "quick-context/similarity-transform",
    "SVD": "quick-context/singular-value-decomposition",
    "Singular Value Decomposition": "quick-context/singular-value-decomposition",
    "Soldering": "quick-context/soldering",
    "Subatomic Particles": "quick-context/subatomic-particles",
    "Substrate": "quick-context/substrate-ic-packaging",
    "Tensor": "quick-context/tensor",
    "Thermal Noise": "quick-context/thermal-noise-electronics",
    "Transistor": "quick-context/transistor",
    "Van der Waals Forces": "quick-context/van-der-waals-forces",
    "Voltage-Current Causality": "quick-context/voltage-current-causality",
    "Voltage": "quick-context/voltage",
    "Wire Bonding": "quick-context/wire-bonding",
    "WiFi Chip": "quick-context/wifi-chip-arduino-uno-r4",
    "Faraday Tensor": "quick-context/faraday-tensor",
}

# Terms sorted by length descending so longer terms match first
SORTED_TERMS = sorted(TERM_MAP.keys(), key=len, reverse=True)


def get_file_path_stem(filepath):
    """Return path stem like 'quick-context/foo' or 'micro-context/foo'"""
    # e.g. /home/.../quick-context/resistor.md -> quick-context/resistor
    parts = filepath.replace('\\', '/').split('/')
    # Find 'micro-context' or 'quick-context' in path
    for i, p in enumerate(parts):
        if p in ('micro-context', 'quick-context'):
            fname = parts[i+1] if i+1 < len(parts) else ''
            stem = fname.replace('.md', '')
            return f"{p}/{stem}"
    return None


def is_in_code_block(text, pos):
    """Check if position pos is inside a fenced code block."""
    # Count ``` before pos
    before = text[:pos]
    # Find all ``` positions
    fence_positions = [m.start() for m in re.finditer(r'```', before)]
    # If odd number of fences, we're inside a code block
    return len(fence_positions) % 2 == 1


def is_in_existing_link(text, pos, end):
    """Check if the position is inside existing [[...]] brackets."""
    # Look for [[ before pos and ]] after end within reasonable distance
    before = text[:pos]
    after = text[end:]
    # Check if we're inside [[ ... ]]
    last_open = before.rfind('[[')
    last_close = before.rfind(']]')
    if last_open > last_close:
        # We might be inside a link
        close_after = after.find(']]')
        if close_after != -1:
            return True
    return False


def is_heading_line(text, pos):
    """Check if the position is on a heading line (starts with #)."""
    # Find start of line
    line_start = text.rfind('\n', 0, pos) + 1
    line = text[line_start:]
    return line.startswith('#')


def extract_frontmatter(content):
    """Extract frontmatter and return (frontmatter_end, frontmatter_dict)."""
    if not content.startswith('---'):
        return 0, {}
    end = content.find('\n---', 3)
    if end == -1:
        return 0, {}
    fm_text = content[3:end]
    fm_dict = {}
    for line in fm_text.strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm_dict[k.strip()] = v.strip()
    return end + 4, fm_dict  # +4 for '\n---'


def get_related_block(content, fm_end):
    """Get the related block start/end if it exists right after frontmatter."""
    # Look for > **Related:** on the line(s) right after fm_end
    rest = content[fm_end:]
    # Skip blank lines
    stripped = rest.lstrip('\n')
    offset = len(rest) - len(stripped)
    if stripped.startswith('> **Related:**'):
        # Find end of this line
        line_end = stripped.find('\n')
        if line_end == -1:
            line_end = len(stripped)
        return fm_end + offset, fm_end + offset + line_end
    return None, None


def build_related_header(related_paths):
    """Build a > **Related:** line from list of paths."""
    links = ' | '.join(f'[[{p}]]' for p in related_paths)
    return f'> **Related:** {links}'


def apply_type_b_links(content, fm_end, current_file_stem):
    """Apply inline term links to body text."""
    # We'll process the body text (after frontmatter)
    body = content[fm_end:]
    result = []
    # Track which terms have been linked already
    linked_terms = set()
    # Also track terms that are already linked in existing [[]] blocks

    # Process line by line
    lines = body.split('\n')
    in_code_block = False

    for line in lines:
        # Track code block state
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue

        # Skip if in code block
        if in_code_block:
            result.append(line)
            continue

        # Skip headings
        if line.startswith('#'):
            result.append(line)
            continue

        # Skip lines that are inside blockquotes with existing links (Related headers)
        if '> **Related:**' in line or '> **See also:**' in line:
            result.append(line)
            continue

        # Process this line for inline links
        new_line = apply_links_to_line(line, linked_terms, current_file_stem)
        result.append(new_line)

    return content[:fm_end] + '\n'.join(result)


def apply_links_to_line(line, linked_terms, current_file_stem):
    """Apply wiki links to a single line, tracking already-linked terms."""
    result = line

    for term in SORTED_TERMS:
        if term in linked_terms:
            continue

        path = TERM_MAP[term]

        # Don't link to self
        if path == current_file_stem:
            continue

        # Find the term in the line (case-sensitive exact word match)
        # Use word boundary matching
        pattern = r'(?<!\[)\b' + re.escape(term) + r'\b(?!\])'

        match = re.search(pattern, result)
        if not match:
            continue

        pos = match.start()
        end_pos = match.end()

        # Skip if already inside a [[]] link
        if is_in_existing_link(result, pos, end_pos):
            continue

        # Apply the link
        wiki_link = f'[[{path}|{term}]]'
        result = result[:pos] + wiki_link + result[end_pos:]
        linked_terms.add(term)

        # Also mark the path as "used" so we don't double-link to the same file
        # by a different display term (handled naturally since linked_terms tracks display terms)

    return result


def get_topically_related(current_path, content, fm_dict):
    """Find 1-5 topically related files based on topic/category."""
    # Get the topic from current file
    term = fm_dict.get('term', '') or fm_dict.get('topic', '')

    # Parse existing related links from the content if present
    existing_related = []
    related_match = re.search(r'>\s*\*\*Related:\*\*\s*(.*?)(?:\n|$)', content)
    if related_match:
        existing_links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', related_match.group(1))
        existing_related = existing_links

    return existing_related


def process_file(filepath, dry_run=False):
    """Process a single markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()

    content = original_content
    current_stem = get_file_path_stem(filepath)

    # Extract frontmatter
    fm_end, fm_dict = extract_frontmatter(content)

    # Type A: Check/update Related header
    # For now we keep existing related headers as they are (they're already curated)
    # We just apply Type B inline links

    # Apply Type B: inline term links
    new_content = apply_type_b_links(content, fm_end, current_stem)

    if new_content != original_content:
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
        return True  # Modified
    return False  # Not modified


def main():
    base_dir = '/home/user/pupper-v3/learning/notes'

    # Collect all files to process
    all_files = []
    for subdir in ['micro-context', 'quick-context']:
        dirpath = os.path.join(base_dir, subdir)
        for fname in sorted(os.listdir(dirpath)):
            if not fname.endswith('.md'):
                continue
            if fname == 'mosfet copy.md':
                continue
            all_files.append(os.path.join(dirpath, fname))

    print(f"Processing {len(all_files)} files...")
    modified = []
    errors = []

    for filepath in all_files:
        try:
            changed = process_file(filepath)
            if changed:
                modified.append(filepath)
                print(f"  Modified: {os.path.relpath(filepath, base_dir)}")
        except Exception as e:
            errors.append((filepath, str(e)))
            print(f"  ERROR {os.path.relpath(filepath, base_dir)}: {e}")

    print(f"\nDone. Modified {len(modified)} files, {len(errors)} errors.")
    return modified, errors


if __name__ == '__main__':
    main()
