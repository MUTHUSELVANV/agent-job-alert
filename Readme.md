# 🤖 Agent AI – Job Match & Email Agent

This project demonstrates a **multi-agent AI system** that autonomously analyzes a resume and job description, evaluates candidate–role fit, and emails a structured, actionable report.

---

## 🧠 Architecture
- **Resume Analyst Agent** – extracts skills, strengths, and experience  
- **Job Description Analyst Agent** – identifies role requirements and priorities  
- **Match Evaluator Agent** – computes fit score, gaps, and recommendations  
- **Email Tool** – delivers results via Gmail SMTP  

---

## 🛠 Tech Stack
- Python  
- CrewAI (multi-agent orchestration)  
- OpenAI API (LLM reasoning)  
- Gmail SMTP (email delivery)  

---

## ⚙️ How It Works
1. Resume and job description are ingested as text  
2. Agents collaborate to extract insights and evaluate fit  
3. A structured report (score, strengths, gaps, recommendations) is generated  
4. The final output is emailed automatically to the user  

---

## ▶️ How to Run

### 0️⃣ Prerequisites
- Python 3.10+ (recommended)
- OpenAI API key
- Gmail App Password (16-character app password)

---

### 1️⃣ Install dependencies
pip install -r requirements.txt

---

### 2️⃣ Create a .env file (required)

Create a file named .env in the project root (same folder as main.py).<br>
OPENAI_API_KEY=
GMAIL_USER=
GMAIL_APP_PASSWORD=

---

### 3️⃣ Add inputs
Update the following files with your content:
resume.txt – paste your resume text
jd.txt – paste the job description

### 4️⃣ Run the project
python main.py

You will receive an email containing the job match report.
