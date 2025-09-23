# PRD Outliner (OpenAI + Streamlit)

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
- Outcome: 7 / 8 runs (87.5%) produced usable PRD outlines (structured, no prefatory text).
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
- PRD (view-only): [Notion Link](https://www.notion.so/your-prd-link)
- 4-week roadmap: [Notion Link](https://www.notion.so/your-roadmap-link)
- Portfolio hub: [Notion Link](https://www.notion.so/your-portfolio-hub)

# Changelog
- 2025-09-22: init public repo
