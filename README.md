# 🏋️ AI Workout Plan Generator

A single-page **Streamlit** app that collects structured fitness inputs and generates a personalised weekly workout plan using an LLM via the **Groq API**.

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a Groq API key

Sign up at <https://console.groq.com> and create a free API key.

### 3. Run the app

```bash
streamlit run app.py
```

Enter your Groq API key in the sidebar, fill in your fitness details, and click **Generate Plan**.

## Features

| Requirement | Status |
|---|---|
| Structured inputs (goal, level, days, equipment, limitations) | ✅ |
| Generate Plan button → day-by-day Markdown plan | ✅ |
| Python function with type hints (`workout_generator.py`) | ✅ |
| Error handling (missing input, API failure, empty response) | ✅ |
| Prompt design respecting all constraints | ✅ |
| **Stretch:** Regenerate button | ✅ |
| **Stretch:** Plan persists in `st.session_state` | ✅ |
| **Stretch:** Download plan as `.md` file | ✅ |
| **Stretch:** Swap an exercise mini-feature | ✅ |

## Project Structure

```
├── app.py                  # Streamlit UI
├── workout_generator.py    # Prompt building + Groq API logic
├── requirements.txt        # Python dependencies
└── README.md
```

## Tech Stack

- **Python 3.12+** — type hints, try/except
- **Streamlit** — interactive UI
- **Groq** — LLM inference (Llama 3.3 70B)
