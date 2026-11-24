"""Streamlit UI for the agent-job-alert project.

Paste a resume and a job description, run the 3 CrewAI agents,
and see the match report in the browser. Email is optional.

Run locally:  streamlit run app.py
Run on EC2:    streamlit run app.py --server.port 8501 --server.address 0.0.0.0
"""

import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Job Match Agent", layout="centered")
st.title("Job Match Agent")
st.write(
    "Paste your resume and a job description. "
    "Three AI agents score the fit and list gaps and fixes."
)

# Optional password gate. Set APP_PASSWORD in .env to turn it on.
# This matters on EC2 because the Streamlit link is public and every
# run spends your OpenAI credits.
app_password = os.getenv("APP_PASSWORD", "")
if app_password:
    gate = st.text_input("App password", type="password")
    if gate != app_password:
        st.warning("Enter the app password to continue.")
        st.stop()

with st.sidebar:
    st.header("Keys")
    st.write("Keys are used only for this run. On EC2 they come from your .env file.")
    openai_key = st.text_input(
        "OpenAI API key", value=os.getenv("OPENAI_API_KEY", ""), type="password"
    )
    gmail_user = st.text_input("Gmail address", value=os.getenv("GMAIL_USER", ""))
    gmail_pw = st.text_input(
        "Gmail app password", value=os.getenv("GMAIL_APP_PASSWORD", ""), type="password"
    )


def _read_default(path):
    """Prefill from resume.txt / jd.txt when they exist in the repo."""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


resume_text = st.text_area(
    "Resume text", value=_read_default("resume.txt"), height=200
)
jd_text = st.text_area(
    "Job description text", value=_read_default("jd.txt"), height=200
)
send_email = st.checkbox("Email me the report", value=True)
run_button = st.button("Run match", type="primary")

if run_button:
    if not openai_key:
        st.error("Add your OpenAI API key in the sidebar first.")
        st.stop()
    if not resume_text.strip() or not jd_text.strip():
        st.error("Paste both your resume and the job description.")
        st.stop()
    if send_email and (not gmail_user or not gmail_pw):
        st.error(
            "Email is on but Gmail details are missing. "
            "Add them in the sidebar or turn email off."
        )
        st.stop()

    os.environ["OPENAI_API_KEY"] = openai_key
    os.environ["GMAIL_USER"] = gmail_user
    os.environ["GMAIL_APP_PASSWORD"] = gmail_pw

    try:
        from crewai import Crew

        from agents import resume_agent, jd_agent, match_agent
        import tasks as tasks_module
    except ImportError as e:
        st.error(f"Missing package: {e}. Run: pip install -r requirements.txt")
        st.stop()

    if not send_email:
        # tasks.py emails the final report through its callback.
        # Replace the sender with a no-op when email is off.
        tasks_module.send_email = lambda subject, body: "Email skipped"

    agents = {"resume": resume_agent, "jd": jd_agent, "match": match_agent}
    task_list = tasks_module.create_tasks(resume_text, jd_text, agents)
    crew = Crew(agents=list(agents.values()), tasks=task_list)

    with st.spinner("Agents are working. This takes 1 to 3 minutes..."):
        try:
            result = crew.kickoff()
        except Exception as e:  # noqa: BLE001 - show the real error to the user
            st.error(f"Run failed: {e}")
            st.stop()

    report = str(result)
    st.success("Done.")
    st.markdown(report)
    st.download_button(
        "Download report", report, file_name="job_match_report.md"
    )
    if send_email:
        st.info("Report also emailed to your Gmail address.")
