---
name: add-citation-hep-th
description: >
  Find authoritative sources for claims, equations, and review passages in
  high-energy physics / string theory LaTeX manuscripts. Use INSPIRE-HEP
  for bibliography data and insert citations in body text or footnotes
  following hep-th conventions.
---
// turbo-all

# Add citations — High-Energy / String Theory (hep-th)

## Start from the active LaTeX root

- Read the root document before editing.
- Detect `\bibliography{...}` or `\addbibresource{...}`.
- Prefer the INSPIRE BibTeX format (`Author:YYxx`).

## Scan for citable blocks

- hep-th papers **rarely use theorem environments**. Instead, scan for:
  1. **Pattern-based blocks**: sentences containing "it is well known that",
     "it was shown in", "as proved by", `\gc`, or unnamed `\cite{}` placeholders.
  2. **Review / Background sections**: entire `\section{Review}` or
     `\subsection{Preliminaries}` blocks are likely review material needing citations.
  3. **Key equations**: `\begin{equation}` or `\begin{align}` with `\label` that
     contain previously-known results.

- Run `python core/scanner.py <root.tex> --config skills/hep-th/config.yaml --json`.

## Search for sources

- **INSPIRE-HEP** is the primary source (use the INSPIRE API or web search).
- Cross-check with arXiv for preprint metadata.
- Prefer published journal versions over preprints.
- For well-known results (e.g. AdS/CFT, Maldacena duality), use the field-standard citation.

### Canonical references for this discipline

| Concept | Default key |
|---------|------------|
| AdS/CFT correspondence | `Maldacena:1997re` |
| Superstring theory | `Polchinski:1998rq`, `Polchinski:1998rr` |
| Gauge/gravity duality review | `Aharony:1999ti` |
| Topological field theory | `Witten:1988ze` |
| D-branes | `Polchinski:1995mt` |
| Conformal bootstrap | `Rattazzi:2008pe` |
| Anomaly inflow | `CallanHarvey:1984` |

## Edit BibTeX carefully

- Use INSPIRE key style: `LastName:YYxx` (e.g. `Maldacena:1997re`).
- Import full BibTeX records from INSPIRE when available.
- Include `reportNumber` and `eprint` fields for arXiv papers.
- Protect special characters in titles.

## Insert citations in TeX

- hep-th convention: cite **inline in body text**, not in environment optional notes.
- Place `\cite{Key}` at the end of the sentence stating the known result.
- For key equations from the literature, cite immediately after the equation environment.
- Use `\footnote{\cite{Key}}` only when the claim is tangential.

## Verify before finishing

- Re-run the scanner with `--only-missing`.
- Confirm all INSPIRE keys resolve correctly.
- **Present the full change list to the user for review before applying.**
