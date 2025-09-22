import os
import textwrap
import streamlit as st
st.set_page_config(page_title="PRD Outliner")

# --- OpenAI client (env key picked up automatically) ---
try:
    from openai import OpenAI
except Exception as e:
    st.stop()

# Allow key from Streamlit Secrets (recommended on share.streamlit.io)
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="PRD Outliner", page_icon="📝", layout="wide")
st.title("PRD Outliner (MVP)")
st.write("Paste a short problem statement and goal, then generate a PRD outline.")
st.caption("Skeleton app; README explains behavior. API wiring lands next.")
st.caption("Paste a short problem statement and goal → Generate a structured PRD outline.")

with st.sidebar:
    st.subheader("Settings")
    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o"],
        index=0,
        help="Mini is faster/cheaper; 4o is stronger."
    )
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.3, 0.1)
    st.markdown("---")
    st.markdown(
        "If you see a key error, add `OPENAI_API_KEY` in **Advanced settings → Secrets**."
    )

# --- Inputs ---
col1, col2 = st.columns(2)
with col1:
    problem = st.text_area(
        "Problem (1–4 sentences)",
        placeholder="e.g., PMs spend too long staring at blank PRD pages, leading to delays and inconsistent quality…",
        height=160,
    )
with col2:
    goal = st.text_area(
        "Goal (1–3 sentences)",
        placeholder="e.g., Generate a structured, editable PRD outline in <2 minutes that raises baseline PRD quality.",
        height=160,
    )

sections = st.multiselect(
    "Include sections",
    [
        "Context",
        "Users & JTBD",
        "User Stories",
        "Success Metrics",
        "Scope (In/Out)",
        "Requirements",
        "Risks & Assumptions",
        "Open Questions",
        "Launch Plan",
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

def build_prompt(problem_text: str, goal_text: str, selected_sections: list[str]) -> str:
    sec_lines = "\n".join([f"- {s}" for s in selected_sections]) or "- Context"
    return textwrap.dedent(f"""
    You are an experienced Product Manager. Draft a concise, practical **PRD outline** from the inputs below.

    ## Inputs
    - Problem: {problem_text.strip()}
    - Goal: {goal_text.strip()}
    - Sections to include:
    {sec_lines}

    ## Requirements
    - Be specific and concrete; avoid fluff.
    - Keep each section short (bullets welcome).
    - Write in **Markdown** with clear headers (`##`).
    - For **Success Metrics**, include *quantitative* examples.
    - For **User Stories**, include 3–6 well-formed stories (“As a … I want … so that …”).
    - For **Scope (In/Out)**, list crisp bullets.
    - If something is unknown, add it under **Open Questions**.

    Return only the Markdown for the PRD outline—no prefaces or explanations.
    """)

def call_openai(markdown_prompt: str, model: str, temperature: float) -> str:
    client = OpenAI()
    try:
        resp = client.responses.create(
            model=model,
            temperature=temperature,
            input=[
                {
                    "role": "system",
                    "content": "You write crisp, actionable PRD outlines that are easy to copy into docs."
                },
                {"role": "user", "content": markdown_prompt},
            ],
        )
        # New SDK has .output_text; fall back to digging if needed
        return getattr(resp, "output_text", "").strip() or str(resp)
    except Exception as e:
        raise RuntimeError(f"OpenAI error: {e}")

# --- Action ---
if gen_btn:
    if not os.environ.get("OPENAI_API_KEY"):
        st.error("Missing API key. Add `OPENAI_API_KEY` in Streamlit **Advanced settings → Secrets**.")
        st.stop()
    if not problem or not goal:
        st.warning("Please fill in both **Problem** and **Goal**.")
        st.stop()

    with st.spinner("Generating outline…"):
        prompt = build_prompt(problem, goal, sections)
        try:
            md = call_openai(prompt, model=model, temperature=temperature)
        except Exception as err:
            st.error(str(err))
        else:
            st.success("Done! PRD outline generated.")
            st.markdown(md)
            st.download_button(
                "Download Markdown",
                md,
                file_name="prd_outline.md",
                mime="text/markdown",
            )
            st.code(prompt, language="markdown")
