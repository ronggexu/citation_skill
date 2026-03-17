---
name: add-citation-DISCIPLINE
description: >
  BRIEF DESCRIPTION: what this skill does, for which type of papers.
---
// turbo-all

# Add citations — DISCIPLINE NAME

## Start from the active LaTeX root

- Read the root document before editing.
- Detect `\bibliography{...}` or `\addbibresource{...}`.
- Preserve the existing citation macro style.

## Scan for citable blocks

- Run `python core/scanner.py <root.tex> --config skills/<discipline>/config.yaml --json`.
- The scan strategies are defined in `config.yaml`.
- Skip obviously original claims unless text says they are adapted.

## Search for sources

- Use the preferred source databases defined in `config.yaml`.
- Build queries from context: block title, first sentence, distinctive terms.
- Verify via secondary sources.
- Separate low-confidence matches for user review.

### Canonical references

<!-- Add a table of well-known concept → default key mappings -->

| Concept | Default key |
|---------|------------|
| TODO    | TODO       |

## Edit BibTeX carefully

- Reuse existing BibTeX keys when the same work is present.
- Match the project's key style (see `config.yaml`).
- Include `author`, `title`, `year` + venue. Add `doi`, `eprint` when verified.
- Do not invent metadata.

## Insert citations in TeX

<!-- Describe the discipline-specific citation placement rules -->
- Statement-style environments → `\begin{env}[\cite{Key}]`
- Narrative → cite in body text at first mention.

## Verify before finishing

- Re-run scanner with `--only-missing`.
- Confirm all new BibTeX keys are reachable.
- **Present the full change list to the user for review before applying.**
