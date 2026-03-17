# Contributing a New Discipline Skill

## Quick Start

1. **Copy the templates**:
   ```
   cp templates/SKILL_TEMPLATE.md   skills/<your-discipline>/SKILL.md
   cp templates/config_template.yaml skills/<your-discipline>/config.yaml
   ```

2. **Edit `config.yaml`**:
   - Set `name`, `display_name`, `description`
   - Choose scan strategies (env / pattern / section)
   - Define the environment names or regex patterns
   - Set source databases and arXiv categories
   - Define the bib key style
   - Add canonical references table

3. **Edit `SKILL.md`**:
   - Write discipline-specific citation placement rules
   - Add a canonical references table
   - Add any special handling notes

4. **Add examples** to `skills/<your-discipline>/examples/` with a sample `.tex` file.

5. **Test**: Run the scanner on your example file:
   ```
   python core/scanner.py examples/sample.tex --config skills/<your-discipline>/config.yaml --json
   ```

## Scan Strategies

| Strategy | Best for | Config key |
|----------|----------|------------|
| `env` | Math papers with `\begin{thm}...\end{thm}` | `type: env` |
| `pattern` | Physics papers with inline claims | `type: pattern` |
| `section` | Papers with review / background sections | `type: section` |
| `equation` | Papers where key equations need citations | `type: equation` |

You can activate **multiple strategies** for a single discipline.

## UX Principle

All scanning and verification commands use `// turbo` annotation so they run
without user approval. **The only user-facing gate is the final citation diff.**
