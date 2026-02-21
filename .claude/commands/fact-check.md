---
name: fact-check
description: Verify factual claims in a document using web search
---

Fact-check the document at **$ARGUMENTS**.

## Process

### Step 1: Read and Extract Claims

Read the specified file and identify all factual claims that can be verified. Focus on:
- Numerical values (dates, measurements, statistics, formulas)
- Definitions of technical terms
- Causal relationships ("X causes Y", "X leads to Y")
- Historical facts or attributions ("invented by", "discovered in")
- Comparisons ("X is faster/better/more efficient than Y")
- Mechanisms ("how X works")

Skip subjective opinions, analogies used for explanation, and widely-accepted axioms.

### Step 2: Verify Each Claim

For each verifiable claim:
1. Use WebSearch to find authoritative sources (academic, official documentation, reputable encyclopedias)
2. Compare the document's claim against the search results
3. Note any discrepancies, including partial inaccuracies or oversimplifications that could mislead

### Step 3: Generate Report

Output a structured report:

```markdown
# Fact-Check Report: [filename]

## Summary
- **Total claims checked:** X
- **Verified:** X
- **Issues found:** X
- **Unable to verify:** X

## Verified Claims
[List claims that checked out, with brief source confirmation]

## Issues Found

### [Issue 1 Title]
- **Document says:** [exact quote or paraphrase]
- **Problem:** [what's wrong - inaccurate, oversimplified, outdated, etc.]
- **Correction:** [what it should say]
- **Source:** [URL or citation]

### [Issue 2 Title]
...

## Unable to Verify
[Claims that couldn't be confirmed or denied - may need expert review]

## Sources Consulted
[List of URLs used for verification]
```

### Step 4: Offer Corrections

After presenting the report, ask:
> Would you like me to fix the issues found in the document?

If the user agrees, edit the file to correct inaccuracies while preserving the document's style and structure.

---

## Guidelines

- **Be thorough but practical:** Don't flag stylistic choices or pedagogical simplifications that aid understanding without being misleading
- **Distinguish severity:** Note whether an issue is a minor imprecision vs. a fundamental error that could cause real confusion
- **Preserve intent:** When suggesting corrections, maintain the document's teaching approach and level of detail
- **Cite sources:** Every correction must have a verifiable source
- **Flag uncertainty:** If sources conflict or the topic is genuinely debated, note this rather than declaring one view "correct"
