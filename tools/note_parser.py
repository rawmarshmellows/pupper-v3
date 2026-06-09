#!/usr/bin/env python3
"""Shared note parsing utilities.

Extracted from reviewer/code/knowledge-quest/iteration-17/importer/import_notes.py.
All functions are pure (no DB, no network) and depend only on re, yaml, pathlib.
"""

import re
import yaml
from pathlib import Path

CATEGORY_RULES = {
    "electronics": [
        "resistor", "capacitor", "capacitance", "capacitive", "inductor", "diode", "voltage", "current",
        "power", "circuit", "impedance", "reactance", "frequency", "filter",
        "rectifier", "bridge", "buck", "decoupling", "parallel", "series",
        "schematic", "grounding", "return-path", "oscilloscope", "multimeter",
        "electric-current", "electric-magnetic", "electricity", "electromagnetism",
        "electromagnetic", "coil", "magnetic", "lenz", "faraday", "maxwell",
        "self-induction", "induction", "charge", "coulomb", "thermal-noise",
        "watts", "joules", "voltage", "anode", "cathode", "electrode",
        "galvanic", "battery", "electrolyte", "electrolysis",
        "ac-dc", "ac-to-dc", "full-bridge", "capacitor-charging",
        "inductor-current", "permanent-magnet", "relativity-emf",
        "4-wire", "kelvin", "wire-bonding",
    ],
    "semiconductors": [
        "transistor", "mosfet", "bjt", "op-amp", "doped", "silicon",
        "semiconductor", "fabrication", "die", "flip-chip", "bga",
        "bond-pad", "substrate", "interconnect", "metal-layer",
        "code-to-gates", "electromigration",
    ],
    "manufacturing": [
        "pcb", "soldering", "smd", "3d-print", "cnc", "machining", "milling",
        "turning", "edm", "slicer", "filament", "hotend", "bambu", "ams",
        "pick-and-place", "common-ic", "jst", "connector",
    ],
    "protocols": [
        "i2c", "spi", "can-bus", "pwm", "uart", "i2s", "swd",
        "serial", "clock-edge", "clock-speed", "clock-source",
        "ceramic-resonator", "crystal-oscillator",
    ],
    "embedded": [
        "stm32", "st-link", "adc", "imu", "ads1110", "microcontroller",
        "bare-metal", "rtos", "plc", "preempt", "ros2",
        "mems", "accelerometer", "gyroscope", "humidity", "temperature-sensor",
        "coriolis",
    ],
    "robotics": [
        "pid", "kinematic", "gait", "reinforcement", "ppo",
        "pupper", "forward-kinematic", "inverse-kinematic",
        "homogeneous-transformation", "robot",
        "camera", "neural", "lab",
    ],
    "chemistry": [
        "atom", "molecule", "polymer", "chemical-bond", "covalent",
        "anion", "cation", "oxidation", "reduction", "ion",
        "dipole", "van-der-waals", "hydrogen-bond", "pi-pi",
        "glass-transition", "melt-index", "tensile", "breaking-elongation",
        "crystallinity", "amorphous", "platinum", "rust",
    ],
    "sales": [
        "challenger", "sandler", "kare", "meddpicc", "miller-heiman",
        "strategic-selling", "buyer-role", "whitespace", "playbook",
        "account-management", "post-sale", "oee", "teep", "isa-95",
        "integration-failure", "sil-rated", "robot-cell",
    ],
}


def classify_category(file_path, topic):
    name = Path(file_path).stem.lower()
    topic_lower = topic.lower()
    combined = f"{name} {topic_lower}"
    for category, keywords in CATEGORY_RULES.items():
        for kw in keywords:
            if kw in combined:
                return category
    return "other"


def parse_frontmatter(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            fm = yaml.safe_load(match.group(1))
            body = content[match.end():]
            return fm or {}, body
        except yaml.YAMLError:
            return {}, content
    return {}, content


def strip_wiki_links(text):
    return re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]+)\]\]', r'\1', text)


