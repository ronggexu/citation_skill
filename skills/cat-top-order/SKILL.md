---
name: add-citation-cat-top-order
description: >
  Find authoritative sources for claims, theorems, and definitions in
  Category Theory / Topology / Order Theory LaTeX manuscripts. Use MathSciNet,
  nLab, or Google Scholar for bibliography data and insert citations
  following mathematical conventions.
---
<!-- // turbo-all -->

# Add citations — Category Theory / Topology / Order Theory (cat-top-order)

## Start from the active LaTeX root

- Read the root document before editing anything.
- **Follow `\input{...}` directives recursively** — lengthy mathematical papers often split chapters/sections into multiple files. Scan every input file.
- **Inspect the preamble** (or a `preamble.tex` if `\input`-ed):
  - Detect `\bibliography{...}` or `\addbibresource{...}` and write BibTeX to the file already in the build.
  - Note `\newtheorem{...}` declarations — in pure mathematics, it is very common to state another author's known result in a theorem environment, explicitly attributing it in the optional argument (e.g. `\begin{thm}[Mac Lane \cite{Mac98}]`).

## Scan for citable blocks

Category theory and topology papers frequently use **theorem environments** to state both new results and known facts. Unlike physics, if a known result is stated as a theorem/proposition, it **must** be cited, typically in the environment header.

Scan the **body text** for the following patterns:

1. **Theorem/Proposition/Lemma Headers**:
   - If the text introduces a classical or known result in an environment without a citation, flag it. Example: "The following result is due to Joyal." followed by `\begin{thm}` without a `\cite` in the optional argument.

2. **Attribution phrases and prose**:
   - "It is a classical result that", "By a theorem of", "As proved in", "Following the terminology of", "The notion of X was introduced by".
   - "Recall that", "We briefly review the theory of".
   - "by the Morita theory", "by the Baez-Dolan cobordism hypothesis", "by the Yoneda lemma" — named mathematical results always require their canonical citation unless fundamentally textbook (e.g., Yoneda lemma is borderline textbook, but specific higher-categorical versions require citations).

3. **Definitions and Concepts**:
   - When a specific, non-trivial mathematical object is defined (e.g. "A *fusion category* is a...", "A *condensable $\mathbb{E}_k$-algebra* is..."), the foundational paper introducing that concept should often be cited if it's the main subject of the section.

4. **Empty `\cite{}` placeholders** or TODO markers left by the author.

## Search for sources

- **MathSciNet / zbMATH first** (if accessible via web search) — preferred for rigorous mathematical metadata.
- **Google Scholar** / **nLab** — use web search to find exact theorems or categorical constructions (nLab is especially authoritative for higher category theory references).
- **arXiv** cross-check for recent preprints.
- **Do not silently discard borderline cases**. If a concept is borderline textbook but might benefit from a citation, include it in the final diff as **Optional** with a lower confidence rating (e.g., ★★★☆☆).
- Separate high-confidence and optional matches clearly and ask the user which to apply.

## Edit BibTeX carefully

- Use a standard author-year or alphanumeric key style depending on the manuscript's existing `.bib` conventions (e.g., `MacLane1998` or `LurieHA`). If the user already has a style, strictly adhere to it.
- Import full BibTeX records. Include `doi`, `journal`, or `publisher` fields.
- Include `eprint` for arXiv preprints.
- Protect special characters and proper nouns in titles (e.g. `{Galois}`, `{$\infty$-categories}`).
- Do not invent metadata.

## Insert citations in TeX

cat-top-order convention: citations are often placed in **theorem headers** or **inline**.

Typical placement patterns:

| Pattern | Example |
|---------|---------|
| Theorem optional argument | `\begin{thm}[Lurie \cite{LurieHA}, Theorem 4.1.2]` |
| Inline attribution | `By a result of Joyal \cite{Joyal02}, the category...` |
| End of sentence | `...form a symmetric monoidal $\infty$-category \cite{LurieHA}.` |
| Specific pointer | `\cite[Proposition 3.2]{AuthorYear}` |

Rules:
- If a specific theorem or proposition from a book/long paper is invoked, **always try to include a specific pointer** in the optional argument of the `\cite` command (e.g., `\cite[Theorem 2.1]{Key}`). Pure math requires precise pointers for lengthier texts.
- When stating a known theorem in an environment, place the citation in the optional argument: `\begin{thm}[\cite{Key}]`.
- Use `~\cite{Key}` (with tilde) before inline citations to prevent line breaks.
- Use a single `\cite{K1,K2}` rather than `\cite{K1}\cite{K2}`.

## Verify and apply

- Re-run `python core/scanner.py <root.tex> --config skills/cat-top-order/config.yaml --only-missing --json` (if applicable).
- Check that every new BibTeX key is reachable from the bibliography command.
- **Present the full change list to the user for review** using `notify_user` with `BlockedOnUser=true`. Wait for the user to confirm which changes to adopt.
- **After user confirms**, apply all approved edits in the same conversation: add BibTeX entries to `.bib` and insert `\cite` commands into `.tex`.
