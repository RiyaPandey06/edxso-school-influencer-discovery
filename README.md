# School Influencer Discovery Tool (EDXSO AI Intern Assignment)

Reference profile → AI analysis → similar-profile discovery → ranking → explained results.

## Run
```bash
python data/generate_data.py   # regenerate the synthetic test dataset (optional, seeded)
python src/discover.py         # CLI: top-25 for the test reference + precision@20 evaluation (no dependencies)
python build.py                # embeds data into src/app.template.html -> dist.html (the deployable web app)
```
Open `dist.html` in a browser, or deploy it as-is to GitHub Pages / Netlify / Vercel (single static file, no backend).

## Layout
`data/generate_data.py` dataset builder · `data/profiles.json` dataset (schema below) · `src/discover.py` Python engine + evaluation · `src/app.template.html` web app (same algorithm in JS) · `TECHNICAL_NOTE.md` · `DEMO_SCRIPT.md`

## Schema (profiles.json)
`id, name, url, headline, role, org, location, summary, experience[], archetype, gt` (`gt` = relevance label used only for evaluation; never used in ranking).

## Data and compliance
The dataset is **synthetic**: fictional names, placeholder `example.org` URLs. No LinkedIn scraping, no login/CAPTCHA bypass. See the technical note for a compliant production path.
