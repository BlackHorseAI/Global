import streamlit as st
import uuid
import datetime
import pytz
import hashlib
import json
import time
import pandas as pd
import random

# --- 1. Core Architectural Components & Configuration ---

DAO_CONSTITUTION = {
    "Preamble": "We, the participants... for when one door closes, another will open in time.",
    "Article_I_DAO": {
        "title": "The Decentralized Autonomous Organization",
        "Section_1_Powers": "The DAO holds the power to vote on protocols. No voting on general proposals until all initial council seats are filled.",
        "Section_2_Voting_Principle": "One Human, One Vote, based on Proof-of-Personhood.",
        "Section_3_Voting_Eligibility": "1-year account age and good standing required to vote."
    },
    "Article_II_Governing_Councils": {
        "title": "The Governing Councils (Board, Ethics, CMA)",
        "Section_1_Composition": "Each council has 100 seats (90 elected, 10 by sortition).",
        "Section_2_Eligibility": "5-year account age, good standing, and verified credentials required.",
        "Section_3_Term": "5-year terms."
    },
    "Article_III_Proposal_Process": {
        "title": "The Proposal & Amendment Process",
        "Section_1_Eligibility": "2-year account age and full verification required.",
        "Section_2_Fee": "A non-refundable 100 AXM fee per proposal.",
        "Section_3_Deliberation": "A mandatory 6-month deliberation period for all proposals.",
        "Section_4_Lifecycle": "Requires sequential ratification: Community (90%), Ethics Council (95%), and Board of Members (95%)."
    },
    "Article_IV_Economics": {
        "title": "Treasury and Economics",
        "Section_1_AXM_Token": "The native asset is Axiom (AXM), with a total fixed supply of 250 Billion.",
        "Section_2_Treasury_Protocol": "The DAO maintains a Treasury, Investment Fund, and Legal Defense Fund."
    },
    "Article_V_Founder_Mandate": {
        "title": "The Founder's Mandate",
        "Section_1_Release": "Founder control was formally relinquished on July 12, 2025, with the final message, 'Be Outstanding.'",
        "Section_2_Reward": "The Founder's immutable reward schedule is constitutionally protected."
    }
}


class DAO:
    """Manages the governance and economy based on its locked constitution."""

    def __init__(self):
        self._constitution = DAO_CONSTITUTION
        self.treasury_axm: float = 135_000_000_000.0
        self.proposals = {}
        self.councils = {"Board": [], "Ethics": [], "CMA": []}

    def get_constitution_as_json(self) -> str:
        return json.dumps(self._constitution, sort_keys=True, indent=2)


class Agent:
    """Represents a participant in the economy."""

    def __init__(self, name: str, is_founder: bool = False):
        self.agent_id = str(uuid.uuid4())
        self.name = name
        self.is_founder = is_founder


# --- 2. Main Application UI ---
st.set_page_config(page_title="The Global Payment Network", layout="wide")
st.title("🌐 The Global Payment Network")

# --- Context & State Initialization ---
TIMEZONE = pytz.timezone("America/Los_Angeles")  # PDT
current_time = datetime.datetime.now(TIMEZONE)
st.caption(f"**Operational Context:** United States | **Time:** {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

if 'dao' not in st.session_state: st.session_state.dao = DAO()
if 'founder' not in st.session_state: st.session_state.founder = Agent(name="The Founder", is_founder=True)
if 'genesis_created' not in st.session_state: st.session_state.genesis_created = False

# --- UI: Founder Controls (Sidebar) ---
with st.sidebar:
    st.header("👑 Founder Control Panel")
    founder = st.session_state.founder

    if founder.is_founder:
        st.success("Founder privileges are ACTIVE.")

        if 'confirming_launch' not in st.session_state: st.session_state.confirming_launch = False
        if 'confirming_relinquish' not in st.session_state: st.session_state.confirming_relinquish = False

        if not st.session_state.genesis_created:
            if st.button("🚀 Launch Network", type="primary"):
                st.session_state.confirming_launch = True

        if st.button("🔥 Relinquish Privileges"):
            st.session_state.confirming_relinquish = True

        # HARDENING FIX: Confirmation dialogues for irreversible actions
        if st.session_state.confirming_launch:
            st.error("Are you sure you want to launch the network? This will create the Genesis Block.")
            if st.button("Confirm Launch"):
                st.session_state.genesis_created = True
                st.session_state.confirming_launch = False
                st.balloons()
                st.rerun()
            if st.button("Cancel Launch"):
                st.session_state.confirming_launch = False
                st.rerun()

        if st.session_state.confirming_relinquish:
            st.error("Are you sure? This action is permanent.")
            if st.button("Confirm Relinquishment"):
                founder.is_founder = False
                st.session_state.confirming_relinquish = False
                st.rerun()
            if st.button("Cancel Relinquishment"):
                st.session_state.confirming_relinquish = False
                st.rerun()
    else:
        st.error("Founder privileges are INACTIVE.")
        st.info("The network is fully decentralized.")

# --- Main UI Tabs ---
st.header("Network Dashboard")

if st.session_state.genesis_created:
    st.success("Network Status: **Online**")
    tab1, tab2 = st.tabs(["🏛️ Governance", "📜 Constitution"])
    with tab1:
        st.subheader("DAO Treasury")
        st.metric("Treasury Balance", f"{st.session_state.dao.treasury_axm:,.0f} AXM")
    with tab2:
        st.subheader("The Constitution")
        st.json(st.session_state.dao.get_constitution_as_json())
else:
    st.warning("Network Status: **Offline**")
    st.info("The Founder must launch the network using the control panel in the sidebar.")