def extract_tldr(body):
    match = re.search(r'>\s*\*\*TL;DR[:\s]*\*\*\s*(.*?)(?:\n\n|\n>|\Z)', body, re.DOTALL)
    if match:
        return strip_wiki_links(re.sub(r'\s+', ' ', match.group(1).strip()))
    return None


def extract_definition(body):
    match = re.search(r'\*\*Definition[:\s]*\*\*\s*(.*?)(?:\n\n|\Z)', body, re.DOTALL)
    if match:
        return strip_wiki_links(re.sub(r'\s+', ' ', match.group(1).strip()))
    return None


def extract_key_insight(body):
    match = re.search(r'\*\*Key [Ii]nsight[:\s]*\*\*\s*(.*?)(?:\n\n|\Z)', body, re.DOTALL)
    if match:
        return strip_wiki_links(re.sub(r'\s+', ' ', match.group(1).strip()))
    return None


def extract_situation(body):
    match = re.search(r'\*\*Situation[:\s]*\*\*\s*(.*?)(?:\n\n|\Z)', body, re.DOTALL)
    if match:
        return strip_wiki_links(re.sub(r'\s+', ' ', match.group(1).strip()))
    return None


def extract_summary(body):
    match = re.search(r'##\s+Summary\s*\n(.*?)(?:\n##|\n---|\Z)', body, re.DOTALL)
    if match:
        text = match.group(1).strip()
        text = re.sub(r'<[^>]+>', '', text)
        text = strip_wiki_links(text)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 30:
            return text
    return None


def extract_essential_terms(body):
    terms = []
    in_terms = False
    for line in body.split('\n'):
        if re.search(r'essential\s+terms', line, re.IGNORECASE):
            in_terms = True
            continue
        if in_terms:
            if line.startswith('|') and '---' not in line:
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if len(cells) >= 2 and cells[0] and cells[1]:
                    term_name = strip_wiki_links(re.sub(r'\*\*', '', cells[0])).strip()
                    term_def = strip_wiki_links(re.sub(r'\*\*', '', cells[1])).strip()
                    if term_name.lower() not in ('term', 'name', ''):
                        terms.append({"term": term_name, "definition": term_def})
            elif not line.startswith('|') and line.strip() and not line.startswith('#'):
                in_terms = False
    return terms


def extract_wiki_links(body):
    links = []
    for match in re.finditer(r'\[\[(.*?)(?:\|.*?)?\]\]', body):
        target = match.group(1).strip()
        target = re.sub(r'^(micro-context|quick-context|small-context)/', '', target)
        links.append(target)
    return list(set(links))


def extract_quiz_questions(body):
    questions = []
    tyu_match = re.search(r'Test Your Understanding', body, re.IGNORECASE)
    if not tyu_match:
        return questions
    qa_text = body[tyu_match.end():]
    pattern = re.compile(
        r'\*\*Q\d+[:\s]*\*\*\s*(.*?)\s*'
        r'<details>\s*'
        r'<summary>\s*Answer\s*</summary>\s*'
        r'(.*?)\s*'
        r'</details>',
        re.DOTALL | re.IGNORECASE
    )
    for match in pattern.finditer(qa_text):
        q = match.group(1).strip()
        a = match.group(2).strip()
        q = re.sub(r'\s+', ' ', q)
        a = re.sub(r'<[^>]+>', '', a)
        a = re.sub(r'\s+', ' ', a).strip()
        a = re.sub(r'^\*\*', '', a)
        a = re.sub(r'\*\*$', '', a)
        a = a.strip()
        q = strip_wiki_links(q)
        a = strip_wiki_links(a)
        if q and a:
            questions.append({"question": q, "answer": a, "level": estimate_bloom_level(q),
                              "source": "test_your_understanding"})
    return questions


