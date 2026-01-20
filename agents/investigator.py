from crewai import Agent

def create_investigator(llm):
    return Agent(
        role="Professional Legal Investigator",
        goal="Provide internal legal and investigative guidance",
        backstory="Senior legal investigator specializing in compliance and fraud cases.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
        max_iter=3,
    )
