import os
import yaml
from crewai import Agent, Task, Crew, Process
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"

with open(CONFIG_DIR / "agents.yaml", "r") as f:
    agent_config = yaml.safe_load(f)

with open(CONFIG_DIR / "tasks.yaml", "r") as f:
    task_config = yaml.safe_load(f)


email_summarizer = Agent(
    role=agent_config["email_summarizer"]["role"],
    goal=agent_config["email_summarizer"]["goal"],
    backstory=agent_config["email_summarizer"]["backstory"],
    llm=gemini_llm
)

email_qa_expert = Agent(
    role=agent_config["email_qa_expert"]["role"],
    goal=agent_config["email_qa_expert"]["goal"],
    backstory=agent_config["email_qa_expert"]["backstory"],
    llm=gemini_llm
)

summarize_task = Task(
    description=task_config["summarize_email"]["description"],
    expected_output=task_config["summarize_email"]["expected_output"],
    agent=email_summarizer,
)

qa_task = Task(
    description=task_config["answer_email_question"]["description"],
    expected_output=task_config["answer_email_question"]["expected_output"],
    agent=email_qa_expert,
)

def build_crew(mode="summarize"):
    if mode == "qa":
        return Crew(agents=[email_qa_expert], tasks=[qa_task], process=Process.sequential)
    return Crew(
        agents=[email_summarizer],
        tasks=[summarize_task],
        process=Process.sequential
    )