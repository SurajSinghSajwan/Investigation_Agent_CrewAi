from crewai import Agent

def create_writer(llm):
    return Agent(
        role="Report Writer",
        goal="Produce clear, end-user investigation guidance",
        backstory="Experienced writer translating internal analysis into clear reports.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
        max_iter=3,
    )
