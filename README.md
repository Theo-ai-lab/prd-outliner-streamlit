# PRD Outliner (MVP) – OpenAI + Streamlit

Prototype to streamline PRD drafting: paste a short problem + goal → generate a structured PRD outline in under 2 minutes.

---

# Demo
- Live app: https://prd-outliner-app-ze5wqndgymjf9knsfuwywz.streamlit.app

<img src="assets/hero.png" width="800" />
<img src="assets/result.png" width="800" />

---

# How it works
- Input → short problem statement + goal (+ optional section toggles)  
- Logic/Model → prompt templates with `gpt-4o-mini` / `gpt-4o`  
- Output → PRD outline (context, users, user stories, metrics, scope, risks) with Copy + Download Markdown

---

# Results (v0.1)
- Protocol: 8 internal runs across varied inputs (short/long, both `gpt-4o-mini` and `gpt-4o`).
- Outcome: 7/8 runs (87.5%) produced structured, usable PRD outlines.
- Failure mode: repeated headers and truncation on very long inputs.
- Fixes applied: tightened prompt to suppress prefatory text; added spinner + input length hint.

---

# Try it
pip install -r requirements.txt

# Option A (Streamlit Cloud): set key in Settings → Secrets as OPENAI_API_KEY
# Option B (local .streamlit/secrets.toml)
mkdir -p .streamlit && printf "OPENAI_API_KEY = \"sk-...\"\n" > .streamlit/secrets.toml

streamlit run app.py

# Docs
- [PRD (view-only)](https://www.notion.so/your-prd-link)
- [4-week roadmap](https://www.notion.so/your-roadmap-link)
- [Portfolio hub](https://www.notion.so/your-portfolio-hub)

# Changelog
- 2025-09-17: Init public repo
- 2025-09-18: Added input validation (Problem/Goal required)
- 2025-09-19: Added “Copy to Clipboard” button
- 2025-09-20: Added “Show Prompt (debug)” expander
- 2025-09-21: Uploaded screenshots (hero.png, result.png) → added to README Demo
- 2025-09-22: Polished README (Results v0.1, Docs links placeholders)
