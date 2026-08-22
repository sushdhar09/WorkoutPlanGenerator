"""
Streamlit single-page app for AI-powered personalised workout plan generation.

Run with:  streamlit run app.py
"""

import streamlit as st

from workout_generator import generate_workout_plan, swap_exercise

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Workout Planner",
    page_icon="🏋️",
    layout="centered",
)

# ── Session-state defaults ───────────────────────────────────────────────────
if "plan" not in st.session_state:
    st.session_state.plan = ""
if "swap_result" not in st.session_state:
    st.session_state.swap_result = ""

# ── Header ───────────────────────────────────────────────────────────────────
st.title("🏋️ AI Workout Plan Generator")
st.markdown(
    "Fill in your details below and get a **personalised weekly workout plan** "
    "powered by AI."
)

# ── Sidebar — API key ───────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    api_key: str = st.text_input(
        "Groq API Key",
        type="password",
        help="Get a free key at https://console.groq.com",
    )

# ── Structured inputs ───────────────────────────────────────────────────────
st.subheader("Tell us about yourself")

col1, col2 = st.columns(2)

with col1:
    fitness_goal: str = st.selectbox(
        "Fitness goal",
        options=[
            "Build muscle",
            "Lose fat",
            "General fitness",
            "Improve endurance",
        ],
        index=0,
    )

    days_per_week: int = st.slider(
        "Days available per week",
        min_value=1,
        max_value=7,
        value=4,
    )

    height_ft: float = st.number_input(
        "Height (feet)",
        min_value=3.0,  # minimum sensible height
        max_value=8.0,  # maximum sensible height
        step=0.1  # allow decimal precision (e.g., 5.5 ft)
    )

with col2:
    experience_level: str = st.selectbox(
        "Experience level",
        options=["Beginner", "Intermediate", "Advanced"],
        index=0,
    )

    equipment: list[str] = st.multiselect(
        "Equipment access",
        options=["No equipment (bodyweight only)", "Home dumbbells", "Resistance bands", "Full gym"],
        default=["Full gym"],
    )

    weight_kg: float = st.number_input(
        "Weight (kg)",
        min_value=20.0,  # minimum sensible weight
        max_value=300.0,  # maximum sensible weight
        step=0.5 # allow half‑kg increments
    )

limitations: str = st.text_area(
    "Injuries or limitations (optional)",
    placeholder="e.g. bad knees, no overhead pressing, lower-back pain…",
    height=80,
)

# ── Input validation helper ──────────────────────────────────────────────────

def validate_inputs() -> str | None:
    """Return an error message string if inputs are invalid, else None."""
    if not api_key or not api_key.strip():
        return "Please enter your **Groq API key** in the sidebar before generating a plan."
    if not equipment:
        return "Please select at least one **equipment** option."
    if days_per_week < 1 or days_per_week > 7:
        return "**Days per week** must be between 1 and 7."
    return None

# ── Generate / Regenerate buttons ────────────────────────────────────────────
btn_col1, btn_col2 = st.columns([1, 1])

with btn_col1:
    generate_clicked: bool = st.button("🏃 Generate Plan", use_container_width=True)
with btn_col2:
    regenerate_clicked: bool = st.button(
        "🔄 Regenerate Plan",
        use_container_width=True,
        disabled=(st.session_state.plan == ""),
    )

if generate_clicked or regenerate_clicked:
    error_msg = validate_inputs()
    if error_msg:
        st.warning(error_msg)
    else:
        st.session_state.swap_result = ""  # clear old swap result
        with st.spinner("Generating your personalised workout plan…"):
            try:
                plan: str = generate_workout_plan(
                    api_key=api_key.strip(),
                    fitness_goal=fitness_goal,
                    experience_level=experience_level,
                    days_per_week=days_per_week,
                    equipment=equipment,
                    height =height_ft,
                    weight =weight_kg,
                    limitations=limitations,
                )
                st.session_state.plan = plan
            except ValueError as ve:
                st.error(f"⚠️ {ve}")
            except Exception as exc:
                # Covers network errors, auth failures, rate limits, etc.
                st.error(
                    f"❌ **API error:** {exc}\n\n"
                    "Please check your API key, network connection, or try again later."
                )

# ── Display the plan ─────────────────────────────────────────────────────────
if st.session_state.plan:
    st.divider()
    st.subheader("Your Workout Plan")
    st.markdown(st.session_state.plan)

    # ── Download button ──────────────────────────────────────────────────────
    st.download_button(
        label="📥 Download plan as Markdown",
        data=st.session_state.plan,
        file_name="workout_plan.md",
        mime="text/markdown",
    )

    # ── Swap exercise mini-feature ───────────────────────────────────────────
    st.divider()
    st.subheader("🔀 Swap an Exercise")
    swap_name: str = st.text_input(
        "Exercise to swap",
        placeholder="e.g. Barbell Squat",
    )

    if st.button("Swap Exercise"):
        if not swap_name or not swap_name.strip():
            st.warning("Please type the name of the exercise you want to swap.")
        else:
            with st.spinner("Finding an alternative…"):
                try:
                    alt: str = swap_exercise(
                        api_key=api_key.strip(),
                        exercise_name=swap_name.strip(),
                        context=st.session_state.plan,
                    )
                    st.session_state.swap_result = alt
                except ValueError as ve:
                    st.error(f"⚠️ {ve}")
                except Exception as exc:
                    st.error(
                        f"❌ **API error:** {exc}\n\n"
                        "Could not generate a swap. Please try again."
                    )

    if st.session_state.swap_result:
        st.info(st.session_state.swap_result)
