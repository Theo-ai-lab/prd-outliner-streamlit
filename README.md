# PRD Outliner (OpenAI + Streamlit)
**Problem → Outcome:** PMs lose time on blank pages; this drafts a structured PRD outline from a problem + goal.  
**Stack:** Python · Streamlit · OpenAI API (GPT-4o-mini)

## Demo
https://prd-outliner-app-ze5wqndgymjf9knsfuwywz.streamlit.app/
(Screenshot/GIF coming)

## How it works
- **Input →** short problem statement + goal (+ optional section toggles)
- **Logic/Model →** prompt templates with GPT-4o-mini generate an outline
- **Output →** PRD outline (context, users, user stories, metrics, risks, non-goals) with copy-to-Markdown

## Results (v0.1)
- Protocol: initial internal test creating first-draft outlines  
- Score: *(fill Sunday)* ; Notes: top 2 issues → fixes planned

## Try it
1. `pip install -r requirements.txt`
2. `export OPENAI_API_KEY=...`  *(or use a `.env`)*
3. `streamlit run app.py`

## Docs
- **PRD (view-only):** <PASTE_LINK_TO_PRD_OUTLINER_PRD>
- **4-week roadmap:** <PASTE_LINK_TO_PRD_OUTLINER_ROADMAP>
- **Portfolio hub:** <PASTE_LINK_TO_NOTION_PORTFOLIO>

## Changelog
- 2025-08-17: init public repo
