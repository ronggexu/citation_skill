---
name: add-citation-cat-top-order
description: >
  Find authoritative sources for statements in LaTeX files on higher category
  theory and topological order, add or deduplicate BibTeX entries in the active
  bibliography, and insert citations into theorem-like environments or narrative
  blocks without disturbing local formatting.
---
// turbo-all

# Add citations — Categorical Topological Order

## Start from the active LaTeX root

- Read the root document before editing anything.
- Detect the bibliography command (`\bibliography{...}` or `\addbibresource{...}`) and write BibTeX to the file already in the build.
- Prefer an existing local `.bib` file over a shared one.
- Preserve the citation macro style already used in the project.

## Scan for citable blocks

- Run `python core/scanner.py <root.tex> --config skills/cat-top-order/config.yaml --json`.
- Use the default env set in `config.yaml` unless the user narrows it.
- Statement-style envs (axm, dfn, thm, prp, lem, cor, ...) → cite in `\begin{env}[\cite{Key}]`.
- Narrative envs (expl, example, rem, rmk) → cite in body text.
- Skip obviously original claims unless text says they are adapted from earlier work.

## Search for sources

- Search Google Scholar first.
- Build queries from the environment title, first sentence, and distinctive mathematical terms.
- Verify via Crossref, arXiv, or MathSciNet.
- Prefer the original source for named concepts (e.g. "Drinfeld center" → Drinfeld).
- Prefer peer-reviewed over preprints when content matches.
- Separate low-confidence matches and ask the user before editing.

### Canonical references for this discipline

| Concept | Default key |
|---------|------------|
| Tensor / fusion category | `EGNO15` |
| $E_k$-algebra / $E_k$-operad | `Lur17` |
| Condensation completion | `GJF19` |
| Morita equivalence (classical) | `Morita58` |
| Morita 2-category | `Hau17`, `DR18` |
| Frobenius algebra (in fusion cat) | `FRS02` |
| Center is Morita invariant | `Dav10` |
| Witt equivalence | `DMNO13` |
| Module categories / indecomposable | `Ost03`, `ENO10` |

## Edit BibTeX carefully

- Reuse an existing key when the same DOI / arXiv ID is already present.
- Match the project's key style (typically `AuthorYY`, e.g. `Hau17`, `KZ20a`).
- Include `author`, `title`, `year` + best venue field. Add `doi`, `eprint` when verified.
- Protect capitalisation for proper nouns: `{Tambara--Yamagami}`, `{Drinfeld}`.
- Do not invent metadata.

## Insert citations in TeX

- Statement-style envs → `\begin{thm}[\cite{Key}]` or `\begin{thm}[Title, \cite{Key}]`.
- Narrative envs → cite at the first sentence introducing the sourced fact.
- If a block already has citations, append only genuinely different sources.

## Verify before finishing

- Re-run `python core/scanner.py <root.tex> --config skills/cat-top-order/config.yaml --only-missing --json`.
- Check statement-style citations on the `\begin{...}` line, narrative citations in body.
- Confirm every new BibTeX key is reachable from the bibliography command.
- **Present the full change list to the user for review before applying.**
