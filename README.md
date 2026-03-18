# Citation Skill

A collection of per-discipline **citation-adding skills** for LaTeX manuscripts.

Each skill follows a shared scaffold but is specialized for the citation conventions, environment names, source databases, and reference styles of its target research area.

## Disciplines

| Skill | Directory | Description |
|-------|-----------|-------------|
| Categorical Topological Order | `skills/cat-top-order/` | Higher category theory, fusion categories, topological phases |
| High-Energy / String Theory | `skills/hep-th/` | String theory, QFT, SUSY, AdS/CFT |
| *(more to come)* | | |

## Usage

1. Copy the desired `skills/<discipline>/` directory into your LaTeX project.
2. The agent reads `SKILL.md` + `config.yaml` and runs the scanner automatically.
3. **Optional Citations**: Borderline cases (e.g., standard background review) are categorized as Optional (★★★☆☆) so they are not silently discarded.
4. **Review and Apply**: The final citation diff is presented to the user for review before applying changes to `.tex` and `.bib` files.

## Architecture

```
citation_skill/
├── core/              # shared scanner, bib tools, source lookup
│   ├── scanner.py
│   ├── strategies/    # env / pattern / section scan plugins
│   ├── bib_utils.py
│   ├── scholar.py
│   └── verify.py
├── skills/            # per-discipline skills
│   ├── cat-top-order/
│   ├── hep-th/
│   └── ...
├── templates/         # skill scaffolding templates
└── docs/              # contributing guide, taxonomy
```

## Adding a New Discipline

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).
