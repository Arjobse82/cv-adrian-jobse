# Adrian Jobse CV site

Plain static site for GitHub Pages, served from the repo root. No build step.

- `index.html`: the CV (skills, ALDI channels, team, tools, experience, contact)
- `work.html`: ALDI work samples, the rollout flow chart (drawn by `scripts/rollout.py`) and the awards list
- `ai-automation.html`: published plugins, Ad Agent (in development), how AI is used, tools
- When the CSS changes, bump `site.css?v=N` in all three pages so browsers don't keep the old one
- `assets/site.css`: the look, a pared-back Monochrome house style (Ad Agent): Inter, #111 ink, greys, one blue
- `assets/work/`: web JPEGs made from the originals in `gitignore/`

## Rules

- Words: load the `trade-copy` skill before writing or editing any copy. Australian spelling.
- Never invent facts, titles, figures or awards. The source notes are in `docs/` (private, not published).
- `gitignore/` (originals) and `docs/` (career notes) stay out of git.
