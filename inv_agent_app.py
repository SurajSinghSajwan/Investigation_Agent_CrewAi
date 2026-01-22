import os
import streamlit as st
from crewai import LLM
from crew.crew_builder import build_crew
from memory.session_store import SessionStore
from config import ASIMOV_BASE_URL, ASIMOV_MODEL

if "ASIMOV_API_KEY" in st.secrets:
    os.environ["ASIMOV_API_KEY"] = st.secrets["ASIMOV_API_KEY"]
    
ASIMOV_API_KEY = os.getenv("ASIMOV_API_KEY")

st.set_page_config(page_title="Investigation Assistant", layout="wide")
st.title("Investigation Assistant")


if "investigation_id" not in st.session_state:
    st.session_state.investigation_id = "INV-001"


store = SessionStore()
state = store.load(st.session_state.investigation_id) or {"messages": []}


llm = LLM(
    model=f"openai/{ASIMOV_MODEL}",
    base_url=ASIMOV_BASE_URL,
    api_key=ASIMOV_API_KEY,
)


for msg in state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])


user_input = st.chat_input("Ask an investigation-related question...")


if user_input:
    state["messages"].append(
        {"role": "user", "content": user_input}
    )

    session_id = st.runtime.scriptrunner.get_script_run_ctx().session_id
    with st.spinner("Investigating..."):
        result = build_crew(
            llm=llm,
            user_query=user_input,
            investigation_id=st.session_state.investigation_id,
            streamlit_session_id=session_id,
        )


    state["messages"].append(
        {"role": "assistant", "content": result}
    )

    store.save(st.session_state.investigation_id, state)
    st.rerun()
