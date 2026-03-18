---
name: add-citation-hep-th
description: >
  Find authoritative sources for claims, equations, and review passages in
  high-energy physics / string theory LaTeX manuscripts. Use INSPIRE-HEP
  for bibliography data and insert citations in body text following hep-th
  conventions.
---
<!-- // turbo-all -->

# Add citations — High-Energy / String Theory (hep-th)

## Start from the active LaTeX root

- Read the root document before editing anything.
- **Follow `\input{...}` directives recursively** — hep-th papers commonly
  split content across `Section1.tex`, `Section2.tex`, `appendixA.tex`, etc.
  Scan every input file as part of the full document.
- **Inspect the preamble** (or a `preamble.tex` if `\input`-ed):
  - Detect `\bibliography{...}` or `\addbibresource{...}` and write BibTeX
    to the file already in the build.
  - Note any **custom equation macros** (e.g. `\def\longeq`, `\def\lceq`,
    `\def\be`/`\ee`) — these wrap `equation`/`aligned` environments and
    must be treated as equation blocks during scanning.
  - Note `\newtheorem{...}` declarations — in hep-th, author-defined
    theorem environments (`theorem`, `prop`, `defn`, `lem`) almost always
    contain **original** results. Do **not** add citations to them unless
    the surrounding text explicitly says the result is adapted or reproved
    from earlier work.
- Prefer an existing local `.bib` file over a shared one.
- Preserve the citation macro style already used in the project.

## Scan for citable blocks

hep-th papers **rarely use theorem environments** for citing known results.
Theorem / Proposition environments typically state the author's own original
results and should **not** receive citations unless the text explicitly says
the result is adapted or reproved from earlier work.

Instead, scan the **body text** for the following patterns:

1. **Attribution phrases** — sentences containing:
   - "it is well known that", "it was shown in", "as shown in",
     "as proved by", "following reference", "were introduced in",
     "was first studied in", "has been studied in", "see also",
     "see for example", "for a nice exposition", "for a recent discussion".
   - "it is proposed that", "it was proposed in", "it has been proposed",
     "has been considered in", "motivated by", "inspired by".
   - "known as the X formula/conjecture/identity/correspondence" — named
     results that deserve their eponymous citation.
   - "we follow the conventions/notation of", "using the formalism
     developed in", "following the approach in" — methodological
     attributions.
   - Empty `\cite{}` placeholders or `\gc` markers left by the author.

2. **Review / Background sections** — entire `\section{Review}`,
   `\section{Introduction}`, `\subsection{Preliminaries}`, or sections
   whose prose summarizes known material (definitions, established
   equations, prior constructions). These sections are typically
   citation-dense; check every paragraph for uncited claims.
   - Also scan **unnumbered subsections** (`\subsection*{...}`,
     `\subsubsection*{...}`) that introduce known parametrizations,
     standard constructions, or asymptotic results — these are frequently
     used in hep-th to present review material without incrementing
     section counters.

3. **Key equations from the literature** — `\begin{equation}` /
   `\begin{align}` blocks (including custom wrappers like `\lceq`,
   `\longeq`, `\be`/`\ee`) that reproduce previously-known results.
   Look for surrounding text cues like "the well-known relation",
   "which was derived in", "one can show [cite]", "yields a universal
   expression ... known as", or a `\label` whose name suggests a named
   result (e.g. `\label{eq:WZW}`, `\label{eq:KZ}`,
   `\label{eq:Cardy_formula}`).

4. **Paragraph-level claims** — standalone `\paragraph{...}` headings
   that introduce known constructions (e.g. `\paragraph{Relation to
   topological strings.}`). The subsequent discussion is usually review
   material referencing specific prior work.

