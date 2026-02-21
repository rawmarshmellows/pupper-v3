---
name: ascii-fixer
description: Fix alignment and rendering issues in ASCII diagrams
---

Fix all ASCII diagrams in the document at **$ARGUMENTS**.

## Process

### Step 1: Read and Identify ASCII Diagrams

Read the specified file and locate all ASCII diagrams. These typically appear within:
- Code blocks (``` or indented blocks)
- Sections labeled as diagrams
- Visual representations using box-drawing characters, arrows, or text art

### Step 2: Analyze Each Diagram

For each ASCII diagram, check for these common issues:

**Alignment Problems:**
- Misaligned box edges (corners don't meet)
- Uneven spacing in tables or grids
- Labels that don't line up with what they describe
- Arrows that don't connect properly

**Character Issues:**
- Inconsistent box-drawing characters (mixing ─ and -, │ and |)
- Broken lines or gaps in borders
- Missing or extra spaces causing visual breaks

**Waveform/Graph Issues:**
- Sine waves that don't show both positive and negative portions
- Waveforms with incorrect amplitude or period representation
- Axes that don't align with data points
- Missing baselines

**Structural Issues:**
- Flow arrows pointing wrong direction relative to described flow
- Components in wrong order relative to explanation
- Missing connections between related elements

### Step 3: Fix Issues

For each issue found:
1. Identify the intended visual representation
2. Correct alignment using consistent spacing
3. Use appropriate box-drawing characters for clean rendering
4. Ensure monospace font assumptions are met
5. Verify the fixed diagram accurately represents the concept

### Step 4: Generate Report and Apply Fixes

Output a summary:

```markdown
# ASCII Diagram Fix Report: [filename]

## Summary
- **Diagrams found:** X
- **Issues fixed:** X
- **Diagrams unchanged:** X

## Fixes Applied

### Diagram 1: [description or line number]
- **Issue:** [what was wrong]
- **Fix:** [what was changed]

### Diagram 2: ...

## Verification Notes
[Any diagrams that may need manual review]
```

Then apply the fixes directly to the file.

---

## Guidelines

- **Preserve intent:** Don't change what the diagram represents, only how it's rendered
- **Consistency:** Use the same character set throughout a diagram (prefer Unicode box-drawing: ─│┌┐└┘├┤┬┴┼)
- **Monospace assumptions:** Ensure diagrams render correctly in monospace fonts
- **Test visually:** After fixing, verify the diagram looks correct in a plain text viewer
- **Document changes:** Note any ambiguous cases where the original intent wasn't clear
