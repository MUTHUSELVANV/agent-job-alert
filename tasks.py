from crewai import Task
from tools.email_tool import send_email


def create_tasks(resume_text: str, jd_text: str, agents: dict):
    t1 = Task(
        description=f"""
Analyze this resume. Output:
1) Top skills (bullets)
2) Domain/industry strengths (bullets)
3) 3 strongest resume lines (quote them)
RESUME:
{resume_text}
""".strip(),
        expected_output=(
            "Bulleted list of top skills; bulleted list of domain strengths; "
            "three quoted resume lines with a 1-line explanation for each."
        ),
        agent=agents["resume"],
    )

    t2 = Task(
        description=f"""
Analyze this job description. Output:
1) Must-have skills (bullets)
2) Nice-to-have skills (bullets)
3) Key responsibilities (bullets)
JOB DESCRIPTION:
{jd_text}
""".strip(),
        expected_output=(
            "Bulleted must-have skills; bulleted nice-to-have skills; "
            "bulleted responsibilities; include important keywords."
        ),
        agent=agents["jd"],
    )

    t3 = Task(
        description="""
Using the resume analysis and JD analysis, produce a single clean Markdown report:
- Match score 0-100 + 1-line justification
- Top strengths for this role (bullets)
- Skill gaps (bullets)
- 5 tailored resume bullet rewrites (bullets, quantified where possible)
- 5 interview prep questions for this JD (bullets)
""".strip(),
        expected_output=(
            "A Markdown report with: match score, strengths, gaps, 5 rewritten bullets, "
            "and 5 interview questions."
        ),
        agent=agents["match"],
        # Email the final report
        callback=lambda output: send_email("Job Match Agent Result", str(output)),
    )

    return [t1, t2, t3]
