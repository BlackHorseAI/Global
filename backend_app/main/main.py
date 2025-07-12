# main.py
import streamlit as st
import datetime
import pytz

# Modular imports
from config.settings import DAO_CONSTITUTION
from core.governance.dao import DAO
from core.identity.agent import Agent

# --- Initialize Application ---
st.set_page_config(page_title="The Global Payment Network", layout="wide")
st.title("🌐 The Global Payment Network")

# --- Context-Aware Configuration ---
TIMEZONE = pytz.timezone("America/Chicago") # CDT
current_time = datetime.datetime.now(TIMEZONE)
st.caption(f"**Operational Context:** United States | **Time:** {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

# --- Initialize Core Services & Agents ---
if 'dao' not in st.session_state: st.session_state.dao = DAO()
if 'agents' not in st.session_state:
    st.session_state.agents = {
        "verified_member_1": Agent(is_verified=True),
        "verified_member_2": Agent(is_verified=True),
        "new_member": Agent(is_verified=False)
    }

dao = st.session_state.dao
release_info = dao._constitution["governance"]["founder_control_release"]

# --- Main UI ---
st.header("Network Status")
st.success(f"Founder Control Released: {release_info['timestamp_utc']} — \"{release_info['final_message']}\". The DAO is fully sovereign.")
st.metric("DAO Treasury Balance", f"{dao.treasury_axm:,.0f} AXM")

st.header("Governance Actions")
st.info("The network now operates exclusively through DAO governance. Only fully verified members may participate in proposals and elections.")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Submit a Proposal")
    proposer_agent_id = st.selectbox(
        "Select Proposing Agent", 
        options=st.session_state.agents.keys(),
        format_func=lambda aid: f"{'Verified' if st.session_state.agents[aid].is_verified else 'Not Verified'} Agent ({aid[:8]}...)"
    )
    if st.button("Submit Test Proposal"):
        proposer_agent = st.session_state.agents[proposer_agent_id]
        success, message = dao.submit_proposal(proposer_agent, "Test Infrastructure Upgrade")
        if success:
            st.success(message)
        else:
            st.error(message)

with col2:
    st.subheader("Run for a Council Seat")
    candidate_agent_id = st.selectbox(
        "Select Candidate Agent", 
        options=st.session_state.agents.keys(),
        format_func=lambda aid: f"{'Verified' if st.session_state.agents[aid].is_verified else 'Not Verified'} Agent ({aid[:8]}...)",
        key="candidate_select"
    )
    if st.button("Submit Candidacy"):
        candidate_agent = st.session_state.agents[candidate_agent_id]
        success, message = dao.submit_candidacy(candidate_agent, "Ethics Council")
        if success:
            st.success(message)
        else:
            st.error(message)

with st.expander("View Full Constitution (Final Version)"):
    st.json(dao.get_constitution_as_json())