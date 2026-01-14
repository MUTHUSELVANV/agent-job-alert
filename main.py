import os
from dotenv import load_dotenv
from crewai import Crew

from agents import resume_agent, jd_agent, match_agent
from tasks import create_tasks

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def main():
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Missing OPENAI_API_KEY in .env")

    resume = read_file("resume.txt")
    jd = read_file("jd.txt")

    agents = {"resume": resume_agent, "jd": jd_agent, "match": match_agent}
    tasks = create_tasks(resume, jd, agents)

    crew = Crew(agents=list(agents.values()), tasks=tasks)
    crew.kickoff()

if __name__ == "__main__":
    main()
