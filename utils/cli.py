from datetime import datetime

def run_separator():
    print("─" * 60)

def ts():
    return datetime.now().strftime("%H:%M:%S")

def crew_start(run_id, investigation_id):
    print(f"[{ts()}] CREW STARTED | run_id={run_id} | investigation={investigation_id}")

def crew_done(duration, total_tokens):
    print(
        f"[{ts()}] CREW DONE | total={duration:.2f}s | tokens={total_tokens}"
    )

def agent_start(agent):
    print(f"[{ts()}] {agent.upper():<12} started")

def agent_done(agent, duration, total_tokens):
    print(
        f"[{ts()}] {agent.upper():<12} completed | "
        f"{duration:.2f}s | tokens={total_tokens}"
    )