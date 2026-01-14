# Agent AI – Job Match & Email Agent

This project demonstrates a multi-agent AI system that autonomously analyzes a resume and job description, evaluates candidate–role fit, and emails a structured report.

## Architecture
- Resume Analyst Agent
- Job Description Analyst Agent
- Match Evaluator Agent
- Email Tool (Gmail SMTP)

## Tech Stack
- Python
- CrewAI
- OpenAI API
- Gmail SMTP

## How it Works
1. Resume and JD are ingested as text
2. Agents collaborate to extract insights
3. Final report is generated and emailed automatically

## How to Run
```bash
pip install -r requirements.txt
python main.py
