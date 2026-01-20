import time
from datetime import datetime
from crewai import Crew, Task, Process
from agents.investigator import create_investigator
from agents.writer import create_writer
from logging_config import setup_logger
from utils.token_usage import extract_token_usage
from utils.cli import crew_start, crew_done, agent_start, agent_done, run_separator

logger = setup_logger() 

def build_crew(llm, user_query, investigation_id, streamlit_session_id):
    run_id = datetime.utcnow().strftime("%Y%m%d-%H%M%S")

    run_separator()
    crew_start(run_id, investigation_id)

    logger.info(
        "Crew execution started",
        extra={"extra_data": {
            "investigation_id": investigation_id,
            "session_id": streamlit_session_id,
            "run_id": run_id,
        }},
    )

    crew_start_time = time.perf_counter()
    total_tokens = 0

    investigator_output, investigator_metrics = _run_investigator(
        llm, user_query, investigation_id, streamlit_session_id
    )
    total_tokens += investigator_metrics["total_tokens"]

    writer_output, writer_metrics = _run_writer(
        llm, investigator_output, investigation_id, streamlit_session_id
    )
    total_tokens += writer_metrics["total_tokens"]

    crew_duration = time.perf_counter() - crew_start_time

    crew_done(crew_duration, total_tokens)
    run_separator()
    print()

    logger.info(
        "Crew execution completed",
        extra={"extra_data": {
            "investigation_id": investigation_id,
            "session_id": streamlit_session_id,
            "run_id": run_id,
            "duration_sec": round(crew_duration, 2),
            "total_tokens": total_tokens,
            "investigator": investigator_metrics,
            "writer": writer_metrics,
        }},
    )

    return writer_output


def _run_investigator(llm, user_query, investigation_id, session_id):
    investigator = create_investigator(llm)

    task = Task(
        description=f"""
Analyze the investigation query from a legal and compliance perspective.

Query:
{user_query}
""",
        expected_output="Internal investigation guidance.",
        agent=investigator,
    )

    crew = Crew(
        agents=[investigator],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    logger.info(
        "Investigator execution started",
        extra={"extra_data": {
            "investigation_id": investigation_id,
            "session_id": session_id,
            "agent": "investigator",
        }},
    )

    agent_start("investigator")

    start = time.perf_counter()
    output = crew.kickoff()
    duration = time.perf_counter() - start

    tokens = extract_token_usage(output)

    agent_done(
        agent="investigator",
        duration=duration,
        total_tokens=tokens["total_tokens"],
    )

    logger.info(
        "Investigator execution completed",
        extra={"extra_data": {
            "investigation_id": investigation_id,
            "session_id": session_id,
            "agent": "investigator",
            "duration_sec": round(duration, 2),
            **tokens,
        }},
    )

    return output.raw, {
        "duration_sec": round(duration, 2),
        **tokens,
    }


def _run_writer(llm, investigator_output, investigation_id, session_id):
    writer = create_writer(llm)

    task = Task(
        description=f"""
Produce a clear end-user response using the internal guidance below.

{investigator_output}
""",
        expected_output="End-user investigation guidance.",
        agent=writer,
    )

    crew = Crew(
        agents=[writer],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    logger.info(
        "Writer execution started",
        extra={"extra_data": {
            "investigation_id": investigation_id,
            "session_id": session_id,
            "agent": "writer",
        }},
    )

    agent_start("writer")

    start = time.perf_counter()
    output = crew.kickoff()
    duration = time.perf_counter() - start

    tokens = extract_token_usage(output)

    agent_done(
        agent="writer",
        duration=duration,
        total_tokens=tokens["total_tokens"],
    )

    logger.info(
        "Writer execution completed",
        extra={"extra_data": {
            "investigation_id": investigation_id,
            "session_id": session_id,
            "agent": "writer",
            "duration_sec": round(duration, 2),
            **tokens,
        }},
    )

    return output.raw, {
        "duration_sec": round(duration, 2),
        **tokens,
    }
