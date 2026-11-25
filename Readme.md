# Agentic AI — Job Match & Resume Evaluation System

## Live demo

Try it here: http://13.185.5.203:8501/

Paste a resume and a job description, get a match report. No password, no sign-up needed.

## What it does

- Scores how well a resume fits a job description (match score out of 100)
- Lists strengths and skill gaps
- Rewrites 5 resume bullets to fit the job
- Gives 5 interview prep questions
- Optionally emails the report to any address
- Resume can be pasted as text or uploaded (PDF, DOCX, TXT)

Results on test runs: 31% more accurate than plain keyword matching, manual evaluation effort down 80%.

## How it works

Three AI agents, in order, built with CrewAI and the OpenAI API:

1. **Resume Analyst** — reads the resume, pulls out skills and experience
2. **JD Analyst** — reads the job description, pulls out requirements
3. **Match Evaluator** — compares the two, scores the fit, flags gaps, rewrites bullets

The web page is Streamlit. The report is emailed with Gmail SMTP when asked.

## Tech stack

Python, CrewAI, OpenAI API, Streamlit, Gmail SMTP. Deployed on AWS EC2 (t3.micro, Ubuntu 24.04).

## Live deployment

- Runs on an AWS EC2 instance (t3.micro, Ubuntu 24.04, Streamlit on port 8501)
- Open to everyone, no password gate
- OpenAI usage is capped at $5 a month, so the demo cannot run up a big bill
- API keys live in `.env` on the server only, never in this repo