5. **Named results and identities** — when the text uses a proper name
   (e.g. "Cardy formula", "Polyakov-Wiegmann identity", "AGT
   correspondence", "Virasoro TQFT", "Argyres-Douglas SCFTs"),
   the eponymous or canonical paper should be cited. If the name
   appears without a `\cite`, flag it.

6. **Footnotes with claims** — `\footnote{...}` blocks may contain
   factual claims or clarifications that reference known results without
   an attached citation (e.g. "We emphasize that Liouville theory is
   not a holographic 2D CFT…; see \cite{...}"). Scan footnotes too.

- Run `python core/scanner.py <root.tex> --config skills/hep-th/config.yaml --json`.

## Search for sources

- **Google Scholar first** — use web search (no browser needed) to quickly
  identify candidate papers. Build queries from: the key equation or
  construction name, distinctive physics terms, and author surnames
  mentioned in surrounding text.
- **INSPIRE-HEP second** — use INSPIRE for retrieving the canonical BibTeX
  key (`LastName:YYxx`) and full BibTeX entry. This can be done via the
  INSPIRE API (`inspirehep.net/api/literature?q=...`) without opening a
  browser.
- Cross-check with **arXiv** for preprint metadata when needed.
- Prefer the published journal version over preprints when both exist.
- For named results (e.g. "Cardy formula", "ETH"), search for the
  canonical/original paper rather than review articles.
- **Do not silently discard borderline cases** (e.g., background intro
  sentences that could use citations, or claims that use a review article
  but might benefit from citing the original source). Include them in the
  final diff as **Optional** with a lower confidence rating (e.g., ★★★☆☆).
- Separate high-confidence and optional matches clearly and ask the user
  which to apply.

## Edit BibTeX carefully

- Use INSPIRE key style: `LastName:YYxx` (e.g. `Maldacena:1997re`,
  `Gaiotto:2012sf`, `Collier:2023fwi`).
- Reuse an existing key when the same DOI / arXiv eprint is already present.
- Import full BibTeX records from INSPIRE when available.
- Include `reportNumber` and `eprint` fields for arXiv papers.
- Protect special characters and proper nouns in titles
  (e.g. `{Knizhnik-Zamolodchikov}`, `{Liouville}`, `{Virasoro}`).
- Do not invent metadata.

## Insert citations in TeX

hep-th convention: cite **inline in body text**, not in environment
optional-argument brackets.

Typical placement patterns (observed in real hep-th manuscripts):

| Pattern | Example |
|---------|---------|
| End of sentence stating a known result | `...the AGT correspondence \cite{Alday:2009aq}.` |
| Attribution phrase | `As was shown in \cite{Haghighat:2023vzu,Gukov:2024adb}, ...` |
| Parenthetical, non-essential | `(see for example \cite{Bonelli:2016qwg} for a nice exposition)` |
| Named result (eponymous) | `...known as the Cardy formula~\cite{Cardy:1986ie}` |
| After an equation block | equation env → `which was derived in \cite{Key}.` |
| Clustered multi-cite | `\cite{Saad:2019lba,Mertens:2020hbs,Collier:2023fwi}` |
| Footnote (tangential) | `\footnote{...see~\cite{Chen:2024unp} for detailed discussion.}` |
| Self-citation chain | `In~\cite{Chen:2022wvy, Cheng:2023kxh}, we proposed ...` |

Rules:
- Place `\cite{Key}` at the **end of the sentence** stating the known result,
  before the period.
- When citing multiple sources for one claim, use a single `\cite{K1,K2,...}`
  rather than multiple `\cite` commands.
- Use `~\cite{Key}` (with tilde) before the cite to prevent line breaks
  between the preceding word and the citation — this is standard hep-th
  style.
- For key equations reproduced from the literature, cite immediately after
  the equation environment in the following sentence.
- Use `\footnote{...\cite{Key}}` for tangential references that would
  otherwise break reading flow — this is more common in hep-th than in
  pure mathematics.
- Do **not** add citations inside `\begin{theorem}[...]` or
  `\begin{prop}[...]` optional arguments — these environments typically
  contain the author's own results in hep-th papers.

## Verify and apply

- Re-run `python core/scanner.py <root.tex> --config skills/hep-th/config.yaml --only-missing --json`.
- Confirm all INSPIRE keys resolve correctly (check against INSPIRE or arXiv).
- Check that every new BibTeX key is reachable from the bibliography command.
- **Present the full change list to the user for review** using
  `notify_user` with `BlockedOnUser=true`. Wait for the user to confirm
  which changes to adopt.
- **After user confirms**, apply all approved edits in the same
  conversation: add BibTeX entries to `.bib` and insert `\cite` commands
  into `.tex`.


