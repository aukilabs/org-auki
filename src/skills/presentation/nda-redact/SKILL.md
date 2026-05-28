---
name: nda-redact
description: Post-processing skill that audits a generated presentation for NDA and sensitive material, then rewrites flagged content with appropriate public-facing language. Called automatically by /presentation when audience is community — the only public audience. Never invoked for internal, investor, or client presentations.
---

# /nda-redact

Audits a generated roundup or slide deck for sensitive content and rewrites flagged passages before the file is committed. Never removes sections entirely — always replaces with appropriate language that preserves the narrative while removing the sensitive detail.

---

## When this runs

Called by `/presentation` after generation is complete, before the file is written to disk. Only runs for `community` audience — the only public one. `investor` and `client` presentations go to the private repo and are shared directly by the company, so they do not need NDA redaction (though their tone and content emphasis still differ from internal).

Receives:
- The full generated HTML string
- The audience: `community`
- The author and project context

---

## What to flag and redact

### Always redact
- **Named partners and customers** before public announcement — replace with a descriptor: "a major retail partner", "a logistics customer in Southeast Asia"
- **Specific financial figures** — ARR, deal size, runway, burn rate, valuations — replace with directional language: "significant commercial traction", "largest deal to date"
- **Unreleased feature names** — replace with capability description: "a new spatial anchoring capability" not "Project Heron"
- **Internal codenames** for projects, products, or initiatives not yet public
- **Personnel matters** — hiring plans, departures, org changes not yet announced
- **Legal / compliance situations** — any mention of disputes, audits, regulatory issues
- **Specific technical vulnerabilities** — security findings, unpatched issues, exploit vectors
- **Internal tooling names** that reveal tech stack or vendor relationships under NDA

### Redact for investor only (keep for community)
- **Detailed technical architecture** — investors want outcomes not implementation; replace with business impact framing
- **Competitor mentions** — remove or replace with "incumbent solutions"

### Keep for both community and investor
- **Shipped product capabilities** that are already public
- **Performance metrics** where the underlying method isn't sensitive (latency, accuracy, speed)
- **Team growth signals** where already announced publicly
- **Strategic direction** at a high level

---

## Replacement guidelines

Write replacements that:
- Preserve the narrative arc — the update should still tell a coherent story
- Match Auki's voice — declarative, technically precise, not vague corporate-speak
- Are defensible — if a journalist read this, nothing here would be a leak
- For community: stay accessible and outward-facing
- For investor: emphasise traction, growth signals, and business outcomes

**Bad replacement:** "We made progress on some internal initiatives."
**Good replacement:** "We completed a significant infrastructure improvement that reduces a key latency metric by more than 50%."

---

## Output

Return the full HTML with replacements applied inline. Flag each change with an HTML comment so the author can review:

```html
<!-- NDA-REDACTED: "Acme Corp pilot" → "a major retail pilot" -->
```

After processing, summarise what was changed for the author:
- N passages redacted
- List each: what was removed and what replaced it
- Flag any passages that were ambiguous — ask the author to review before committing

---

## Tone note

The author wrote this. They know what's sensitive. If anything is borderline, surface it rather than silently removing it. The goal is an output the author is confident sharing, not one they discover has been over-sanitised.