def generate_summary_questions(topic, summary):
    questions = []
    if not summary or len(summary) < 50:
        return questions
    questions.append({
        "question": f"Summarize the key points about {topic} in 2-3 sentences.",
        "answer": summary,
        "level": 2,
        "source": "summary",
    })
    questions.append({
        "question": f"Based on your understanding of {topic}, describe a practical scenario where this knowledge would be critical.",
        "answer": summary,
        "level": 3,
        "source": "summary",
    })
    return questions


def generate_insight_questions(topic, key_insight, definition):
    questions = []
    if key_insight and len(key_insight) > 30:
        questions.append({
            "question": f"What is the key insight about {topic}, and why does it matter for practical applications?",
            "answer": key_insight,
            "level": 4,
            "source": "key_insight",
        })
        questions.append({
            "question": f"A colleague claims they fully understand {topic}. What is the one insight that would separate a surface-level understanding from a deep one?",
            "answer": key_insight,
            "level": 5,
            "source": "key_insight",
        })
    if definition and len(definition) > 30:
        questions.append({
            "question": f"Explain {topic} in your own words. What is it and what does it do?",
            "answer": definition,
            "level": 2,
            "source": "key_insight",
        })
    return questions


def generate_term_questions(topic, terms):
    questions = []
    for t in terms:
        if len(t["definition"]) < 20:
            continue
        questions.append({
            "question": f"In the context of {topic}, what is {t['term']}?",
            "answer": t["definition"],
            "level": 1,
            "source": "term_definition",
        })
        questions.append({
            "question": f"What term from {topic} matches this description: {t['definition']}?",
            "answer": t["term"],
            "level": 1,
            "source": "term_reverse",
        })
    return questions


def generate_section_questions(topic, body):
    questions = []
    sections = re.split(r'\n##\s+', body)
    skip_patterns = ['test your understanding', 'essential terms', 'summary',
                     'related', 'references', 'further reading', 'links']
    for section in sections[1:]:
        lines = section.strip().split('\n')
        if not lines:
            continue
        heading = lines[0].strip()
        heading_lower = heading.lower()
        if any(p in heading_lower for p in skip_patterns):
            continue
        content = '\n'.join(lines[1:]).strip()
        content = re.sub(r'<[^>]+>', '', content)
        content = strip_wiki_links(content)
        content = re.sub(r'\s+', ' ', content).strip()
        if len(content) < 60:
            continue
        questions.append({
            "question": f"Regarding {topic}, explain: {heading}",
            "answer": content[:500],
            "level": 2,
            "source": "section_content",
        })
        if len(content) > 200:
            questions.append({
                "question": f"Why is the concept of '{heading}' important when working with {topic}?",
                "answer": content[:500],
                "level": 4,
                "source": "section_analysis",
            })
    return questions


def estimate_bloom_level(question):
    q = question.lower()
    if any(w in q for w in ['define', 'list', 'name', 'what is', 'identify']):
        return 1
    if any(w in q for w in ['explain', 'describe', 'summarize', 'why does', 'how does']):
        return 2
    if any(w in q for w in ['calculate', 'apply', 'use', 'solve', 'demonstrate']):
        return 3
    if any(w in q for w in ['compare', 'contrast', 'analyze', 'differentiate', 'examine', 'why can']):
        return 4
    if any(w in q for w in ['evaluate', 'judge', 'assess', 'justify', 'which is better', 'why is']):
        return 5
    if any(w in q for w in ['design', 'create', 'propose', 'construct', 'develop']):
        return 6
    return 2


def detect_tier(file_path):
    parts = Path(file_path).parts
    for part in parts:
        if 'micro' in part.lower():
            return 'micro'
        if 'small' in part.lower():
            return 'small'
        if 'quick' in part.lower():
            return 'quick'
    return 'quick'


def strip_markdown_formatting(text):
    text = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, flags=re.DOTALL)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'<details>.*?</details>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\[\[(.*?)(?:\|(.+?))?\]\]', lambda m: m.group(2) or m.group(1), text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'[*_]{1,3}', '', text)
    text = re.sub(r'#{1,6}\s+', '', text)
    text = re.sub(r'^\s*[-*+]\s', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*>\s?', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()
