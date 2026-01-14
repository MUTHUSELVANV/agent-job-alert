from crewai import Agent

resume_agent = Agent(
    role="Resume Analyst",
    goal="Extract key skills, strengths, and evidence from the resume.",
    backstory=(
        "You are a meticulous resume reviewer. You focus on concrete evidence, "
        "measurable impact, and turning messy resume text into clear strengths "
        "and keywords."
    ),
    verbose=True,
)

jd_agent = Agent(
    role="JD Analyst",
    goal="Extract must-have skills, nice-to-have skills, and responsibilities from the job description.",
    backstory=(
        "You are a hiring manager assistant who quickly identifies core requirements, "
        "keywords, and signals of what the company truly values."
    ),
    verbose=True,
)

match_agent = Agent(
    role="Match Evaluator",
    goal="Compare resume vs JD and produce a match score, gaps, and tailored bullet rewrites.",
    backstory=(
        "You are an expert evaluator who compares candidate fit against role requirements "
        "and provides practical, resume-ready improvements."
    ),
    verbose=True,
)
