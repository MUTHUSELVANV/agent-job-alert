"""Streamlit UI for the agent-job-alert project.

Paste or upload a resume, paste a job description, run the 3 CrewAI
agents, and see the match report in the browser. Email is optional.

Keys come only from the .env file on the server. They are never
shown in the UI, so visitors cannot see or change them.

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

# Keys come only from .env on the server. They are never shown in the
# UI, so visitors cannot see or change them.
openai_key = os.getenv("OPENAI_API_KEY", "")
gmail_user = os.getenv("GMAIL_USER", "")
gmail_pw = os.getenv("GMAIL_APP_PASSWORD", "")


def _read_default(path):
    """Prefill from resume.txt / jd.txt when they exist in the repo."""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def _read_uploaded_resume(uploaded):
    """Read text from an uploaded resume file (pdf, docx, or txt)."""
    name = uploaded.name.lower()
    try:
        if name.endswith(".txt"):
            return uploaded.read().decode("utf-8", errors="ignore")
        if name.endswith(".pdf"):
            import pdfplumber

            parts = []
            with pdfplumber.open(uploaded) as pdf:
                for page in pdf.pages:
                    parts.append(page.extract_text() or "")
            return "\n".join(parts)
        if name.endswith(".docx"):
            import docx

            doc = docx.Document(uploaded)
            return "\n".join(p.text for p in doc.paragraphs)
    except ImportError:
        st.error(
            "A file reader is missing on the server. "
            "Run: pip install -r requirements.txt"
        )
    except Exception as e:  # noqa: BLE001 - show the real error to the user
        st.error(f"Could not read that file: {e}")
    return ""


resume_mode = st.radio(
    "How to add your resume",
    ["Paste text", "Upload file"],
    horizontal=True,
)
resume_text = ""
if resume_mode == "Paste text":
    resume_text = st.text_area(
        "Resume text", value=_read_default("resume.txt"), height=200
    )
else:
    uploaded = st.file_uploader(
        "Upload your resume", type=["pdf", "docx", "txt"]
    )
    if uploaded is not None:
        resume_text = _read_uploaded_resume(uploaded)
        if resume_text.strip():
            st.text_area(
                "Resume text (from file)",
                value=resume_text,
                height=200,
                disabled=True,
            )
        else:
            st.warning(
                "Could not read any text from that file. Try another file."
            )
jd_text = st.text_area(
    "Job description text", value=_read_default("jd.txt"), height=200
)
send_email = st.checkbox("Email me the report", value=True)
report_to = ""
if send_email:
    report_to = st.text_input(
        "Send report to",
        value=gmail_user,
        help="The report is sent from your Gmail account to this address.",
    )
run_button = st.button("Run match", type="primary")

if run_button:
    if not openai_key:
        st.error(
            "OpenAI API key is missing on the server. "
            "Add OPENAI_API_KEY to the .env file on EC2."
        )
        st.stop()
    if not resume_text.strip() or not jd_text.strip():
        st.error("Add your resume and the job description first.")
        st.stop()
    if send_email and (not gmail_user or not gmail_pw):
        st.error(
            "Email is on but Gmail details are missing on the server. "
            "Add GMAIL_USER and GMAIL_APP_PASSWORD to the .env file on EC2, "
            "or turn email off."
        )
        st.stop()
    if send_email and "@" not in report_to:
        st.error("Enter a valid email address to send the report to.")
        st.stop()

    os.environ["OPENAI_API_KEY"] = openai_key
    os.environ["GMAIL_USER"] = gmail_user
    os.environ["GMAIL_APP_PASSWORD"] = gmail_pw
    os.environ["REPORT_EMAIL_TO"] = report_to

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
        st.info(f"Report also emailed to {report_to}.")
