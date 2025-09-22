# app.py
import os
import json
import textwrap
import html
import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

# ── OpenAI client (read key from Streamlit Secrets, or env if running locally)
def get_client() -> OpenAI:
    # Prefer Streamlit Secrets in Streamlit Cloud
    if "OPENAI_API_KEY" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    # Construct client (OpenAI lib reads key from env)
    return OpenAI()

st.set_page_config(page_title="PRD Outliner", page_icon="📝", layout="wide")
st.title("PRD Outliner (MVP)")
st.caption("Paste a short problem statement and goal → Generate a structured PRD outline.")

# ── Sidebar: settings
with st.sidebar:
    st.subheader("Settings")
    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o"],  # default first
        index=0,
        help="Mini is faster/cheaper; 4o is stronger."
    )
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.30, 0.1)
    st.markdown("---")
    st.markdown(
        "If you see a key error, add "
        "`OPENAI_API_KEY` in **Advanced settings → Secrets**."
    )

# ── Inputs
col1, col2 = st.columns(2)
with col1:
    problem = st.text_area(
        "Problem (1–4 sentences)",
        placeholder="e.g., PMs waste time creating product requirement documents from scratch, leading to delays.",
        height=140,
    )
with col2:
    goal = st.text_area(
        "Goal (1–3 sentences)",
        placeholder="e.g., Generate a clear PRD outline in under 2 minutes that improves consistency and quality.",
        height=140,
    )

sections = st.multiselect(
    "Include sections",
    [
        "Context",
        "Users & JTBD",
        "User Stories",
        "Success Metrics",
        "Scope (In/Out)",
        "Risks & Assumptions",
        "Open Questions",
        "Launch Plan",
        "Requirements",
    ],
    default=[
        "Context",
        "Users & JTBD",
        "User Stories",
        "Success Metrics",
        "Scope (In/Out)",
        "Risks & Assumptions",
    ],
)

gen_btn = st.button("Generate PRD Outline", type="primary")

# ── Prompt builder (shown under an expander after generation)
def build_prompt(problem_text: str, goal_text: str, selected_sections: list[str]) -> str:
    sec_lines = "\n- ".join([s for s in selected_sections]) or "Context"
    return textwrap.dedent(f"""
        You are an experienced Product Manager. Draft a concise, practical **PRD outline** from the inputs below.

        ## Inputs
        - **Problem**: {problem_text.strip()}
        - **Goal**: {goal_text.strip()}
        - **Sections to include**:
        - {sec_lines}

        ## Requirements
        - Be specific and concrete; avoid fluff.
        - Keep each section short (bullets welcome).
        - Write in **Markdown** with clear headers (`##`).
        - For **Success Metrics**, include **quantitative** examples.
        - For **User Stories**, include 3–6 well-formed stories (“As a … I want … so that …”).
        - For **Scope (In/Out)**, list crisp bullets.
        - If something is unknown, add it under **Open Questions**.

        Return only the Markdown for the PRD outline—no prefaces or explanations.
    """).strip()

def call_openai(markdown_prompt: str, model_name: str, temp: float) -> str:
    client = get_client()
    try:
        resp = client.responses.create(
            model=model_name,
            temperature=temp,
            input=[
                {"role": "system",
                 "content": "You write crisp, actionable PRD outlines that are easy to copy into docs."},
                {"role": "user", "content": markdown_prompt},
            ],
        )
        # New SDK: use output_text if present; else fallback
        return getattr(resp, "output_text", "").strip() or str(resp)
    except Exception as e:
        raise RuntimeError(f"OpenAI error: {e}")

# ── Action
if gen_btn:
    # 1) Validation
    if not os.environ.get("OPENAI_API_KEY") and "OPENAI_API_KEY" not in st.secrets:
        st.error("Missing API key. Add `OPENAI_API_KEY` in Streamlit **Advanced settings → Secrets**.")
        st.stop()
    if not problem or not goal:
        st.warning("Please fill in both **Problem** and **Goal** before generating.")
        st.stop()

    with st.spinner("Generating outline…"):
        prompt = build_prompt(problem, goal, sections)
        try:
            md = call_openai(prompt, model, temperature)
        except Exception as err:
            st.error(str(err))
        else:
            st.success("Done! PRD outline generated.")
            st.markdown(md)

            # Download Markdown
            st.download_button(
                "Download Markdown",
                md,
                file_name="prd_outline.md",
                mime="text/markdown",
                use_container_width=False,
            )

            # Copy to clipboard (works in Streamlit Cloud using a tiny JS snippet)
            if st.button("Copy to clipboard", type="secondary"):
                # escape + JSON-encode to safely inject into <script>
                encoded = json.dumps(md)
                components.html(
                    f"""
                    <script>
                      const txt = {encoded};
                      navigator.clipboard.writeText(txt).then(
                        () => {{ window.parent.postMessage({{"stToast":"copied"}}, "*"); }},
                        () => {{ window.parent.postMessage({{"stToast":"failed"}}, "*"); }}
                      );
                    </script>
                    """,
                    height=0,
                )
                st.toast("Copied outline to clipboard ✅", icon="✅")

            # Prompt preview (debug) inside an expander
            with st.expander("Show prompt (debug)"):
                st.code(prompt, language="markdown")
